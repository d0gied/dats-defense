from libs.game.game import Game, EnemyBase, AttackCommand
from libs.models.cell import Coordinate

PRIORITIES = {"normal": 1, "fast": 2, "bomber": 4, "liner": 6, "juggernaut" : 5, "chaos_knight": 3}

async def start(game: Game) -> None:
    for zpot in game.world().zpots:
        if zpot.type == "base":
            game.move_base(Coordinate(x=zpot.x, y=zpot.y))
            break

async def loop(game: Game) -> None:
    unite_response = game.units()
    max_x, max_y = 0, 0
    all_connected = game.get_all_connected()
    for base in all_connected:
        max_x, max_y = max(max_x, base.x), max(max_y, base.y)
        accessible_targets = game.get_all_accessible_targets(base.id)
        most_priority = (-1, base.x, base.y)
        for target in accessible_targets:
            if isinstance(target, EnemyBase):
                most_priority = max((0, target.x, target.y), most_priority)
            else:
                most_priority = max((PRIORITIES[target.type], target.x, target.y), most_priority)
        game.attack(block_id=base.id, target=Coordinate(x=most_priority[1], y=most_priority[2]))

    matrix = [[0 for i in range(max_x + 1)] for j in range(max_y + 1)]
    for base in all_connected:
        matrix[base.x][base.y] = 1
    already_build = set()
    for base in all_connected:
        diff = [(1, 0), (0, 1)]
        for x_diff, y_diff in diff:
            if matrix[base.x + x_diff][base.y + y_diff] == 0 and (base.x + x_diff, base.y + y_diff) not in already_build:
                game.build(Coordinate(x=base.x + x_diff, y=base.y + y_diff))
