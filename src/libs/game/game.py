from config import Config
from ..models.core import (
    CommandPayload,
    CommandResponse,
    ErrorResponse,
    ParticipateResponse,
    UnitsRepsonse,
    WorldResponse,
    RoundsResponse,
    AttackCommand,
    BuildCommand,
    Coordinate,
)
from typing import Any, Callable, Awaitable, Coroutine
from requests import post, get, put, Session
import urllib3
import asyncio
from loguru import logger

TAsyncGameFunc = Callable[["Game"], Coroutine[Any, Any, None]]


class Game:
    def __init__(
        self,
        *,
        api_base_url: str = Config.Server.API_BASE_URL,
    ) -> None:
        self._api_base_url = api_base_url.strip("/") + "/"

        self._do_command: bool = False
        self._attacks: list[AttackCommand] = []
        self._builds: list[BuildCommand] = []
        self._move_base: Coordinate = Coordinate(x=0, y=0)

        self._start_func: TAsyncGameFunc | None = None
        self._loop_func: TAsyncGameFunc | None = None

        self._units_data: UnitsRepsonse | None = None
        self._world_data: WorldResponse | None = None

    def _command(self, payload: CommandPayload) -> CommandResponse:
        response = post(
            self._api_base_url + "play/zombidef/command",
            json=payload.model_dump(),
            headers={"X-Auth-Token": Config.Server.TOKEN},
        )
        if response.status_code != 200:
            resp = ErrorResponse.model_validate(response.json())
            logger.error(f"Error sending command: {resp.error}")
            raise Exception(f"Error sending command: {resp.error}")
        return CommandResponse.model_validate(response.json())

    def _participate(self) -> ParticipateResponse:
        response = put(
            self._api_base_url + "play/zombidef/participate",
            headers={"X-Auth-Token": Config.Server.TOKEN},
        )
        if response.status_code != 200:
            resp = ErrorResponse.model_validate(response.json())
            logger.error(f"Error participating: {resp.error}")
            raise Exception(f"Error participating: {resp.error}")
        return ParticipateResponse.model_validate(response.json())

    def _units(self) -> UnitsRepsonse:
        response = get(
            self._api_base_url + "play/zombidef/units",
            headers={"X-Auth-Token": Config.Server.TOKEN},
        )

        if response.status_code != 200:
            resp = ErrorResponse.model_validate(response.json())
            logger.error(f"Error getting units data: {resp.error}")
            raise Exception(f"Error getting units data: {resp.error}")
        return UnitsRepsonse.model_validate(response.json())

    def _world(self) -> WorldResponse:
        response = get(
            self._api_base_url + "play/zombidef/world",
            headers={"X-Auth-Token": Config.Server.TOKEN},
        )

        if response.status_code != 200:
            resp = ErrorResponse.model_validate(response.json())
            logger.error(f"Error getting world data: {resp.error}")
            raise Exception(f"Error getting world data: {resp.error}")
        return WorldResponse.model_validate(response.json())

    def _rounds(self) -> RoundsResponse:
        response = get(
            self._api_base_url + "rounds/zombidef",
            headers={"X-Auth-Token": Config.Server.TOKEN},
        )

        if response.status_code != 200:
            resp = ErrorResponse.model_validate(response.json())
            logger.error(f"Error getting rounds data: {resp.error}")
            raise Exception(f"Error getting rounds data: {resp.error}")
        return RoundsResponse.model_validate(response.json())

    def attack(self, block_id: str, target: Coordinate) -> None:
        logger.info(f"Attacking {block_id} at {target.x}, {target.y}")
        self._attacks.append(AttackCommand(blockId=block_id, target=target))
        self._do_command = True

    def build(self, target: Coordinate) -> None:
        logger.info(f"Building at {target.x}, {target.y}")
        self._builds.append(BuildCommand(x=target.x, y=target.y))
        self._do_command = True

    def move_base(self, target: Coordinate) -> None:
        logger.info(f"Moving base to {target.x}, {target.y}")
        self._move_base = target
        self._do_command = True

    def units(self) -> UnitsRepsonse:
        if self._units_data is None:
            self._units_data = self._units()
        return self._units_data

    def world(self) -> WorldResponse:
        if self._world_data is None:
            self._world_data = self._world()
        return self._world_data

    def push(self) -> None:
        if self._do_command:
            payload = CommandPayload(
                attack=self._attacks, build=self._builds, moveBase=self._move_base
            )
            logger.info("Pushing command")
            self._command(payload)

    def start(self, func: TAsyncGameFunc) -> TAsyncGameFunc:
        self._start_func = func
        logger.info("Game start function set")
        return func

    def loop(self, func: TAsyncGameFunc) -> TAsyncGameFunc:
        self._loop_func = func
        logger.info("Game loop function set")
        return func

    def run(self) -> None:
        asyncio.run(self._run())

    async def _run(self) -> None:
        if self._start_func is None or self._loop_func is None:
            logger.error("start and loop function must be set")
            raise ValueError("start and loop function must be set")
        logger.info("Game started")
        self._units_data = self._units()
        self._world_data = self._world()
        await self._start_func(self)
        logger.info("Game loop started")
        while True:
            self._units_data = self._units()
            self._world_data = self._world()
            await self._loop_func(self)
            self.push()
            self._attacks = []
            self._builds = []
            self._move_base = Coordinate(x=0, y=0)
            self._do_command = False

            next_tick = self.units().turn_ends_in_ms / 1000
            logger.info(f"Game loop ticked, next turn in {next_tick:.2f} seconds, sleeping for {next_tick + 0.1:.2f} seconds")

            await asyncio.sleep(next_tick + 0.1)
