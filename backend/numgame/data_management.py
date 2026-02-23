from numgame.config import settings
from numgame.data_models import Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from collections.abc import AsyncGenerator
from typing import Any
import logging

logger = logging.getLogger("DataBaseManager")
# DB connection
async_engine = create_async_engine(settings.database_url, echo=False)
DBSession = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
# get Database
async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    async with DBSession() as session, session.begin():
        yield session
# Data Model Initialization
async def init_models() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables initialized.")