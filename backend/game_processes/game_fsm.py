from logging import getLogger
import asyncio
# Redis
import redis.asyncio as aioredis
# FastAPI
from fastapi import WebSocket
# project dependencies
from data_management.enums import GameState, WSResponseType
from game_processes.bot_game_process import BotGameProcess
from utils.utils import (
    generate_uuid,
    decide_is_user_first
)
from game_processes.bot_controller import BotStateMachine

logger = getLogger("game_fsm")


# Game state machine
class GameStateMachine:
    def __init__(self,
                 client: WebSocket,
                 redis_client: aioredis.Redis,
                 ):
        self.ws_client = client
        # async lock
        self.lock = asyncio.Lock()
        self.state = GameState.INIT
        # Game
        self.game_id = f"game:{generate_uuid()}"
        self.game = BotGameProcess(
            client=redis_client,
            game_id=self.game_id,
        )
        self.is_user_first = False
        self.bot_state_machine = BotStateMachine()

    # game initialize
    async def game_initialize(self, target: int):
        self.is_user_first = decide_is_user_first()
        await self.game.initializeBotPlay(
            is_user_first=self.is_user_first,
            target=target
        )
        move_info = {
            "type": WSResponseType.MOVE_DIVISION.value,
            "first_move": self.is_user_first
        }
        await self.ws_client.send_json(move_info)
        # Transition
        if self.is_user_first:
            await self.state_transition(GameState.PLAYER_TURN)
        else:
            await self.state_transition(GameState.BOT_TURN)

    # Bot actions
    async def bot_turn(self):
        content = {
            "type": WSResponseType.BOT_TURN_START.value,
        }
        await self.ws_client.send_json(content)
        # Execution of operations
        while await self.game.getBotActionPoint() >= await self.game.getOperationCost():
            bot_status = await self.game.getBotStatus()
            self.bot_state_machine.update_state(
                point=bot_status.point,
                opponent_point=bot_status.opponent_point,
                productivity=bot_status.productivity,
                destructivity=bot_status.destructivity,
                target=bot_status.target
            )
            operation = self.bot_state_machine.choose_action()
            result = await self.game.botOperationExecution(operation)
            if result["success"]:
                data = await self.game.updateUserStatus()
                content = {
                    "type": WSResponseType.DATA_UPDATE.value,
                    "data": data
                }
                await self.ws_client.send_json(content)
            else:
                break
        # Turn to next
        if self.is_user_first:
            await self.state_transition(GameState.SETTLEMENT)
        else:
            await self.state_transition(GameState.PLAYER_TURN)

    # State process
    async def on_enter_state(self, new_state: GameState):
        pass

    # State Transition
    async def state_transition(self, new_state: GameState):
        async with self.lock:
            logger.info(f"State transition: {self.state} -> {new_state}")
            self.state = new_state
            await self.on_enter_state(new_state)
