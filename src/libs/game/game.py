from config import Config
from ..models.core import CommandPayload, CommandResponse, ErrorResponse
from typing import Any
from requests import post, get, put, Session
import urllib3


class Game:
    def __init__(
        self,
        *,
        api_base_url: str = Config.Server.API_BASE_URL,
    ) -> None:
        self.api_base_url = api_base_url.strip("/") + "/"

    def _command(self, payload: CommandPayload) -> CommandResponse | ErrorResponse:
        response = post(
            self.api_base_url + "zombidef/command", json=payload.model_dump()
        )
        if response.status_code != 200:
            return ErrorResponse.model_validate(response.json())
        return CommandResponse.model_validate(response.json())

    def _participate(self) -> None: ...

    def _units(self) -> Any: ...

    def _world(self) -> Any: ...

    def _zombiedef(self) -> Any: ...
