from logging import getLogger
import uvicorn
from collections.abc import AsyncGenerator
from typing import Any
from contextlib import asynccontextmanager
# FastAPI dependencies
from fastapi import FastAPI
# Project Dependencies
from numgame.config import settings
from numgame.data_management import init_models
import numgame.logger_config as logger_config
from numgame.redis_manager import create_redis_client
from numgame.server_user_management import user_router
from numgame.server_utils import utils_router
from numgame.utils import limiter
# Slowapi Dependencies
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

# run before execution
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:
    # Database Config
    await init_models()
    # Redis Config
    redis_client = await create_redis_client()
    app.state.redis_client = redis_client
    yield
    await redis_client.aclose()
    logger.info(f"Redis connection closed")

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
    },
    {
        "name": "userInfo",
        "description": "The api for the front-end to get user info"
    },
    {
        "name": "generateUserName",
        "description": "The api for generating random user name"
    }
]
# APP
app = FastAPI(
    lifespan=lifespan,
    title="NumGame Server",
    description="Backend Server for NumGame",
    openapi_tags=tags,
    root_path="/api",
)
# Limiter setting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# Add router
app.include_router(user_router)
app.include_router(utils_router)

# run server
def run():
    logger_config.setup_logging()
    logger.info("Starting server")
    uvicorn.run(app, host="localhost", port=settings.server_port)

if __name__ == "__main__":
    run()