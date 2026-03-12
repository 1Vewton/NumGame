from logging import getLogger
# Redis Management
import redis.asyncio as aioredis
# Project dependencies
from numgame.utils import generate_uuid

# logger
logger = getLogger("Token Manager")


# Generate login token
async def generate_login_token(
        user_id: str,
        client: aioredis.Redis) -> str:
    logger.info("Generate Login Token")
    token = f"user_token:{generate_uuid()}"
    # Data
    token_data = {
        "user_id": user_id
    }
    # Store token into redis
    await client.hset(token, mapping=token_data)
    await client.expire(token, 86400)
    return token


# Get user id from the token
async def search_user_token(
        token: str,
        client: aioredis.Redis):
    logger.info("Searching User Token")
    exists = await client.exists(token)
    if exists:
        logger.info("Found User Token")
        # Get user id
        user_id = await client.hget(token, "user_id")
        logger.info(f"ID: {user_id}")
        return {
            "success": True,
            "user_id": user_id
        }
    else:
        # User token not found in redis
        logger.info("User Token Not Found or Expired")
        return {
            "success": False,
            "message": "User Token Not Found or Expired"
        }
