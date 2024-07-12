from config import Config
from ..models.core import CommandPayload, CommandResponse, ErrorResponse, ParticipateResponse, UnitsRepsonse, WorldResponse, RoundsResponse
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
            self.api_base_url + "play/zombidef/command", json=payload.model_dump(),
            headers={ "X-Auth-Token": Config.Server.TOKEN },
        )
        if response.status_code != 200:
            return ErrorResponse.model_validate(response.json())
        return CommandResponse.model_validate(response.json())

    def _participate(self) -> ErrorResponse | ParticipateResponse:
        response = put(
          self.api_base_url + "play/zombidef/participate",
          headers={ "X-Auth-Token": Config.Server.TOKEN },
        )
        if response.status_code != 200:
          return ErrorResponse.model_validate(response.json())
        return ParticipateResponse.model_validate(response.json())

    def _units(self) -> ErrorResponse | UnitsRepsonse:
        response = get(
            self.api_base_url + "play/zombidef/units",
            headers={ "X-Auth-Token": Config.Server.TOKEN },
        )

        if response.status_code != 200:
            return ErrorResponse.model_validate(response.json())
        return UnitsRepsonse.model_validate(response.json())

    def _world(self) -> ErrorResponse | WorldResponse:
        response = get(
            self.api_base_url + "play/zombidef/world",
            headers={ "X-Auth-Token": Config.Server.TOKEN },
        )

        if response.status_code != 200:
            return ErrorResponse.model_validate(response.json())
        return WorldResponse.model_validate(response.json())

    def _rounds(self) -> ErrorResponse | RoundsResponse:
        response = get(
            self.api_base_url + "rounds/zombidef",
            headers={ "X-Auth-Token": Config.Server.TOKEN },
        )

        if response.status_code != 200:
            return ErrorResponse.model_validate(response.json())
        return RoundsResponse.model_validate(response.json())
