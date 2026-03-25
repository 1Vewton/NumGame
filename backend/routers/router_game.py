import logging
import asyncio
# FastAPI
from fastapi import (
    APIRouter,
    WebSocket,
    Depends,
    WebSocketDisconnect,
    WebSocketException
)
from fastapi.responses import JSONResponse
# Project Dependencies
from data_management.data_management import get_db
from data_management.data_models import players
from data_management.enums import (
    BotGamePlayer
)
from utils.utils import (
    generate_uuid,
    decide_is_user_first
)
from utils.token_management import (
    search_user_token
)
from utils.config import settings
from game_processes.redis_manager import get_redis
from game_processes.bot_game_process import BotGameProcess
from game_processes.bot_controller import BotStateMachine
# ORM dependencies
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated
from datetime import datetime
# Redis
import redis.asyncio as aioredis

# logger
logger = logging.getLogger("Game Server")
# Router
game_router = APIRouter(prefix="/game")


# Game server test endpoint
@game_router.get("/test", tags=["test"])
async def test():
    return JSONResponse(
        status_code=200,
        content={
            "message": "Hello World!"
        }
    )


# Play with bot
@game_router.websocket("/botPlay")
async def botPlay(websocket: WebSocket,
                  session: Annotated[AsyncSession, Depends(get_db)],
                  redis: aioredis.Redis = Depends(get_redis)):
    # Get info from the connection
    target = websocket.query_params.get("target")
    # Accept connection
    await websocket.accept()
    # Basic game settings
    game_id = generate_uuid()
    redis_storage_id = f"bot_game:{game_id}"
    is_game_initialized = False
    game = BotGameProcess(
        client=redis,
        game_id=redis_storage_id
    )
    try:
        # Check user info
        logger.info("Checking user info")
        login_token = websocket.cookies.get("login_token")
        if login_token:
            search_user_id = await search_user_token(
                token=login_token,
                client=redis
            )
            if search_user_id["success"]:
                user_id = search_user_id["user_id"]
                # Check whether the cookie exists
                user_info = await session.execute(
                    select(players).where(
                        players.id == user_id
                    )
                )
                result = user_info.first()
                # Check whether the user exists
                if result:
                    # Decide first move
                    is_user_first = decide_is_user_first()
                    if is_user_first:
                        move_info = {
                            "type": "move_division",
                            "first_move": True
                        }
                    else:
                        move_info = {
                            "type": "move_division",
                            "first_move": True
                        }
                    await websocket.send_json(move_info)
                    # Initialize the game
                    await game.initializeBotPlay(
                        target=int(target),
                        is_user_first=is_user_first
                    )
                    game_start_time = datetime.now()
                    is_game_initialized = True
                    # initialize bot
                    bot = BotStateMachine()
                    # Track whether the game is finished
                    game_finished = asyncio.Event()
                    # Bot turn
                    is_bot_turn = asyncio.Event()
                    # Heartbeat Sequence Number
                    next_sequence = 0
                    timeout_count = 0
                    # Pending
                    pending_hb = {}

                    # Heart Beat
                    async def send_heartbeat():
                        nonlocal next_sequence, timeout_count
                        try:
                            while not game_finished.is_set():
                                # Interval for sending heartbeat
                                await asyncio.sleep(settings.heartbeat_interval)
                                # Sequence processing
                                sequence = next_sequence
                                next_sequence += 1
                                # Add it into pending hbs
                                hb = asyncio.get_running_loop().create_future()
                                pending_hb[sequence] = hb
                                # heartbeat content
                                heartbeat_content = {
                                    "type": "heartbeat",
                                    "time_stamp": asyncio.get_running_loop().time(),
                                    "sequence": sequence
                                }
                                # Send heartbeat
                                await websocket.send_json(heartbeat_content)
                                # Waiting for receiving
                                try:
                                    await asyncio.wait_for(hb, timeout=settings.heartbeat_timeout)
                                    # Clear the timeout count
                                    timeout_count = 0
                                    logger.info(f"Heartbeat {sequence} acknowledged")
                                except asyncio.TimeoutError:
                                    timeout_count += 1
                                    logger.error(f"Heartbeat {sequence} timed out")
                                    # Timeout count exceed the total timeout allowed
                                    if timeout_count >= settings.total_timeout_cnt:
                                        await websocket.close(code=1008,
                                                              reason=(
                                                                  "Heartbeat timeout exceeded "
                                                                  f"Maximum timeout count {settings.total_timeout_cnt}"
                                                              ))
                                        game_finished.set()
                                        return
                                except asyncio.CancelledError:
                                    break
                                finally:
                                    # Clearer
                                    pending_hb.pop(sequence, None)
                        except WebSocketDisconnect:
                            logger.warning("Client disconnected during heartbeat process")
                        except Exception as e:
                            logger.error(f"Heartbeat failed due to {e}")
                        finally:
                            # Finish the game
                            game_finished.set()

                    # Bot operating
                    async def bot_operating():
                        while not game_finished.is_set():
                            await is_bot_turn.wait()
                            # Update the state of the bot
                            game_state = await game.getBotStatus()
                            bot.update_state(
                                point=game_state.point,
                                opponent_point=game_state.opponent_point,
                                target=game_state.target,
                                destructivity=game_state.destructivity,
                                productivity=game_state.productivity
                            )
                            # Start executing
                            bot_action_point = await game.getBotActionPoint()
                            cost = await game.getOperationCost()
                            while bot_action_point >= cost:
                                operation = bot.choose_action()
                                await game.botOperationExecution(operation)
                                cost = await game.getOperationCost()
                            is_bot_turn.clear()

                    # Message receiving
                    async def receive_message():
                        try:
                            while not game_finished.is_set():
                                # Receive message
                                message = await websocket.receive_json()
                                msg_type = message.get("type")
                                # If it is a response for the heartbeat
                                if msg_type == "heartbeat":
                                    sequence_res = message.get("sequence")
                                    # Finish the heartbeat
                                    if sequence_res is not None and sequence_res in pending_hb.keys():
                                        future = pending_hb[sequence_res]
                                        if not future.done():
                                            future.set_result(True)
                                    else:
                                        logger.error(f"Cannot find heartbeat with sequence {sequence_res}")
                                elif msg_type == "player_operation":
                                    # Get operation id
                                    operation_id = message.get("operation_id")
                                    operation = message.get("operation")
                                    current_player = await game.getCurrentPlayer()
                                    # Check whether this is the turn for the player
                                    if current_player == BotGamePlayer.PLAYER:
                                        pass
                                    else:
                                        content = {
                                            "type": "execution_result",
                                            "operation_id": operation_id,
                                            "success": False,
                                            "reason": "This is not your turn"
                                        }
                                        await websocket.send_json(content)
                        except WebSocketDisconnect:
                            logger.error("Client disconnected during main game process")
                        except Exception as e:
                            logger.error(f"Main game process failed due to {e}")
                        finally:
                            game_finished.set()

                    # Tasks
                    heartbeat_task = asyncio.create_task(send_heartbeat())
                    receive_message_task = asyncio.create_task(receive_message())
                    # Wait for the task to get complete
                    await asyncio.wait(
                        [heartbeat_task,
                         receive_message_task],
                        return_when=asyncio.FIRST_COMPLETED
                    )
                    # Cancel tasks
                    heartbeat_task.cancel()
                    receive_message_task.cancel()
                    try:
                        await heartbeat_task
                        await receive_message_task
                    except asyncio.CancelledError:
                        pass
                else:
                    # User not exist
                    await websocket.close(code=1008, reason="User not found")
            else:
                await websocket.close(code=1008, reason="Token invalid or expired")
        else:
            # Cookie not exist
            await websocket.close(code=1008, reason="Please log in first!")
    except WebSocketDisconnect:
        # Error handling of web socket disconnect
        logger.warning("User disconnected")
    except WebSocketException as e:
        # Error handling of the web socket error
        await websocket.close(code=e.code, reason=str(e))
    except Exception as e:
        # Error handling of other errors
        await websocket.close(code=1011, reason=str(e))
    finally:
        # Handle the game info deleting at the end
        if is_game_initialized:
            await game.deleteData()
