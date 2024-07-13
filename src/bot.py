from libs.game.game import Game
from libs.models.cell import Coordinate

async def start(game: Game) -> None:
    for zpot in game.world().zpots:
        if zpot.type == "base":
            game.move_base(Coordinate(x=zpot.x, y=zpot.y))
            break

async def loop(game: Game) -> None:
    base = game.units().base
