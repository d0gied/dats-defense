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

gold_history = []

async def start(game: Game) -> None:
    global gold_history
    gold_history = []

async def find_target(game: Game, base: Base, hps: dict[tuple[int, int], int]) -> Coordinate | None:
    possible_targets: dict[tuple[int, int], int] = {}
    for unit in game.get_all_accessible_targets(base.id):
        if isinstance(unit, EnemyBase):
            priority = PRIORITIES["enemy"] + abs(unit.x - base.x) + abs(unit.y - base.y) + hps.get((unit.x, unit.y), 0)
            priority = priority if hps.get((unit.x, unit.y), 0) > 0 else 0
            possible_targets[(unit.x, unit.y)] = (
                possible_targets.get((unit.x, unit.y), 0) + priority
            )
        else:
            if unit.type not in PRIORITIES:
                logger.warning(
                    f"Unknown unit type: {unit.type}, setting priority to 10"
                )
            priority = PRIORITIES.get(unit.type, 10) + abs(unit.x - base.x) + abs(unit.y - base.y) + hps.get((unit.x, unit.y), 0)
            priority = priority if hps.get((unit.x, unit.y), 0) > 0 else 0
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
    global gold_history
    current_base = game.get_all_connected()
    full_base = game.units().base
    head = game.get_head()
    gold_history.append(game.get_gold())

    logger.info(f"Current gold: {game.get_gold()}")
    hps: dict[tuple[int, int], int] = {}

    for unit in game.units().zombies + game.units().enemy_blocks:
        hps[(unit.x, unit.y)] = unit.health

    targets: dict[tuple[int, int], int] = {}
    for base in current_base:
        target = await find_target(game, base, hps)
        if target is not None:
            game.attack(block_id=base.id, target=target)
            logger.info(f"Attacking {target} with base {base.id}")
            targets[(target.x, target.y)] = targets.get((target.x, target.y), 0) + 1
            hps[(target.x, target.y)] -= base.attack
            hps[(target.x, target.y)] = max(0, hps[(target.x, target.y)])

    logger.info(f"Targets attacked: {len(targets)}")
    logger.info(f"Max overlap: {max(targets.values()) if targets else 0}")
    logger.info(f"Current gold: {game.get_gold()}")


    center_of_mass = [0, 0]
    for base in full_base:
        center_of_mass[0] += base.x
        center_of_mass[1] += base.y

    center_of_mass[0] = round(center_of_mass[0] / len(current_base))
    center_of_mass[1] = round(center_of_mass[1] / len(current_base))

    closest = head
    min_distance = 1000000
    for base in full_base:
        distance = abs(base.x - center_of_mass[0]) + abs(base.y - center_of_mass[1])
        if distance < min_distance:
            min_distance = distance
            closest = base
    game.move_base(Coordinate(x=closest.x, y=closest.y))

    min_x = min([base.x for base in full_base]) - 2
    min_y = min([base.y for base in full_base]) - 2
    max_x = max([base.x for base in full_base]) + 2
    max_y = max([base.y for base in full_base]) + 2

    matrix = [[0 for _ in range(max_x - min_x + 1)] for _ in range(max_y - min_y + 1)]
    for base in full_base:
        matrix[base.y - min_y - 1][base.x - min_x - 1] += 1
        matrix[base.y - min_y + 1][base.x - min_x - 1] += 1
        matrix[base.y - min_y - 1][base.x - min_x + 1] += 1
        matrix[base.y - min_y + 1][base.x - min_x + 1] += 1

    cells_to_build: list[tuple[int, Coordinate]] = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != 0 and game.can_build(Coordinate(x=j + min_x, y=i + min_y), no_warn=True):
                cells_to_build.append((matrix[i][j], (Coordinate(x=j + min_x, y=i + min_y))))

    cells_to_build.sort(key=lambda x: x[0], reverse=True)
    gold = game.get_gold(extra=False)
    should_left = round((sum(gold_history[:5]) / len(gold_history[:5])) * 0.3)
    logger.info(f"Should left: {should_left}")
    free_gold = max(gold - should_left, 0)
    logger.info(f"Free gold: {free_gold}")
    top_cells = cells_to_build[:free_gold]
    built = 0
    current_to_build = 0
    while built < free_gold and current_to_build < len(top_cells):
        could = game.build(Coordinate(x=top_cells[current_to_build][1].x, y=top_cells[current_to_build][1].y))
        current_to_build += 1
        if could:
            built += 1
            logger.info(f"Building base at {top_cells[current_to_build - 1][1]}")
    logger.info(f"Built {built} bases")



async def dead(game: Game) -> None:
    logger.info(f"Game ended with {game.units().player.gold} points")


async def waiting(game: Game) -> None:
    pass
