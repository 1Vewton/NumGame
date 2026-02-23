from contextlib import asynccontextmanager
from fastapi import FastAPI
from collections.abc import AsyncGenerator
from typing import Any
from numgame.data_management import init_models

# run before execution
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:
    await init_models()
    yield

# APP
app = FastAPI(lifespan=lifespan)