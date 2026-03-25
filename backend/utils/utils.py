import uuid
import logging
from pathlib import Path
# slowapi
from slowapi import Limiter
from slowapi.util import get_remote_address
# Project dependencies
from utils.config import settings
from data_management.enums import FailReason
# Important tools
import pandas as pd
import numpy as np
import random

# Limiter
limiter = Limiter(key_func=get_remote_address)
# Logger
logger = logging.getLogger("Utils")
# File path
BASE_DIR = Path(__file__).resolve().parent.parent
NAMES_FILE_PATH = BASE_DIR / f"assets/{settings.names_csv}"


# Generate uuid
def generate_uuid():
    return str(uuid.uuid4())


# Generate random name
def generate_random_name():
    # Read from file
    names_table = pd.read_csv(NAMES_FILE_PATH)
    names = names_table["name"]
    names_list = names.tolist()
    name = np.random.choice(names_list, 2)
    # Capitalize
    name[0] = name[0][0].upper() + name[0][1:]
    name[1] = name[1][0].upper() + name[1][1:]
    return name[0] + " " + name[1]


# Decide first move in bot play
def decide_is_user_first():
    result = random.randint(0, 1)
    if result == 0:
        return True
    else:
        return False


# Show fail reason to user
def fail_reason2user(fail_reason: FailReason):
    if fail_reason == FailReason.NO_ENOUGH_ACTION_POINT:
        return "No enough action point to execute the process"


if __name__ == "__main__":
    print(decide_is_user_first())
