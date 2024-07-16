from libs.alerts import AlertManager
from argparse import ArgumentParser
from libs.game.game import Game, CommandPayload
from libs.game.api import GameApi
from libs.models.core import (
    AttackCommand,
    Coordinate,
    BuildCommand,
    ErrorResponse,
    ParticipateResponse,
    UnitsRepsonse,
    WorldResponse,
)
from config import Config
from loguru import logger
import json
from fastapi import FastAPI, background
import asyncio
import sys

logger.remove()

# set loguru logging to file
logger.add("debug.log", rotation="1 day", retention="7 days", level="DEBUG")
logger.add("error.log", rotation="1 day", retention="7 days", level="ERROR")
logger.add("info.log", rotation="1 day", retention="7 days", level="INFO")

# set loguru logging to console
logger.add(sys.stderr, level="INFO")

parser = ArgumentParser(description="Big Data Small Memory")

parser.add_argument(
    "--mode", action="store", help="Set the mode of the bot: 'main', 'test', 'local'"
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
parser.add_argument(
    "--daemon",
    action="store_true",
    help="Start the daemon",
)
parser.add_argument(
    "--api",
    action="store_true",
    help="Start the api",
)

async def main(loop: asyncio.AbstractEventLoop):
    # BASE_URL = "http://127.0.0.1:8000/"
    args = parser.parse_args()
    BASE_URL = Config.Server.API_BASE_URL
    if args.mode == "test":
        BASE_URL = Config.Server.API_TEST_BASE_URL
    if args.mode == "local":
        BASE_URL = "http://127.0.0.1:8001/"

    async with GameApi(api_base_url=BASE_URL) as api:
        game = Game(api=api)
        if args.participate:
            resp = await api.participate()
            print(json.dumps(resp.model_dump(), indent=4))
        if args.units:
            units = await api.units()
            print(json.dumps(units.model_dump(), indent=4))
        if args.world:
            world = await api.world()
            print(json.dumps(world.model_dump(), indent=4))
        if args.rounds:
            rounds = await api.rounds()
            print(json.dumps(rounds.model_dump(), indent=4))

        run_forever = False

        if args.bot:
            from bot import (
                start as bot_start,
                loop as bot_loop,
                dead as bot_dead,
                waiting as bot_waiting,
            )


            game.start(bot_start)
            game.loop(bot_loop)
            game.dead(bot_dead)
            game.waiting(bot_waiting)
            run_forever = True


        if args.daemon:
            from daemon import start as bot_start, loop as bot_loop, waiting as bot_waiting

            game.start(bot_start)
            game.loop(bot_loop)
            game.waiting(bot_waiting)
            run_forever = True


        if args.api:
            from uvicorn import Config as UvicornConfig
            from uvicorn.server import Server
            from fastapi.middleware.cors import CORSMiddleware

            logger.info("Starting API")
            app = FastAPI()
            app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

            @app.get("/play/zombidef/units")
            async def app_units() -> UnitsRepsonse | ErrorResponse:
                return game._units_data  # type: ignore

            @app.get("/play/zombidef/world")
            async def app_world() -> WorldResponse | ErrorResponse:
                return game._world_data  # type: ignore

            @app.post("/play/zombidef/participate")
            async def app_participate() -> ParticipateResponse | ErrorResponse:
                return game._participate_data  # type: ignore

            config = UvicornConfig(app=app, log_level="critical")
            server = Server(config)
            loop.create_task(server.serve())
            run_forever = True
        if run_forever:
            await game._run()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    if asyncio.run(main(loop)):
        loop.run_forever()
