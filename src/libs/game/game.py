from config import Config
from libs.models.block import EnemyBase
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
    Coordinate,
    Base
)
from typing import Any, Callable, Awaitable, Coroutine
from requests import post, get, put, Session
import urllib3
import asyncio
from loguru import logger
from time import perf_counter
from fastapi import FastAPI

TAsyncGameFunc = Callable[["Game"], Coroutine[Any, Any, None]]
async def mock_func(game: "Game") -> None:
    pass

BASE_DAMAGE = 10
HEAD_DAMAGE = 40

def timing(func: Any) -> Any:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter()
        result = func(*args, **kwargs)
        logger.info(f"{func.__name__} executed in {perf_counter() - start_time:.6f} seconds")
        return result

    return wrapper

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

        self._start_funcs: list[TAsyncGameFunc] = []
        self._loop_funcs: list[TAsyncGameFunc] = []
        self._waiting_funcs: list[TAsyncGameFunc] = []
        self._dead_funcs: list[TAsyncGameFunc] = []

        self._units_data: UnitsRepsonse | ErrorResponse | None = None
        self._world_data: WorldResponse | ErrorResponse | None = None
        self._participate_data: ParticipateResponse | ErrorResponse | None = None

        self._extra_gold: int = 0 # for killing zombies

    def _command(self, payload: CommandPayload) -> CommandResponse:
        response = post(
            self._api_base_url + "play/zombidef/command",
            json=payload.model_dump(),
            headers={"X-Auth-Token": Config.Server.TOKEN},
        )
        if response.status_code != 200:
            resp = ErrorResponse.model_validate(response.json())
            logger.debug(f"Error sending command: {resp}")
            raise Exception(f"Error sending command: {resp.error}")
        return CommandResponse.model_validate(response.json())

    def _participate(self) -> ParticipateResponse | ErrorResponse:
        response = put(
            self._api_base_url + "play/zombidef/participate",
            headers={"X-Auth-Token": Config.Server.TOKEN},
        )
        if response.status_code != 200:
            resp = ErrorResponse.model_validate(response.json())
            logger.debug(f"Error participating: {resp}")
            return resp
        return ParticipateResponse.model_validate(response.json())

    def _units(self) -> UnitsRepsonse | ErrorResponse:
        response = get(
            self._api_base_url + "play/zombidef/units",
            headers={"X-Auth-Token": Config.Server.TOKEN},
        )

        if response.status_code != 200:
            resp = ErrorResponse.model_validate(response.json())
            logger.debug(f"Error getting units data: {resp}")
            return resp
        return UnitsRepsonse.model_validate(response.json())

    def _world(self) -> WorldResponse | ErrorResponse:
        response = get(
            self._api_base_url + "play/zombidef/world",
            headers={"X-Auth-Token": Config.Server.TOKEN},
        )

        if response.status_code != 200:
            resp = ErrorResponse.model_validate(response.json())
            logger.debug(f"Error getting world data: {resp}")
            return resp
        return WorldResponse.model_validate(response.json())

    def _rounds(self) -> RoundsResponse:
        response = get(
            self._api_base_url + "rounds/zombidef",
            headers={"X-Auth-Token": Config.Server.TOKEN},
        )

        if response.status_code != 200:
            resp = ErrorResponse.model_validate(response.json())
            logger.debug(f"Error getting rounds data: {resp}")
            raise Exception(f"Error getting rounds data: {resp.error}")
        return RoundsResponse.model_validate(response.json())

    @timing
    def get_head(self) -> Base:
        for block in self.units().base:
            if block.is_head:
                return block
        logger.error("No head block found")
        raise Exception("No head block found")

    @timing
    def get_block_by_id(self, block_id: str) -> Base | None:
        for block in self.units().base:
            if block.id == block_id:
                return block
        return None

    @timing
    def get_base_at(self, x: int, y: int) -> Base | None:
        for base in self.units().base:
            if base.x == x and base.y == y:
                return base
        return None

    @timing
    def is_connected(self, block_id: str) -> bool:
        blocks = self.units().base
        head = self.get_head()

        queue = [head]
        visited: set[str] = set()
        while queue:
            current = queue.pop(0)
            visited.add(current.id)
            if current.id == block_id:
                return True

            for block in blocks:
                if block.id not in visited and abs(block.x - current.x) + abs(block.y - current.y) == 1:
                    queue.append(block)

        return False

    @timing
    def get_all_accessible_targets(self, block_id: str) -> list[Zombie | EnemyBase]:
        blocks = self.units().base
        block = self.get_block_by_id(block_id)
        if block is None:
            logger.error(f"Block {block_id} not found")
            raise Exception(f"Block {block_id} not found")

        max_distance = 8 if block.is_head else 4
        targets = []

        for zombie in self.units().zombies:
            distance = abs(zombie.x - block.x) ** 2 + abs(zombie.y - block.y) ** 2
            if distance <= max_distance * max_distance:
                targets.append(zombie)

        for enemy in self.units().enemy_blocks:
            distance = abs(enemy.x - block.x) ** 2 + abs(enemy.y - block.y) ** 2
            if distance <= max_distance * max_distance:
                targets.append(enemy)

        return targets

    def get_turn(self) -> int:
        return self.units().turn

    def get_gold(self, extra=True) -> int:
        if extra:
            return self.units().player.gold + extra
        return self.units().player.gold

    @timing
    def get_all_connected(self) -> list[Base]:
        blocks = self.units().base
        head = self.get_head()

        queue: list[Base] = [head]
        visited: set[str] = set()
        connected = []
        while queue:
            current = queue.pop(0)
            visited.add(current.id)
            connected.append(current)

            for block in blocks:
                if block.id not in visited and abs(block.x - current.x) + abs(block.y - current.y) == 1:
                    queue.append(block)

        return connected

    @timing
    def attack(self, block_id: str, target: Coordinate) -> bool:
        if not self.is_connected(block_id):
            logger.warning(f"Block {block_id} is not connected to the head")
            return False

        block = self.get_block_by_id(block_id)
        if block is None:
            logger.warning(f"Block {block_id} not found")
            return False
        distance = abs(target.x - block.x) ** 2 + abs(target.y - block.y) ** 2

        if block.is_head and distance > 64:
            logger.warning(f"Head block can only attack at distance 8, not {distance ** 0.5:.2f}")
            return False

        if not block.is_head and distance > 16:
            logger.warning(f"Block can only attack at distance 4, not {distance ** 0.5:.2f}")
            return False

        killed_zombies: int = 0
        damage = HEAD_DAMAGE if block.is_head else BASE_DAMAGE
        for zombie in self.units().zombies:
            if zombie.x == target.x and zombie.y == target.y:
                killed_zombies += zombie.health <= damage

        self._extra_gold += killed_zombies

        logger.info(f"Attacking {block_id} at {target.x}, {target.y}, {killed_zombies} zombies killed")
        self._attacks.append(AttackCommand(blockId=block_id, target=target))
        self._do_command = True

        return True

    @timing
    def build(self, target: Coordinate) -> bool:
        has_base = False
        free_gold = self.units().player.gold + self._extra_gold - len(self._builds)
        if free_gold < 1:
            logger.warning(f"Not enough gold to build at {target.x}, {target.y}")
            return False

        for base in self.units().base:
            if base.x == target.x and base.y == target.y:
                logger.warning(f"Base already exists at {target.x}, {target.y}")
                return False
            if abs(base.x - target.x) + abs(base.y - target.y) == 1:
                has_base = True

        if not has_base:
            logger.warning(f"No base nearby {target.x}, {target.y}")
            return False

        for base in self.units().enemy_blocks:
            if abs(base.x - target.x) <= 1 and abs(base.y - target.y) <= 1:
                logger.warning(f"Enemy block({base.x}, {base.y}) too close to {target.x}, {target.y}")
                return False

        for zombie in self.units().zombies:
            if zombie.x == target.x and zombie.y == target.y:
                logger.warning(f"Zombie({zombie.type}) already exists at {target.x}, {target.y}")
                return False

        for zpot in self.world().zpots:
            if zpot.x == target.x and zpot.y == target.y:
                logger.warning(f"Zpot({zpot.type}) already exists at {target.x}, {target.y}")
                return False
            if abs(zpot.x - target.x) + abs(zpot.y - target.y) == 1:
                logger.warning(f"Zpot({zpot.x}, {zpot.y}) too close to {target.x}, {target.y}")
                return False

        logger.info(f"Building at {target.x}, {target.y}")
        self._builds.append(BuildCommand(x=target.x, y=target.y))
        self._do_command = True
        return True


    @timing
    def move_base(self, target: Coordinate) -> None:
        if self.get_base_at(target.x, target.y) is None:
            logger.warning(f"Block already exists at {target.x}, {target.y}")
            return
        logger.info(f"Moving base to {target.x}, {target.y}")
        self._move_base = target
        self._do_command = True

    def units(self) -> UnitsRepsonse:
        if self._units_data is None:
            resp = self._units()
            self._units_data = resp
        if isinstance(self._units_data, ErrorResponse):
            raise Exception(f"Error: {self._units_data.error}")
        return self._units_data

    def world(self) -> WorldResponse:
        if self._world_data is None:
            resp = self._world()
            self._world_data = resp
        if isinstance(self._world_data, ErrorResponse):
            raise Exception(f"Error: {self._world_data.error}")
        return self._world_data

    def push(self) -> None:
        if self._do_command:
            payload = CommandPayload(
                attack=self._attacks, build=self._builds, moveBase=self._move_base
            )
            logger.info("Pushing command")
            self._command(payload)

    def start(self, func: TAsyncGameFunc) -> TAsyncGameFunc:
        self._start_funcs.append(func)
        logger.info("Game start function set")
        return func

    def loop(self, func: TAsyncGameFunc) -> TAsyncGameFunc:
        self._loop_funcs.append(func)
        logger.info("Game loop function set")
        return func

    def waiting(self, func: TAsyncGameFunc) -> TAsyncGameFunc:
        self._waiting_funcs.append(func)
        logger.info("Game waiting function set")
        return func

    def dead(self, func: TAsyncGameFunc) -> TAsyncGameFunc:
        self._dead_funcs.append(func)
        logger.info("Game dead function set")
        return func

    def run(self) -> None:
        asyncio.run(self._run())

    async def _run(self, force=False) -> None:

        current_state = "UNKNOWN"
        logger.info("Loop started")

        while True:
            self._units_data = self._units()
            self._world_data = self._world()
            self._participate_data = self._participate()
            next_tick: float = 2

            if isinstance(self._participate_data, ParticipateResponse):
                if not current_state.startswith("PREPARING") \
                    or abs(self._participate_data.starts_in_sec - 60) <= 1 \
                    or abs(self._participate_data.starts_in_sec - 30) <= 1 \
                    or abs(self._participate_data.starts_in_sec - 10) <= 1 \
                    or abs(self._participate_data.starts_in_sec - 5) <= 1:
                    logger.info(f"Preparing game, starts in {self._participate_data.starts_in_sec} seconds")
                current_state = "PREPARING"
                logger.debug(f"Game starts in {self._participate_data.starts_in_sec} seconds")
                for func in self._waiting_funcs:
                    try:
                        await func(self)
                    except Exception as e:
                        logger.error(e)

            elif isinstance(self._units_data, UnitsRepsonse) and self._units_data.base:
                self._attacks = []
                self._builds = []
                self._move_base = Coordinate(x=self.get_head().x, y=self.get_head().y)
                self._do_command = False

                if current_state != "RUNNING":
                    for func in self._start_funcs:
                        try:
                            await func(self)
                        except Exception as e:
                            logger.error(e)
                    logger.info("Game started")
                current_state = "RUNNING"
                for func in self._loop_funcs:
                    try:
                        await func(self)
                    except Exception as e:
                        logger.error(e)
                self.push()

                next_tick = self.units().turn_ends_in_ms / 1000
            else:
                if current_state != "DEAD":
                    for func in self._dead_funcs:
                        try:
                            await func(self)
                        except Exception as e:
                            logger.error(e)
                for func in self._waiting_funcs:
                    try:
                        await func(self)
                    except Exception as e:
                        logger.error(e)
                current_state = "DEAD"

            logger.debug(f"Game loop ticked, next turn in {next_tick:.2f} seconds, sleeping for {next_tick + 0.1:.2f} seconds")
            await asyncio.sleep(next_tick + 0.1)
