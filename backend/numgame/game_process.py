from logging import getLogger
# Redis
import redis.asyncio as aioredis

# logger
logger = getLogger("Game Process")


# Game process class
class GameProcess:
    def __init__(self, client: aioredis.Redis, game_id: str):
        self.client = client
        self.game_id = game_id

    # Initialize a bot play game
    async def initializeBotPlay(self,
                                target: int = 10):
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
            "turn": 0,
            "target": target
        }
        # Store it to hash table
        await self.client.hset(self.game_id, mapping=score_info)

    # Get bot action point
    async def getBotActionPoint(self):
        logger.info("Trying to get the action point for bot")
        bot_action_point = await self.client.hget(
            self.game_id,
            "bot_action_point"
        )
        return bot_action_point

    # Get player action point
    async def playerActionPoint(self):
        logger.info("Trying to get the action point for player")
        player_action_point = await self.client.hget(
            self.game_id,
            "player_action_point"
        )
        return player_action_point

    # Get player score
    async def playerScore(self):
        logger.info("Trying to get the score for player")
        player_score = await self.client.hget(
            self.game_id,
            "player_score"
        )
        return player_score

    # Get bot score
    async def botScore(self):
        logger.info("Trying to get the score for bot")
        bot_score = await self.client.hget(
            self.game_id,
            "bot_score"
        )
        return bot_score

    # Get bot action point per turn
    async def botActionPointPT(self):
        logger.info("Trying to get the action point per turn for bot")
        bot_action_point_per_turn = await self.client.hget(
            self.game_id,
            "bot_action_point_per_turn"
        )
        return bot_action_point_per_turn

    # Delete game data
    async def deleteData(self):
        logger.info(f"Delete Data of key {self.game_id}")
        await self.client.delete(self.game_id)
