import uuid
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging

# Limiter
limiter = Limiter(key_func=get_remote_address)
# Logger
logger = logging.getLogger("Utils")
# Generate uuid
def generate_uuid():
    return str(uuid.uuid4())