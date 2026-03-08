import asyncio
# Fastapi dependencies
from fastapi import APIRouter
from fastapi.responses import JSONResponse
# logging
import logging

from starlette import status

# Project dependencies
from numgame.utils import generate_random_name

# Logger
logger = logging.getLogger("Utility Server")
# API Router
utils_router = APIRouter(prefix="/utils")


# APIs
# Generate user name
@utils_router.get("/generateUserName", tags=["generateUserName"])
async def generateUserName():
    logger.info(f"Generating username")
    try:
        loop = asyncio.get_event_loop()
        # Generate name
        name = await loop.run_in_executor(None,
                                          generate_random_name)
        content = {
            "success": True,
            "username": name
        }
        return JSONResponse(status_code=200, content=content)
    except Exception as e:
        # Error handling
        content = {
            "success": False,
            "message": str(e)
        }
        return JSONResponse(status_code=500, content=content)
