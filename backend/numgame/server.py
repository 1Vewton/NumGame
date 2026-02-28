from numgame.config import settings
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from collections.abc import AsyncGenerator
from typing import Any, Annotated
from numgame.data_management import init_models, get_db
from numgame.data_models import players
from numgame.request_body import (
    PlayerData,
    NewPlayerData,
    LoginPlayerData
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from numgame.utils import generate_uuid
from logging import getLogger
import uvicorn

# run before execution
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:
    await init_models()
    yield

# Basic Settings
logger = getLogger("Server")
tags = [
    {
        "name": "userRegister",
        "description": "The api for registration of user"
    },
    {
        "name": "userLogin",
        "description": "The api for login of user"
    },
    {
        "name": "autoLogin",
        "description": "The api for auto login of user"
    }
]
# APP
app = FastAPI(
    lifespan=lifespan,
    title="NumGame Server",
    description="Backend Server for NumGame",
    openapi_tags=tags
)

# Register API
@app.post(path="/api/userRegister", tags=["userRegister"])
async def userRegister(new_user: NewPlayerData, session: Annotated[AsyncSession, Depends(get_db)]):
    logger.info("Creating new user")
    try:
        # Set data
        registration_date = datetime.now()
        player_id = generate_uuid()
        user_name = new_user.player_name
        existing = await session.execute(select(players).where(players.user_name == user_name))
        if existing.scalar_one_or_none():
            content = {
                "success": False,
                "reason": "Username already exists"
            }
            return JSONResponse(content=content, status_code=409)
        # New player instance
        new_player_data = players(id=player_id, user_name=user_name, registered_at=registration_date)
        # Add it to database
        session.add(new_player_data)
        # Response
        content = {
            "success": True,
            "user_name": new_player_data.user_name,
            "user_id": new_player_data.id
        }
        return JSONResponse(content=content, status_code=201)
    except Exception as e:
        logger.error(f"User registration failed due to {e}")
        # Response
        content = {
            "success": False,
            "reason": str(e)
        }
        return JSONResponse(content=content, status_code=500)
# API to get user info
@app.post(path="/api/userLogin", tags=["userLogin"])
async def userLogin(user: LoginPlayerData, session: Annotated[AsyncSession, Depends(get_db)]):
    logger.info("Logging in user")
    try:
        user_name = user.player_name
        # Query
        user_info = await session.execute(select(players).where(players.user_name == user_name))
        result = user_info.first()
        if result:
            result_processed = result[0]
            # Response
            content = {
                "success": True,
                "user_name": result_processed.user_name,
                "user_id": result_processed.id
            }
            response = JSONResponse(content=content, status_code=200)
            response.set_cookie(key="user_id", value=result_processed.id, httponly=True)
            return response
        else:
            # When the user name does not exist
            content = {
                "success": False,
                "reason": "Username does not exist"
            }
            response = JSONResponse(content=content, status_code=401)
            return response
    except Exception as e:
        # Error Handling
        logger.error(f"User login failed due to {e}")
        # Response
        content = {
            "success": False,
            "reason": str(e)
        }
        return JSONResponse(content=content, status_code=500)
# API to auto login
@app.get(path="/api/autoLogin", tags=["autoLogin"])
async def autoLogin(request:Request, session: Annotated[AsyncSession, Depends(get_db)]):
    logger.info("automatically login user")
    try:
        # Get cookie
        user_id = request.cookies.get("user_id")
        # Check if user id exists.
        if user_id:
            pass
        else:
            content = {
                "success": False,
                "reason": "User id does not exist"
            }
            return JSONResponse(content=content, status_code=401)
    except Exception as e:
        # Error handling
        logger.error(f"Auto login failed due to {e}")
        # Response
        content = {
            "success": False,
            "reason": str(e)
        }
        return JSONResponse(content=content, status_code=500)

# run server
def run():
    logger.info("Starting server")
    uvicorn.run(app, host="localhost", port=settings.server_port)

if __name__ == "__main__":
    run()