from libs.game.game import Game, EnemyBase, AttackCommand
from libs.models.block import Base
from libs.models.cell import Coordinate
from loguru import logger

PRIORITIES = {"normal": 1, "fast": 2, "bomber": 4, "liner": 6, "juggernaut" : 5, "chaos_knight": 3, "enemy": 1}

async def start(game: Game) -> None:
    ...

async def find_target(game: Game, base: Base) -> Coordinate | None:
    possible_targets: dict[tuple[int, int], int] = {}
    for unit in game.get_all_accessible_targets(base.id):
        if isinstance(unit, EnemyBase):
            priority = PRIORITIES["enemy"]
            possible_targets[(unit.x, unit.y)] = possible_targets.get((unit.x, unit.y), 0) + priority
        else:
            if unit.type not in PRIORITIES:
                logger.warning(f"Unknown unit type: {unit.type}, setting priority to 10")
            priority = PRIORITIES.get(unit.type, 10)
            possible_targets[(unit.x, unit.y)] = possible_targets.get((unit.x, unit.y), 0) + priority
    if not possible_targets:
        return None
    best = max(possible_targets.items(), key=lambda x: x[1])
    target = Coordinate(x=best[0][0], y=best[0][1])
    priority = best[1]

    logger.debug(f"Base {base.id} is attacking {target} with priority {priority}")
    return target

async def loop(game: Game) -> None:
    current_base = game.get_all_connected()
    logger.debug(f"Current gold: {game.units().player.gold}")
    for base in current_base:
        target = await find_target(game, base)
        if target is not None:
            game.attack(block_id=base.id, target=target)



async def dead(game: Game) -> None:
    logger.info(f"Game ended with {game.units().player.gold} points")

async def waiting(game: Game) -> None:
    pass
