from enums import *
from utils import generate_random_name

# Bot Logic
class BotStateMachine:
    def __init__(self):
        # Store the possible operations
        self.operations = [Operations.PRODUCE,
                           Operations.DESTRUCT,
                           Operations.ENHANCE_PRODUCTIVITY,
                           Operations.ENHANCE_DESTRUCTIBILITY,
                           Operations.ENHANCE_ACTION_POINT]
        # Weight of operation for each state
        self.operation_weights = {
            StateMachine.START_STAGE:[
                0.1,
                0.0,
                0.45,
                0.40,
                0.05
            ],
            StateMachine.BALANCE:[
                0.25,
                0.25,
                0.25,
                0.2,
                0.05
            ],
            StateMachine.ADVANTAGE:[
                0.5,
                0.05,
                0.2,
                0.2,
                0.05
            ],
            StateMachine.DISADVANTAGE:[
                0.1,
                0.4,
                0.2,
                0.3,
                0.0
            ],
            StateMachine.RUSH_STAGE:[
                0.4,
                0.4,
                0.075,
                0.075,
                0.05
            ]
        }
        # The current state
        self.current_state = None
        # Bot Name
        self.name = "<bot> " + generate_random_name()