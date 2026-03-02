import uuid
from slowapi import Limiter
from slowapi.util import get_remote_address

# Limiter
limiter = Limiter(key_func=get_remote_address)
# Generate uuid
def generate_uuid():
    return str(uuid.uuid4())