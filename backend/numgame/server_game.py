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
# Project Dependencies
from numgame.data_management import get_db
from numgame.data_models import players
from numgame.utils import (
    generate_uuid,
    decide_is_user_first
)
from numgame.redis_manager import get_redis
from numgame.game_process import (
    initializeBotPlay,
    deleteData
)
from numgame.bot_controller import BotStateMachine
from numgame.token_management import (
    search_user_token
)
from numgame.config import settings
# ORM dependencies
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated
# Redis
import redis.asyncio as aioredis

# logger
logger = logging.getLogger("Game Server")
# Router
router = APIRouter(prefix="/game")


# Play with bot
@router.websocket("/botPlay")
async def botPlay(websocket: WebSocket,
                  session: Annotated[AsyncSession, Depends(get_db)],
                  redis: aioredis.Redis = Depends(get_redis)):
    # Accept connection
    await websocket.accept()
    # Basic game settings
    game_id = generate_uuid()
    redis_storage_id = f"bot_game:{game_id}"
    is_game_initialized = False
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
                    # Initialize the game
                    await initializeBotPlay(client=redis, game_id=redis_storage_id)
                    is_game_initialized = True
                    # Decide first move
                    is_user_first = decide_is_user_first()
                    # initialize bot
                    bot = BotStateMachine()
                    # Track whether the game is finished
                    game_finished = asyncio.Event()

                    # Heart Beat
                    async def send_heartbeat():
                        while not game_finished.is_set():
                            # Interval for sending heartbeat
                            await asyncio.sleep(settings.heartbeat_interval)
                            # heartbeat content
                            heartbeat_content = {
                                "type": "heartbeat",
                                "time_stamp": asyncio.get_running_loop().time()
                            }
                            await websocket.send_json(heartbeat_content)

                    # Tasks
                    heartbeat_task = asyncio.create_task(send_heartbeat())
                    # Wait for the task to get complete
                    await asyncio.wait(
                        [heartbeat_task],
                        return_when=asyncio.FIRST_COMPLETED
                    )
                    # Cancel tasks
                    heartbeat_task.cancel()
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
    # Handle the game info deleting at the end
    if is_game_initialized:
        await deleteData(client=redis, game_id=redis_storage_id)
