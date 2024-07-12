from config import Config
from ..models.core import CommandPayload
from typing import Any


class Game:
  def __init__(
    self,
    *,
    api_base_url: str = Config.Server.API_BASE_URL,
  ) -> None:
    self.api_base_url = api_base_url

  def _command(self, payload: CommandPayload) -> None: ...

  def _participate(self) -> None: ...

  def _units(self) -> Any: ...

  def _world(self) -> Any: ...

  def _zombiedef(self) -> Any: ...
