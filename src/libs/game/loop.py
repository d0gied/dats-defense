from config import Config

class Game:
  def __init__(
    self,
    api_base_url: str = Config.Server.API_BASE_URL,
  ) -> None:
    self.api_base_url = api_base_url
