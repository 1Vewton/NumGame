from logging import getLogger
# Redis
import redis.asyncio as aioredis

# logger
logger = getLogger("Game Process")


# Initialize a bot play game
async def initializeBotPlay(client: aioredis.Redis, game_id: str):
    logger.info("New Bot Game set")
    # Data info
    score_info = {
        "player_score": 0,
        "player_productivity": 1,
        "player_destructivity": 1,
        "player_action_point": 0,
        "player_action_point_per_turn": 10,
        "bot_score": 0,
        "bot_productivity": 1,
        "bot_destructivity": 1,
        "bot_action_point": 0,
        "bot_action_point_per_turn": 10,
        "turn": 0
    }
    # Store it to hash table
    await client.hset(game_id, mapping=score_info)


# Delete game data
async def deleteData(client: aioredis.Redis, game_id: str):
    logger.info(f"Delete Data of key {game_id}")
    await client.delete(game_id)
