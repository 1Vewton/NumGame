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
    Operations,
    WSResponseType
)
from utils.utils import (
    decide_is_user_first
)
from utils.token_management import (
    search_user_token
)
from utils.config import settings
from game_processes.redis_manager import get_redis
from game_processes.game_fsm import BotGameStateMachine
# ORM dependencies
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated
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
    target = int(websocket.query_params.get("target"))
    player_timeout = int(websocket.query_params.get("player_timeout"))
    # Accept connection
    await websocket.accept()
    # Basic game settings
    is_game_initialized = False
    game = None
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
                    move_info = {
                        "type": WSResponseType.MOVE_DIVISION.value,
                        "first_move": is_user_first
                    }
                    await websocket.send_json(move_info)
                    # Track whether the game is finished
                    game_finished = asyncio.Event()
                    # Initialize the game
                    is_game_initialized = True
                    game = BotGameStateMachine(
                        session=session,
                        player_id=user_id,
                        player_timeout=player_timeout,
                        game_finished_event=game_finished,
                        client=websocket,
                        redis_client=redis,
                        target=target
                    )
                    await game.start()
                    # Heartbeat Sequence Number
                    next_sequence = 0
                    timeout_count = 0
                    # Pending
                    pending_hb = {}

                    # Game loop
                    async def game_loop():
                        logger.info("Game loop executed")
                        await game.run_game_loop()

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
                                    "type": WSResponseType.HEARTBEAT.value,
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

                    # Message receiving
                    async def receive_message():
                        try:
                            while not game_finished.is_set():
                                # Receive message
                                message = await websocket.receive_json()
                                msg_type = WSResponseType(message.get("type"))
                                # If it is a response for the heartbeat
                                if msg_type == WSResponseType.HEARTBEAT:
                                    sequence_res = message.get("sequence")
                                    # Finish the heartbeat
                                    if sequence_res is not None and sequence_res in pending_hb.keys():
                                        future = pending_hb[sequence_res]
                                        if not future.done():
                                            future.set_result(True)
                                    else:
                                        logger.error(f"Cannot find heartbeat with sequence {sequence_res}")
                                elif msg_type == WSResponseType.PLAYER_OPERATION:
                                    # operation execution
                                    operation = message.get("operation")
                                    if operation is not None:
                                        await game.user_operation(Operations(operation))
                                    else:
                                        logger.error("No operation found")
                        except WebSocketDisconnect:
                            logger.error("Client disconnected during main game process")
                        except Exception as e:
                            logger.error(f"Main game process failed due to {e}")
                        finally:
                            game_finished.set()

                    # Tasks
                    game_loop_task = asyncio.create_task(game_loop())
                    heartbeat_task = asyncio.create_task(send_heartbeat())
                    receive_message_task = asyncio.create_task(receive_message())
                    # Wait for the task to get complete
                    await asyncio.wait(
                        [
                            heartbeat_task,
                            receive_message_task,
                            game_loop_task
                        ],
                        return_when=asyncio.FIRST_COMPLETED
                    )
                    # Cancel tasks
                    heartbeat_task.cancel()
                    receive_message_task.cancel()
                    game_loop_task.cancel()
                    try:
                        await heartbeat_task
                        await receive_message_task
                        await game_loop_task
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
            await game.end_game()
