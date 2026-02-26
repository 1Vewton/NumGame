from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from collections.abc import AsyncGenerator
from typing import Any, Annotated
from numgame.data_management import init_models, get_db
from numgame.data_models import players
from numgame.request_body import NewPlayerData
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from numgame.utils import generate_uuid
from logging import getLogger

# run before execution
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:
    await init_models()
    yield

# Basic Settings
logger = getLogger("Server")
# APP
app = FastAPI(
    lifespan=lifespan,
    title="NumGame Server",
    description="Backend Server for NumGame"
)

# Register API
@app.post(path="/api/userRegister")
async def userRegister(new_user: NewPlayerData, session: Annotated[AsyncSession, Depends(get_db)]):
    logger.info("Creating new user")
    try:
        # Set data
        registration_date = datetime.now()
        player_id = generate_uuid()
        user_name = new_user.player_name
        existing = await session.execute(select(players).where(players.user_name == user_name))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Username already exists")
        # New player instance
        new_player_data = players(id=player_id, user_name=user_name, registered_at=registration_date)
        # Add it to database
        session.add(new_player_data)
    except Exception as e:
        logger.error(f"User registration failed due to {e}")
        raise HTTPException(status_code=500, detail=f"User registration failed")