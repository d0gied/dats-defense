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
        self._attacks: list[AttackCommand] = []
        self._builds: list[BuildCommand] = []
        self._move_base: Coordinate = Coordinate(x=0, y=0)

        self._start_func: TAsyncGameFunc | None = None
        self._loop_func: TAsyncGameFunc | None = None

        self._next_tick: int = 1

    def _command(self, payload: CommandPayload) -> CommandResponse | ErrorResponse:
        response = post(
            self._api_base_url + "play/zombidef/command",
            json=payload.model_dump(),
            headers={"X-Auth-Token": Config.Server.TOKEN},
        )
        if response.status_code != 200:
            return ErrorResponse.model_validate(response.json())
        return CommandResponse.model_validate(response.json())

    def _participate(self) -> ErrorResponse | ParticipateResponse:
        response = put(
            self._api_base_url + "play/zombidef/participate",
            headers={"X-Auth-Token": Config.Server.TOKEN},
        )
        if response.status_code != 200:
            return ErrorResponse.model_validate(response.json())
        return ParticipateResponse.model_validate(response.json())

    def _units(self) -> ErrorResponse | UnitsRepsonse:
        response = get(
            self._api_base_url + "play/zombidef/units",
            headers={"X-Auth-Token": Config.Server.TOKEN},
        )

        if response.status_code != 200:
            return ErrorResponse.model_validate(response.json())
        return UnitsRepsonse.model_validate(response.json())

    def _world(self) -> ErrorResponse | WorldResponse:
        response = get(
            self._api_base_url + "play/zombidef/world",
            headers={"X-Auth-Token": Config.Server.TOKEN},
        )

        if response.status_code != 200:
            return ErrorResponse.model_validate(response.json())
        return WorldResponse.model_validate(response.json())

    def _rounds(self) -> ErrorResponse | RoundsResponse:
        response = get(
            self._api_base_url + "rounds/zombidef",
            headers={"X-Auth-Token": Config.Server.TOKEN},
        )

        if response.status_code != 200:
            return ErrorResponse.model_validate(response.json())
        return RoundsResponse.model_validate(response.json())

    def attack(self, block_id: str, target: Coordinate) -> None:
        logger.info(f"Attacking {block_id} at {target.x}, {target.y}")
        self._attacks.append(AttackCommand(blockId=block_id, target=target))

    def build(self, target: Coordinate) -> None:
        logger.info(f"Building at {target.x}, {target.y}")
        self._builds.append(BuildCommand(x=target.x, y=target.y))

    def move_base(self, target: Coordinate) -> None:
        logger.info(f"Moving base to {target.x}, {target.y}")
        self._move_base = target

    def push(self) -> CommandResponse | ErrorResponse:
        payload = CommandPayload(
            attack=self._attacks, build=self._builds, moveBase=self._move_base
        )
        logger.info("Pushing command")
        return self._command(payload)

    def start(self, func: TAsyncGameFunc) -> TAsyncGameFunc:
        self._start_func = func
        logger.info("Game start function set")
        return func

    def loop(self, func: TAsyncGameFunc) -> TAsyncGameFunc:
        self._loop_func = func
        logger.info("Game loop function set")
        return func

    def set_next_tick_in_seconds(self, seconds: int) -> None:
        logger.info(f"Setting next tick in {seconds} seconds")
        self._next_tick = seconds


    def run(self) -> None:
        asyncio.run(self._run())

    async def _run(self) -> None:
        if self._start_func is None or self._loop_func is None:
            logger.error("start and loop function must be set")
            raise ValueError("start and loop function must be set")
        logger.info("Game started")
        await self._start_func(self)
        logger.info("Game loop started")
        while True:
            await self._loop_func(self)
            await asyncio.sleep(self._next_tick)
            self._attacks = []
            self._builds = []
            self._move_base = Coordinate(x=0, y=0)
            self._next_tick = 1
            logger.info("Game loop ticked")
