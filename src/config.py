from configloader import envstr, envint

class Config:
    class Telegram:
       TOKEN: str = envstr("TELEGRAM_BOT_TOKEN")
       CHAT_ID: int = envint("TELEGRAM_CHAT_ID")
       TOPIC_ID: int = envint("TELEGRAM_TOPIC_ID")
