from enum import Enum


# Game operations
class Operations(Enum):
    PRODUCE = 1
    DESTRUCT = 2
    ENHANCE_PRODUCTIVITY = 3
    ENHANCE_DESTRUCTIBILITY = 4
    ENHANCE_ACTION_POINT = 5


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


# Bot game player enum
class BotGamePlayer(Enum):
    PLAYER = 1
    BOT = 2
