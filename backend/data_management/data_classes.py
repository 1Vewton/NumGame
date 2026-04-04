from data_management.enums import FailReason


# Data model for updating the status of Bot state machine
class BotStateMachineStatus:
    point: int
    opponent_point: int
    productivity: int
    destructivity: int
    target: int


# Game operation result
class OperationResult:
    success: bool
    end_turn: bool


# Player Operation Result
class PlayerOperationResult:
    success: bool
    end_turn: bool
    reason: FailReason
