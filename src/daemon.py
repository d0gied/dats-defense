from libs.game.game import Game, EnemyBase, AttackCommand
from libs.models.cell import Coordinate
from loguru import logger
import json

PRIORITIES = {"normal": 1, "fast": 2, "bomber": 4, "liner": 6, "juggernaut" : 5, "chaos_knight": 3}

logger.add("daemon.log", rotation="1 day", retention="7 days", level="INFO")

filename: str = "rounds.json"

async def waiting(game: Game) -> None:
    ...

async def start(game: Game) -> None:
    global filename
    filename = f"{game.units().realm_name}.json"
    data = {
        "world": game.world().model_dump(),
        "steps": []
    }
    with open(filename, "w") as f:
        f.write(json.dumps(data, indent=4))

async def loop(game: Game) -> None:
    units = game.units()

    logger.debug(f"Units: {json.dumps(units.model_dump(), indent=4)}")

    prev_data = json.loads(open(filename, "r").read())
    prev_data["steps"].append(units.model_dump())

    with open(filename, "w") as f:
        f.write(json.dumps(prev_data, indent=4))
