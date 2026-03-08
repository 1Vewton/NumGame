import redis.asyncio as aioredis
import logging
from numgame.config import settings
from fastapi import Request

logger = logging.getLogger("Redis Manager")
# Create an async redis client
async def create_redis_client() -> aioredis.Redis:
    # Redis client config
    client = aioredis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        password=settings.redis_password
    )
    # Check Redis connection state
    try:
        await client.ping()
        logger.info("Redis connected.")
    except Exception as e:
        logger.error(f"Redis ping failed: {e}")
        raise e
    return client

# Get redis
def get_redis(request:Request) -> aioredis.Redis:
    return request.app.state.redis_client