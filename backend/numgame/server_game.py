import logging
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
from numgame.utils import generate_uuid
from numgame.redis_manager import get_redis
from numgame.game_process import (
    initializeBotPlay
)
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
    redis_storage_id = f"game_{game_id}"
    is_game_initialized = False
    try:
        # Check user info
        logger.info("Checking user info")
        user_id = websocket.cookies.get("user_id")
        if user_id:
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
            else:
                # User not exist
                await websocket.close(code=1008, reason="User not found")
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
        pass
