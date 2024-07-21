from typing import Literal
from aiohttp import ClientSession
from pydantic import BaseModel
from loguru import logger
from config import Config
from ..models.core import (
    CommandPayload,
    ErrorResponse,
    CommandResponse,
    ParticipateResponse,
    UnitsRepsonse,
    WorldResponse,
    RoundsResponse,
)
import asyncio
from abc import ABC, abstractmethod

class BaseApi(ABC):
    @abstractmethod
    async def command(self, payload: CommandPayload) -> CommandResponse | ErrorResponse: ...

    @abstractmethod
    async def participate(self) -> ParticipateResponse | ErrorResponse: ...

    @abstractmethod
    async def units(self) -> UnitsRepsonse | ErrorResponse: ...

    @abstractmethod
    async def world(self) -> WorldResponse | ErrorResponse: ...

    @abstractmethod
    async def rounds(self) -> RoundsResponse | ErrorResponse: ...


class ServerApi(BaseApi):
    def __init__(
        self,
        *,
        api_base_url: str = Config.Server.API_BASE_URL,
        token: str = Config.Server.TOKEN,
    ) -> None:
        self._api_base_url = api_base_url.strip("/")
        self._token = token
        self._session = ClientSession()

    async def request[
        T: BaseModel
    ](
        self,
        method: Literal["GET", "POST", "PUT"],
        path: str,
        output_model: type[T],
        payload: BaseModel | None = None,
    ) -> (T | ErrorResponse):
        headers = {"X-Auth-Token": self._token}
        data = None
        if payload:
            data = payload.model_dump(by_alias=True)

        context_logger = logger.bind(method=method, path=path, data=data)

        context_logger.debug(f"Sending request")

        async with self._session.request(
            method, self._api_base_url + path, json=data, headers=headers
        ) as response:
            if not await response.text():
                context_logger.error(f"No response")
                return ErrorResponse(errCode=-1, error="No response")

            data = await response.json()
            context_logger.debug(f"Response: {data}")
            if response.status != 200:
                resp = ErrorResponse.model_validate(data)
                context_logger.debug(f"Error response: {resp}")
                return resp
            return output_model.model_validate(data)

    async def command(self, payload: CommandPayload) -> CommandResponse | ErrorResponse:
        return await self.request(
            "POST", "/play/zombidef/command", CommandResponse, payload
        )

    async def participate(self) -> ParticipateResponse | ErrorResponse:
        return await self.request(
            "PUT", "/play/zombidef/participate", ParticipateResponse
        )

    async def units(self) -> UnitsRepsonse | ErrorResponse:
        return await self.request("GET", "/play/zombidef/units", UnitsRepsonse)

    async def world(self) -> WorldResponse | ErrorResponse:
        return await self.request("GET", "/play/zombidef/world", WorldResponse)

    async def rounds(self) -> RoundsResponse | ErrorResponse:
        return await self.request("GET", "/rounds/zombidef", RoundsResponse)

    async def close(self) -> None:
        await self._session.close()
        logger.info("Game API session closed")

    async def __aenter__(self) -> "ServerApi":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()
