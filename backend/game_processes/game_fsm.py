from logging import getLogger
# FastAPI
from fastapi import WebSocket

logger = getLogger("game_fsm")


class GameStateMachine:
    def __init__(self, client: WebSocket):
        self.client = client
