import logging
# FastAPI
from fastapi import APIRouter

# logger
logger = logging.getLogger("Game Server")
# Router
router = APIRouter(prefix="/game")
