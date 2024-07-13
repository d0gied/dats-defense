from libs.game.game import Game, EnemyBase, AttackCommand
from libs.models.cell import Coordinate
from loguru import logger

PRIORITIES = {"normal": 1, "fast": 2, "bomber": 4, "liner": 6, "juggernaut" : 5, "chaos_knight": 3}

logger.add("daemon.log", rotation="1 day", retention="7 days", level="INFO")

async def loop(game: Game) -> None:
    units = game.units()
    world = game.world()

    logger.info(f"Units: {units.model_dump()}")
    logger.info(f"World: {world.model_dump()}")
