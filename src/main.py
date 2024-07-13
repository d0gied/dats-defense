from libs.alerts import AlertManager
from argparse import ArgumentParser
from libs.game.game import Game, CommandPayload
from libs.models.core import AttackCommand, Coordinate, BuildCommand
from config import Config
from loguru import logger

# set loguru logging to file
logger.add("logs.log", rotation="1 day", retention="7 days", level="INFO")

parser = ArgumentParser(description="Big Data Small Memory")

parser.add_argument(
    "--command-test", action="store_true", help="Send a test command to the game server"
)
parser.add_argument(
    "--participate-test",
    action="store_true",
    help="Send a test participate request to the game server",
)
parser.add_argument(
    "--units-test",
    action="store_true",
    help="Send a test units request to the game server",
)
parser.add_argument(
    "--world-test",
    action="store_true",
    help="Send a test world request to the game server",
)
parser.add_argument(
    "--rounds-test",
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
    BASE_URL = Config.Server.API_TEST_BASE_URL
    args = parser.parse_args()
    if args.command_test:
        game = Game(api_base_url=BASE_URL)
        game._command(
            CommandPayload(
                attack=[
                    AttackCommand(
                        blockId="f47ac10b-58cc-0372-8562-0e02b2c3d479",
                        target=Coordinate(x=1, y=1),
                    )
                ],
                build=[],
                moveBase=Coordinate(x=1, y=1),
            )
        )
    if args.participate_test:
        game = Game(api_base_url=BASE_URL)
        game._participate()
    if args.units_test:
        game = Game(api_base_url=BASE_URL)
        game._units()
    if args.world_test:
        game = Game(api_base_url=BASE_URL)
        game._world()
    if args.rounds_test:
        game = Game(api_base_url=BASE_URL)
        game._rounds()
    if args.bot:
        game = Game(api_base_url=BASE_URL)
        from bot import start as bot_start, loop as bot_loop
        game.start(bot_start)
        game.loop(bot_loop)
        game.run()
