import uuid
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging
from pathlib import Path
from numgame.config import settings
import pandas as pd
import numpy as np

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
    # Read from fi;e
    names_table = pd.read_csv(NAMES_FILE_PATH)
    names = names_table["name"]
    names_list = names.tolist()
    name = np.random.choice(names_list, 2)
    # Capitalize
    name[0] = name[0][0].upper() + name[0][1:]
    name[1] = name[1][0].upper() + name[1][1:]
    return name[0] + " " + name[1]


if __name__ == "__main__":
    print(generate_random_name())
