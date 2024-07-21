
from libs.models.core import ErrorResponse, Round
from .api import BaseApi
from datetime import datetime
from enum import Enum


class GameDispatcher:
    def __init__(
        self,
        api: BaseApi,
    ) -> None:
        self.api = api
        self.rounds: list[Round] = []

    async def get_units(self): ...

    async def _update_rounds(self) -> None:
        response = await self.api.rounds()
        if isinstance(response, ErrorResponse):
            raise Exception(response.error)
        self.rounds = response.rounds

    async def current_round(self) -> Round | None:
        if not self.rounds:
            await self._update_rounds()

        now = datetime.now().astimezone()
        for round in self.rounds:
            if round.start_at <= now and now <= round.end_at:
                return round

        return None

    async def next_round(self) -> Round | None:
        if not self.rounds:
            await self._update_rounds()

        now = datetime.now().astimezone()
        for round in self.rounds:
            if now < round.start_at:
                return round

        return None
