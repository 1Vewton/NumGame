import logging
from typing import Annotated
# FastAPI dependencies
from fastapi import Depends, Request, APIRouter
from fastapi.responses import JSONResponse
# Project dependencies
from numgame.data_management import get_db
from numgame.data_models import players
from numgame.request_body import (
    PlayerData,
    NewPlayerData,
    LoginPlayerData
)
from numgame.utils import generate_uuid, limiter
# ORM Dependencies
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

# Logger
logger = logging.getLogger("User Management Server")
#API Router
user_router = APIRouter(prefix="/user")

# User management APIs.
# Register API
@user_router.post(path="/userRegister", tags=["userRegister"])
@limiter.limit("5/minute")
async def userRegister(request:Request,
                       new_user: NewPlayerData,
                       session: Annotated[AsyncSession, Depends(get_db)]):
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
@user_router.post(path="/userLogin", tags=["userLogin"])
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
@user_router.get(path="/autoLogin", tags=["autoLogin"])
async def autoLogin(request:Request, session: Annotated[AsyncSession, Depends(get_db)]):
    logger.info("automatically login user")
    try:
        # Get cookie
        user_id = request.cookies.get("user_id")
        # Check if user id exists.
        if user_id:
            # Get user from dB
            user_info = await session.execute(select(players).where(players.id == user_id))
            result = user_info.first()
            if result:
                # Successfully logged in
                processed_result = result[0]
                content = {
                    "success": True,
                    "user_name": processed_result.user_name,
                    "user_id": processed_result.id
                }
                # Set response and cookie
                response = JSONResponse(content=content, status_code=200)
                response.set_cookie(key="user_id", value=processed_result.id, httponly=True)
                return response
            else:
                content = {
                    "success": False,
                    "reason": "User id does not exist"
                }
                return JSONResponse(content=content, status_code=401)
        else:
            content = {
                "success": False,
                "reason": "User id not found"
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
# info getting API
@user_router.post(path="/userInfo", tags=["userInfo"])
async def userInfo(request:Request,
                   player_data:PlayerData,
                   session: Annotated[AsyncSession, Depends(get_db)]):
    logger.info("Requesting user information")
    try:
        # Get cookie
        user_id = request.cookies.get("user_id")
        if user_id:
            # User info query
            user_info = await session.execute(
                select(players).where(
                    (players.id == user_id) &
                    (players.id == player_data.player_id) &
                    (players.user_name == player_data.player_name)
                )
            )
            result = user_info.first()
            if result:
                # Get the fetch result and turn it into dict
                processed_result = result[0]
                result_dict = processed_result.to_dict()
                # Response
                content = {
                    "success": True,
                    "result": result_dict
                }
                return JSONResponse(content=content, status_code=200)
            else:
                # If the user is not found
                content = {
                    "success": False,
                    "reason": "User not found or conflict with your cookie"
                }
                return JSONResponse(content=content, status_code=401)
        else:
            # When cookie is not found
            content = {
                "success": False,
                "reason": "Please login first"
            }
            return JSONResponse(content=content, status_code=401)
    except Exception as e:
        # Error handling
        logger.error(f"Info fetching failed due to {e}")
        # Response
        content = {
            "success": False,
            "reason": str(e)
        }
        return JSONResponse(content=content, status_code=500)