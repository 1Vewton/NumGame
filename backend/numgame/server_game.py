import logging
# FastAPI
from fastapi import APIRouter

# logger
logger = logging.getLogger("game server")
# Router
router = APIRouter(prefix="/game")
