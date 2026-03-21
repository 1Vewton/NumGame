from logging import getLogger
# Redis
import redis.asyncio as aioredis
# Project dependencies
from data_management.enums import FailReason

# logger
logger = getLogger("Game Process")


# Bot Game process class
class BotGameProcess:
    def __init__(self, client: aioredis.Redis, game_id: str):
        self.client = client
        self.game_id = game_id

    # Initialize a bot play game
    async def initializeBotPlay(self,
                                target: int = 10,
                                operation_cost: int = 10):
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
            "target": target,
            "operation_cost": operation_cost
        }
        # Store it to hash table
        await self.client.hset(self.game_id, mapping=score_info)

    '''
    Action point
    '''

    # Get bot action point
    async def getBotActionPoint(self):
        logger.info("Trying to get the action point for bot")
        bot_action_point = await self.client.hget(
            self.game_id,
            "bot_action_point"
        )
        return bot_action_point

    # Get player action point
    async def getPlayerActionPoint(self):
        logger.info("Trying to get the action point for player")
        player_action_point = await self.client.hget(
            self.game_id,
            "player_action_point"
        )
        return player_action_point

    # Get bot action point per turn
    async def getBotActionPointPT(self):
        logger.info("Trying to get the action point per turn for bot")
        bot_action_point_per_turn = await self.client.hget(
            self.game_id,
            "bot_action_point_per_turn"
        )
        return bot_action_point_per_turn

    # Get player action point per turn
    async def getPlayerActionPointPT(self):
        logger.info("Trying to get the action point per turn for player")
        player_action_point_per_turn = await self.client.hget(
            self.game_id,
            "player_action_point_per_turn"
        )
        return player_action_point_per_turn

    '''
    Score
    '''

    # Get player score
    async def getPlayerScore(self):
        logger.info("Trying to get the score for player")
        player_score = await self.client.hget(
            self.game_id,
            "player_score"
        )
        return player_score

    # Get bot score
    async def getBotScore(self):
        logger.info("Trying to get the score for bot")
        bot_score = await self.client.hget(
            self.game_id,
            "bot_score"
        )
        return bot_score

    '''
    Productivity
    '''

    # Get player productivity
    async def getPlayerProductivity(self):
        logger.info("Trying to get the productivity for player")
        player_productivity = await self.client.hget(
            self.game_id,
            "player_productivity"
        )
        return player_productivity

    # Get bot productivity
    async def getBotProductivity(self):
        logger.info("Trying to get the productivity for bot")
        bot_productivity = await self.client.hget(
            self.game_id,
            "bot_productivity"
        )
        return bot_productivity

    '''
    Destructivity
    '''

    # Get the destructivity of player
    async def getPlayerDestructivity(self):
        logger.info("Trying to get the destructivity for player")
        player_destructivity = await self.client.hget(
            self.game_id,
            "player_destructivity"
        )
        return player_destructivity

    # Get the destructivity of bot
    async def getBotDestructivity(self):
        logger.info("Trying to get the destructivity for bot")
        bot_destructivity = await self.client.hget(
            self.game_id,
            "bot_destructivity"
        )
        return bot_destructivity

    '''
    Game info fetching
    '''

    # Get Target Score
    async def getTarget(self):
        logger.info("Trying to get the target for the game")
        game_target = await self.client.hget(
            self.game_id,
            "target"
        )
        return game_target

    # Get action point cost
    async def getOperationCost(self):
        logger.info("Trying to get the cost for operations")
        operation_cost = await self.client.hget(
            self.game_id,
            "operation_cost"
        )
        return operation_cost

    # Game info fetching
    async def getGameData(self):
        logger.info("Trying to get the game data")
        game_data = await self.client.hgetall(self.game_id)
        return game_data

    '''
    Operations
    '''

    # Use action point
    async def usePlayerActionPoint(self):
        logger.info("Trying to use the action point for player")
        # AP-OC: Get final action point
        action_point = int(await self.getPlayerActionPoint())
        operation_cost = int(await self.getOperationCost())
        result = action_point - operation_cost
        # Process result
        if result < 0:
            return {
                "success": False,
                "reason": FailReason.NO_ENOUGH_ACTION_POINT
            }
        else:
            # Set the action point
            await self.client.hincrby(
                self.game_id,
                "player_action_point",
                -(operation_cost)
            )
            return {
                "success": True
            }

    # Bot action point using
    async def useBotActionPoint(self):
        logger.info("Trying to use the action point for player")
        # AP-OC: Get final action point
        action_point = int(await self.getBotActionPoint())
        operation_cost = int(await self.getOperationCost())
        result = action_point - operation_cost
        # Process result
        if result < 0:
            return {
                "success": False,
                "reason": FailReason.NO_ENOUGH_ACTION_POINT
            }
        else:
            # Set the action point
            await self.client.hincrby(
                self.game_id,
                "bot_action_point",
                -(operation_cost)
            )
            return {
                "success": True
            }

    # Increase the point
    async def playerProduce(self):
        logger.info("Player trying to produce")
        # Check whether action point is enough
        result = await self.usePlayerActionPoint()
        if result["success"]:
            player_productivity = int(await self.getPlayerProductivity())
            # The adding process
            await self.client.hincrby(
                self.game_id,
                "player_score",
                player_productivity
            )
            return {
                "success": True
            }
        else:
            # Return operation failed reason
            return {
                "success": False,
                "reason": result["reason"]
            }

    # Decrease the point of the opponent
    async def playerDestruct(self):
        logger.info("Player trying to destruct")
        # Use action point
        result = await self.usePlayerActionPoint()
        if result["success"]:
            player_destructivity = int(await self.getPlayerDestructivity())
            # The minus process
            await self.client.hincrby(
                self.game_id,
                "bot_score",
                -(player_destructivity)
            )
            return {
                "success": True
            }
        else:
            return {
                "success": False,
                "reason": result["reason"]
            }

    # Player Enhance Productivity
    async def playerEnhanceProductivity(self):
        logger.info("Player trying to enhance productivity")
        # Use action point
        result = await self.usePlayerActionPoint()
        if result["success"]:
            await self.client.hincrby(
                self.game_id,
                "player_productivity",
                1
            )
            return {
                "success": True
            }
        else:
            return {
                "success": False,
                "reason": result["reason"]
            }

    # Player Enhance Destructivity
    async def playerEnhanceDestructivity(self):
        logger.info("Player trying to enhance destructivity")
        # Use action point
        result = await self.usePlayerActionPoint()
        if result["success"]:
            await self.client.hincrby(
                self.game_id,
                "player_destructivity",
                1
            )
            return {
                "success": True
            }
        else:
            return {
                "success": False,
                "reason": result["reason"]
            }

    # Player enhance the action point per turn
    async def playerEnhanceActionPointPT(self):
        logger.info("Player trying to enhance action point production per turn")
        # Use action point
        result = await self.usePlayerActionPoint()
        if result["success"]:
            await self.client.hincrby(
                self.game_id,
                "player_action_point_per_turn",
                1
            )
            return {
                "success": True
            }
        else:
            return {
                "success": False,
                "reason": result["reason"]
            }

    # Bot produce
    async def botProduce(self):
        logger.info("Bot trying to produce scores")
        # Use Action point
        result = await self.useBotActionPoint()
        if result["success"]:
            bot_productivity = int(await self.getBotProductivity())
            await self.client.hincrby(
                self.game_id,
                "bot_score",
                bot_productivity
            )
            return {
                "success": True
            }
        else:
            return {
                "success": False,
                "reason": result["reason"]
            }

    # Bot Destruct
    async def botDestruct(self):
        logger.info("Bot trying to destruct score of opponent")
        # Use action point
        result = await self.useBotActionPoint()
        if result["success"]:
            bot_destructivity = int(await self.getBotDestructivity())
            await self.client.hincrby(
                self.game_id,
                "player_score",
                bot_destructivity
            )
            return {
                "success": True
            }
        else:
            return {
                "success": False,
                "reason": result["reason"]
            }

    # Delete game data
    async def deleteData(self):
        logger.info(f"Delete Data of key {self.game_id}")
        await self.client.delete(self.game_id)
