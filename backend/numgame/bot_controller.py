from enums import Operations, StateMachine
from numgame.config import settings
import numpy as np

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
        self.name = settings.simple_bot_name
        # Data
        self.point = 0
        self.opponent_point = 0
        self.productivity = 0
        self.destructivity = 0
        self.target = 0
    # Update state
    def update_state(self, point, opponent_point, productivity, destructivity, target):
        # Data update
        self.point = point
        self.opponent_point = opponent_point
        self.productivity = productivity
        self.destructivity = destructivity
        self.target = target
        # Update state of the state machine
        if(self.point <= 2
                and self.opponent_point <= 2
                and self.destructivity <= 2):
            self.current_state = StateMachine.START_STAGE
        elif(self.opponent_point - self.point > self.target/4):
            self.current_state = StateMachine.DISADVANTAGE
        elif(self.point - self.opponent_point > self.target/4):
            self.current_state = StateMachine.ADVANTAGE
        elif(self.point>=self.target):
            self.current_state = StateMachine.RUSH_STAGE
        else:
            self.current_state = StateMachine.BALANCE
    # Bot choice
    def choose_action(self):
        weight = self.operation_weights[self.current_state]
        choice = np.random.choice(self.operations, p=weight)
        return choice

# Test
if __name__ == "__main__":
    bot = BotStateMachine()
    bot.update_state(10,0,0,0,10)
    print(bot.choose_action())