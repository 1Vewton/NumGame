# Data model for updating the status of Bot state machine
class BotStateMachineStatus:
    point: int
    opponent_point: int
    productivity: int
    destructivity: int
    target: int
