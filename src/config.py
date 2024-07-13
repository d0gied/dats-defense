from configloader import envstr, envint, LoaderConfig

LoaderConfig.set_auto_load_dotenv(True)

class Config:
    class Telegram:
        TOKEN: str = envstr("TELEGRAM_BOT_TOKEN")
        CHAT_ID: str = envstr("TELEGRAM_CHAT_ID")
        TOPIC_ID: int = envint("TELEGRAM_TOPIC_ID")

    class Server:
        API_BASE_URL: str = "https://games.datsteam.dev/"
        API_TEST_BASE_URL: str = "https://games-test.datsteam.dev/"
        TOKEN: str = envstr("TEAM_TOKEN")
