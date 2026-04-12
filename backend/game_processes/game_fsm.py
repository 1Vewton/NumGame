from logging import getLogger
import asyncio
from typing import Annotated
# Redis
import redis.asyncio as aioredis
# FastAPI
from fastapi import WebSocket, Depends
# sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    select,
    update
)
from datetime import datetime
# project dependencies
from data_management.enums import (
    GameState,
    WSResponseType,
    Operations,
    FailReason,
    TurnFinishReason
)
from data_management.data_models import players, games
from game_processes.bot_game_process import BotGameProcess
from utils.utils import (
    generate_uuid,
    decide_is_user_first
)
from game_processes.bot_controller import BotStateMachine
from data_management.data_management import get_db
from utils.config import settings

logger = getLogger("game_fsm")


# Game state machine
class BotGameStateMachine:
    def __init__(self,
                 session: Annotated[AsyncSession, Depends(get_db)],
                 player_id: str,
                 player_timeout: int,
                 game_finished_event: asyncio.Event,
                 client: WebSocket,
                 redis_client: aioredis.Redis,
                 target=10,
                 ):
        # Database session
        self.session = session
        # websocket client
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
        self.player_id = player_id
        self.start_time = None
        self.end_time = None
        self.round = 0
        self.is_player_win = True
        self.user_executing = asyncio.Event()
        self.player_timeout = player_timeout
        # Game finished asyncio event: Stop the game
        self.game_finished_event = game_finished_event

    # Start
    async def start(self):
        self.start_time = datetime.now()
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
        # Limit the maximum execution turns
        execution_turns = 0
        # Execution of operations
        while await self.game.getBotActionPoint() >= await self.game.getOperationCost() \
                and execution_turns < settings.maximum_bot_operation_times:
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
            execution_turns += 1
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
                content = {
                    "type": WSResponseType.TURN_FINISH.value,
                    "reason": TurnFinishReason.FRONTEND_OPERATION.value
                }
                await self.ws_client.send_json(content)
                # Change game state
                if self.is_user_first:
                    await self.state_transition(GameState.BOT_TURN)
                else:
                    await self.state_transition(GameState.SETTLEMENT)
                self.user_executing.set()
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

    # Game finished
    async def game_finished(self):
        # Users info
        first_move_user_id = None
        second_move_user_id = None
        bot_id = None
        # log
        if self.is_player_win:
            logger.info("Player win")
        else:
            logger.info("Bot win")
        # Update user info
        user_info = await self.session.execute(
            select(players).where(
                players.id == self.player_id
            )
        )
        result = user_info.first()
        if result:
            processed_result = result[0]
            new_total_games = processed_result.total_games + 1
            await self.session.execute(
                update(players).
                where(players.id == self.player_id).
                values(total_games=new_total_games)
            )
            logger.info("User info update complete")
            # Record the user id to get stored in the games table
            if self.is_user_first:
                first_move_user_id = self.player_id
            else:
                second_move_user_id = self.player_id
            # User win process
            if self.is_player_win:
                new_wins = processed_result.wins + 1
                await self.session.execute(
                    update(players).
                    where(players.id == self.player_id).
                    values(wins=new_wins)
                )
                # Content to send to the front-end
                content = {
                    "type": WSResponseType.PLAYER_WIN.value,
                }
                await self.ws_client.send_json(content)
        # update bot info
        bot_info = await self.session.execute(
            select(players).where(
                players.user_name == settings.simple_bot_name
            )
        )
        result = bot_info.first()
        if result:
            processed_result = result[0]
            new_total_games = processed_result.total_games + 1
            await self.session.execute(
                update(players).
                where(players.user_name == settings.simple_bot_name).
                values(total_games=new_total_games)
            )
            logger.info("Bot profile update successful")
            # Record bot info for games record
            bot_id = processed_result.id
            if self.is_user_first:
                second_move_user_id = bot_id
            else:
                first_move_user_id = bot_id
            # Update bot winning
            if not self.is_player_win:
                new_wins = processed_result.wins + 1
                await self.session.execute(
                    update(players).
                    where(players.id == bot_id).
                    values(wins=new_wins)
                )
                content = {
                    "type": WSResponseType.BOT_WIN.value
                }
                await self.ws_client.send_json(content)
        self.end_time = datetime.now()
        # Data for the game to get stored
        if self.is_player_win:
            new_game_data = games(
                id=self.game_id,
                first_move=first_move_user_id,
                second_move=second_move_user_id,
                winner=self.player_id,
                rounds=self.round,
                started_time=self.start_time,
                ended_time=self.end_time
            )
        else:
            new_game_data = games(
                id=self.game_id,
                first_move=first_move_user_id,
                second_move=second_move_user_id,
                winner=bot_id,
                rounds=self.round,
                started_time=self.start_time,
                ended_time=self.end_time
            )
        self.session.add(new_game_data)
        # Game finished
        self.game_finished_event.set()

    # Settlement
    async def game_settlement(self):
        logger.info("Start game settlement")
        self.round += 1
        await self.game.nextTurn()
        player_score = await self.game.getPlayerScore()
        bot_score = await self.game.getBotScore()
        target = await self.game.getTarget()
        # update user status
        user_status = await self.game.updateUserStatus()
        content = {
            "type": WSResponseType.DATA_UPDATE.value,
            "data": user_status
        }
        await self.ws_client.send_json(content)
        if (player_score > target
                and bot_score > target):
            self.end_time = datetime.now()
            if player_score > bot_score:
                self.is_player_win = True
            elif bot_score > player_score:
                self.is_player_win = False
            await self.state_transition(GameState.FINISH)
        else:
            # Turn to other states
            if self.is_user_first:
                await self.state_transition(GameState.PLAYER_TURN)
            else:
                await self.state_transition(GameState.BOT_TURN)
        # Send content
        content = {
            "type": WSResponseType.BOT_TURN_FINISH.value
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
            # Wait til user finished or timeout
            try:
                await asyncio.wait_for(
                    self.user_executing.wait(),
                    timeout=self.player_timeout
                )
            except asyncio.TimeoutError:
                logger.info("Timeout, force state switching")
                content = {
                    "type": WSResponseType.TURN_FINISH.value,
                    "reason": TurnFinishReason.TIMEOUT.value
                }
                await self.ws_client.send_json(content)
            self.user_executing.clear()
        elif new_state == GameState.SETTLEMENT:
            await self.game_settlement()
        elif new_state == GameState.FINISH:
            await self.game_finished()

    # State Transition
    async def state_transition(self, new_state: GameState):
        async with self.lock:
            logger.info(f"State transition: {self.state} -> {new_state}")
            self.state = new_state

    # Run loop
    async def run_game_loop(self):
        logger.info("Start executing game loop")
        # Execution loop
        while not self.game_finished_event.is_set():
            state = self.state
            await self.on_enter_state(state)
            if self.state == GameState.FINISH:
                break

    # End game
    async def end_game(self):
        await self.game.deleteData()
