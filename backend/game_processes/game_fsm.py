from logging import getLogger
import asyncio
# Redis
import redis.asyncio as aioredis
# FastAPI
from fastapi import WebSocket
# project dependencies
from data_management.enums import (
    GameState,
    WSResponseType,
    Operations,
    FailReason
)
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
                 target = 10
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
        self.target = target

    # Start
    async def start(self):
        logger.info("Game starting")
        await self.state_transition(GameState.INIT)

    # game initialize
    async def game_initialize(self, target: int):
        logger.info("Game initialize")
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
        logger.info("Bot turn start")
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

    # User state
    async def user_turn_start(self):
        logger.info("New user turn start")
        content = {
            "type": WSResponseType.PLAYER_TURN_START.value
        }
        await self.ws_client.send_json(content)

    # User operation execution
    async def user_operation(self, operation: Operations):
        logger.info("New user operation")
        if self.state == GameState.PLAYER_TURN:
            # Skip turn
            if operation == Operations.SKIP:
                # Change game state
                if self.is_user_first:
                    await self.state_transition(GameState.BOT_TURN)
                else:
                    await self.state_transition(GameState.PLAYER_TURN)
            else:
                # Execution turn
                logger.info("Start executing user operation")
                result = await self.game.playerOperationExecution(operation)
                if result["success"]:
                    content = {
                        "type": WSResponseType.PLAYER_OPERATION.value,
                        "success": True,
                    }
                    await self.ws_client.send_json(content)
                else:
                    content = {
                        "type": WSResponseType.PLAYER_OPERATION.value,
                        "success": False,
                        "reason": result["reason"].value
                    }
                    await self.ws_client.send_json(content)
        else:
            content = {
                "type": WSResponseType.PLAYER_OPERATION.value,
                "success": False,
                "reason": FailReason.NOT_YOUR_TURN.value
            }
            await self.ws_client.send_json(content)

    # State process
    async def on_enter_state(self, new_state: GameState):
        if new_state == GameState.INIT:
            await self.game_initialize(self.target)
        elif new_state == GameState.BOT_TURN:
            await self.bot_turn()
        elif new_state == GameState.PLAYER_TURN:
            await self.user_turn_start()

    # State Transition
    async def state_transition(self, new_state: GameState):
        async with self.lock:
            logger.info(f"State transition: {self.state} -> {new_state}")
            self.state = new_state
            await self.on_enter_state(new_state)
