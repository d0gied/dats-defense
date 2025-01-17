from configloader import envstr, envint, LoaderConfig

class Config:
    class Telegram:
        TOKEN: str = envstr("TELEGRAM_BOT_TOKEN")
        CHAT_ID: int = envint("TELEGRAM_CHAT_ID")
        TOPIC_ID: int = envint("TELEGRAM_TOPIC_ID")

    class Server:
        API_BASE_URL: str = "https://games.datsteam.dev/"
        API_TEST_BASE_URL: str = "https://games-test.datsteam.dev/"
        TOKEN: str = envstr("TEAM_TOKEN")

    class Metrics:
        INFLUXDB_TOKEN = envstr("INFLUXDB_TOKEN")
