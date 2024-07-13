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
    min_x, min_y, max_x, max_y = 1e9, 1e9, 0, 0
    for base in game.get_all_connected():
        min_x, min_y, max_x, max_y = min(min_x, base.x), min(min_y, base.y), max(max_x, base.x), max(max_y, base.y)
        accessible_targets = game.get_all_accessible_targets(base)
        most_priority = (-1, base.x, base.y)
        for target in accessible_targets:
            if isinstance(target, EnemyBase):
                most_priority = max((0, target.x, target.y), most_priority)
            else:
                most_priority = max((PRIORITIES[target.type], target.x, target.y), most_priority)
        game.attack(block_id=base.id, target=Coordinate(x=most_priority[1], y=most_priority[2]))
