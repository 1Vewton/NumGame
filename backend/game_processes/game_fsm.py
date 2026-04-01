from logging import getLogger
import asyncio
# Redis
import redis.asyncio as aioredis
# FastAPI
from fastapi import WebSocket
# project dependencies
from data_management.enums import GameState
from game_processes.bot_game_process import BotGameProcess
from utils.utils import (
    generate_uuid,
    decide_is_user_first
)
from data_management.enums import WSResponseType

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

    # State process
    async def on_enter_state(self, new_state: GameState):
        pass

    # State Transition
    async def state_transition(self, new_state: GameState):
        async with self.lock:
            logger.info(f"State transition: {self.state} -> {new_state}")
            self.state = new_state
            await self.on_enter_state(new_state)
