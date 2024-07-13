from libs.game.game import Game, EnemyBase, AttackCommand
from libs.models.cell import Coordinate

PRIORITIES = {"normal": 1, "fast": 2, "bomber": 4, "liner": 6, "juggernaut" : 5, "chaos_knight": 3}

async def start(game: Game) -> None:
    for zpot in game.world().zpots:
        if zpot.type == "base":
            game.move_base(Coordinate(x=zpot.x, y=zpot.y))
            break

async def loop(game: Game) -> None:
    ...
