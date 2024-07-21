from functools import wraps
from config import Config
from libs.models.block import Block, EnemyBase
from libs.models.player import Player
from libs.models.zombie import Zombie
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
    Base,
    ZPot,
)
from ..models.cell import Cell, Coordinate
from typing import Any, Callable, Awaitable, Coroutine
from requests import post, get, put, Session
import urllib3
import asyncio
from loguru import logger
from time import perf_counter
from fastapi import FastAPI
from .api import ServerApi

TAsyncGameFunc = Callable[["Game"], Coroutine[Any, Any, None]]


async def mock_func(game: "Game") -> None: ...


BASE_DAMAGE = 10
HEAD_DAMAGE = 40


def timing(func):
    def wrapper(*args: Any, **kwargs: Any):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        logger.debug(
            f"{func.__name__} executed in {perf_counter() - start_time:.6f} seconds"
        )
        return result

    return wraps(func)(wrapper)


class Game:
    def __init__(self, *, api: ServerApi) -> None:
        self._api = api

        self._do_command: bool = False
        self._attacks: list[AttackCommand] = []
        self._builds: list[BuildCommand] = []
        self._move_base: Coordinate | None = None

        self._start_funcs: list[TAsyncGameFunc] = []
        self._loop_funcs: list[TAsyncGameFunc] = []
        self._waiting_funcs: list[TAsyncGameFunc] = []
        self._dead_funcs: list[TAsyncGameFunc] = []

        self._units_data: UnitsRepsonse | ErrorResponse
        self._world_data: WorldResponse | ErrorResponse
        self._participate_data: ParticipateResponse | ErrorResponse

        self._extra_gold: int = 0  # for killing zombies
        self._is_connected_last: int = -1

    def attack(self, block: Block, target: Coordinate | Cell) -> None: ...

    @timing
    def can_build(self, target: Coordinate, no_warn: bool = False) -> bool:
        has_base = False
        free_gold = self.player.gold + self._extra_gold - len(self._builds)
        if free_gold < 1:
            return False

        for base in self.units.base:
            if base.x == target.x and base.y == target.y:
                return False
            if abs(base.x - target.x) + abs(base.y - target.y) == 1:
                has_base = True

        if not has_base:
            return False

        for base in self.units.enemy_blocks:
            if abs(base.x - target.x) <= 1 and abs(base.y - target.y) <= 1:
                return False

        for zombie in self.units.zombies:
            if zombie.x == target.x and zombie.y == target.y:
                return False

        for zpot in self.world.zpots:
            if zpot.x == target.x and zpot.y == target.y:
                return False
            if abs(zpot.x - target.x) + abs(zpot.y - target.y) == 1:
                return False
        return True

    def build(self, target: Coordinate) -> bool:
        if not self.can_build(target):
            return False
        logger.info(f"Building at {target.x}, {target.y}")
        self._builds.append(BuildCommand(x=target.x, y=target.y))
        self._do_command = True
        return True

    def move_base(self, target: Coordinate) -> bool: ...

    @property
    def units(self) -> UnitsRepsonse:
        if isinstance(self._units_data, ErrorResponse):
            raise Exception(f"Error: {self._units_data.error}")
        return self._units_data

    @property
    def world(self) -> WorldResponse:
        if isinstance(self._world_data, ErrorResponse):
            raise Exception(f"Error: {self._world_data.error}")
        return self._world_data

    async def push(self) -> None:
        if self._do_command:
            payload = CommandPayload(
                attack=self._attacks, build=self._builds, moveBase=self._move_base
            )
            logger.info("Pushing command")
            result = await self._api.command(payload)
            logger.debug(result)

    @property
    def turn(self) -> int:
        return self.units.turn

    @property
    def turn_ends_in_ms(self) -> int:
        return self.units.turn_ends_in_ms

    @property
    def player(self) -> Player:
        return self.units.player
