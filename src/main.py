from libs.alerts import AlertManager
from argparse import ArgumentParser
from libs.game.game import Game, CommandPayload
from libs.game.api import ServerApi
from libs.models.core import (
    AttackCommand,
    Coordinate,
    BuildCommand,
    ErrorResponse,
    ParticipateResponse,
    UnitsRepsonse,
    WorldResponse,
)
from libs.metrics.client import MetricsClient
from libs.game.dispatcher import GameDispatcher

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
parser.add_argument(
    "--test-metrics",
    action="store_true",
    help="Test the metrics",
)
parser.add_argument(
    "--round",
    action="store_true",
    help="Get the current round",
)
parser.add_argument(
    "--next-round",
    action="store_true",
    help="Get the next round",
)
parser.add_argument(
    "--alert", action="store", help="Send an alert")



async def main(loop: asyncio.AbstractEventLoop):
    # BASE_URL = "http://127.0.0.1:8000/"
    args = parser.parse_args()
    BASE_URL = Config.Server.API_BASE_URL
    if args.mode == "test":
        BASE_URL = Config.Server.API_TEST_BASE_URL
    if args.mode == "local":
        BASE_URL = "http://127.0.0.1:8001/"

    async with ServerApi(api_base_url=BASE_URL) as api:
        dp = GameDispatcher(api=api)

        if args.alert:
            async with AlertManager() as alert:
                await alert.send_alert(str(args.alert))
        if args.test_metrics:
            metrics = MetricsClient(
                host="localhost",
                port=8086
            )
            await metrics.push_rate(
                measurement="test",
                tags={"test": "test"},
                fields={"test": "1"},
            )

        if args.participate:
            resp = await api.participate()
            print(resp.model_dump_json(indent=4))
        if args.units:
            units = await api.units()
            print(units.model_dump_json(indent=4))
        if args.world:
            world = await api.world()
            print(world.model_dump_json(indent=4))
        if args.rounds:
            rounds = await api.rounds()
            print(rounds.model_dump_json(indent=4))

        if args.round:
            round = await dp.current_round()
            if round:
                if round.status == "not started":
                    print(f"NEXT | NOT STARTED | Starts in {round.starts_in()}")
                elif round.status == "active":
                    print(f"CURRENT | RUNNING | Ends in {round.ends_in()}")
                    next = await dp.next_round()
                    if next:
                        print(f"NEXT | NOT STARTED | Starts in {next.starts_in()}")



        if args.next_round:
            round = await dp.next_round()
            if round:
                print(json.dumps(round.model_dump(), indent=4))

        run_forever = False

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



if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    if asyncio.run(main(loop)):
        loop.run_forever()
