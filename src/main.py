from libs.alerts import AlertManager
from argparse import ArgumentParser
from libs.game.game import Game, CommandPayload
from libs.models.core import AttackCommand, Coordinate, BuildCommand
from config import Config
from loguru import logger
import json

# set loguru logging to file
logger.add("logs.log", rotation="1 day", retention="7 days", level="INFO")

parser = ArgumentParser(description="Big Data Small Memory")

parser.add_argument(
    "--mode",
    action="store",
    help="Set the mode of the bot: 'main', 'test', 'local'"
)
parser.add_argument(
    "--participate",
    action="store_true",
    help="Send a test participate request to the game server",
)
parser.add_argument(
    "--units",
    action="store_true",
    help="Send a test units request to the game server",
)
parser.add_argument(
    "--world",
    action="store_true",
    help="Send a test world request to the game server",
)
parser.add_argument(
    "--rounds",
    action="store_true",
    help="Send a test rounds request to the game server",
)
parser.add_argument(
    "--bot",
    action="store_true",
    help="Start the bot",
)

if __name__ == "__main__":
    # BASE_URL = "http://127.0.0.1:8000/"
    args = parser.parse_args()
    BASE_URL = Config.Server.API_BASE_URL
    if args.mode == "test":
        BASE_URL = Config.Server.API_TEST_BASE_URL
    if args.mode == "local":
        BASE_URL = "http://127.0.0.1:8000/"

    game = Game(api_base_url=BASE_URL)
    if args.participate:
        resp = game._participate()
        print(json.dumps(resp.model_dump(), indent=4))
    if args.units:
        units = game._units()
        print(json.dumps(units.model_dump(), indent=4))
    if args.world:
        world = game._world()
        print(json.dumps(world.model_dump(), indent=4))
    if args.rounds:
        rounds = game._rounds()
        print(json.dumps(rounds.model_dump(), indent=4))
    if args.bot:
        from bot import start as bot_start, loop as bot_loop
        game.start(bot_start)
        game.loop(bot_loop)
        game.run()
