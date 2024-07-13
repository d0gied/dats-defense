from libs.game.game import Game, EnemyBase, AttackCommand
from libs.models.block import Base
from libs.models.cell import Coordinate
from loguru import logger

from libs.models.zombie import Zombie

PRIORITIES = {
    "normal": 1,
    "fast": 2,
    "bomber": 4,
    "liner": 6,
    "juggernaut": 5,
    "chaos_knight": 3,
    "enemy": 1,
}


async def start(game: Game) -> None: ...


async def find_target(game: Game, base: Base) -> Coordinate | None:
    possible_targets: dict[tuple[int, int], int] = {}
    for unit in game.get_all_accessible_targets(base.id):
        if isinstance(unit, EnemyBase):
            priority = PRIORITIES["enemy"]
            possible_targets[(unit.x, unit.y)] = (
                possible_targets.get((unit.x, unit.y), 0) + priority
            )
        else:
            if unit.type not in PRIORITIES:
                logger.warning(
                    f"Unknown unit type: {unit.type}, setting priority to 10"
                )
            priority = PRIORITIES.get(unit.type, 10)
            possible_targets[(unit.x, unit.y)] = (
                possible_targets.get((unit.x, unit.y), 0) + priority
            )
    if not possible_targets:
        return None
    best = max(possible_targets.items(), key=lambda x: x[1])
    target = Coordinate(x=best[0][0], y=best[0][1])
    priority = best[1]

    logger.info(f"Base {base.id} is attacking {target} with priority {priority}")
    return target


async def loop(game: Game) -> None:
    current_base = game.get_all_connected()
    full_base = game.units().base
    head = game.get_head()

    logger.info(f"Current gold: {game.get_gold()}")
    for base in current_base:
        target = await find_target(game, base)
        if target is not None:
            game.attack(block_id=base.id, target=target)
            logger.info(f"Attacking {target} with base {base.id}")
            for unit in game.get_units_at(target):
                if isinstance(unit, (EnemyBase, Zombie)):
                    game.attack(block_id=base.id, target=target)
                    logger.info(f"Attacking {unit} with damage {base.attack}")

    logger.info(f"Current gold: {game.get_gold()}")

    most_alive: Base = head
    for base in full_base:
        if base.health > most_alive.health:
            most_alive = base
    if most_alive.id != head.id:
        new_head_pos = Coordinate(x=most_alive.x, y=most_alive.y)
        game.move_base(new_head_pos)
        logger.info(f"Moving base to {new_head_pos}")

async def dead(game: Game) -> None:
    logger.info(f"Game ended with {game.units().player.gold} points")


async def waiting(game: Game) -> None:
    pass
