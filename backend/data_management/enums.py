from enum import Enum


# Game operations
class Operations(Enum):
    PRODUCE = 1
    DESTRUCT = 2
    ENHANCE_PRODUCTIVITY = 3
    ENHANCE_DESTRUCTIBILITY = 4
    ENHANCE_ACTION_POINT = 5
    SKIP = 6


# Robot Status
class StateMachine(Enum):
    START_STAGE = 1
    ADVANTAGE = 3
    DISADVANTAGE = 4
    BALANCE = 5
    RUSH_STAGE = 6


# Operation Fail Reason
class FailReason(Enum):
    NO_ENOUGH_ACTION_POINT = 1
    NO_SUCH_OPERATION = 2
    NOT_YOUR_TURN = 3


# Response Type
class WSResponseType(Enum):
    HEARTBEAT = 1
    PLAYER_OPERATION = 2
    OPERATION_EXECUTION_RESULT = 3
    MOVE_DIVISION = 4
    DATA_UPDATE = 5
    BOT_TURN_START = 6
    PLAYER_TURN_START = 7
    TURN_FINISH = 8
    BOT_TURN_FINISH = 9
    PLAYER_WIN = 10
    BOT_WIN = 11


# Turn finish reason
class TurnFinishReason(Enum):
    FRONTEND_OPERATION = 1
    TIMEOUT = 2


# Bot game player enum
class BotGamePlayer(Enum):
    PLAYER = 1
    BOT = 2


# Game state
class GameState(Enum):
    INIT = 0
    PLAYER_TURN = 1
    BOT_TURN = 2
    SETTLEMENT = 3
    FINISH = 4
