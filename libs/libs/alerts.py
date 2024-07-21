from aiogram import Bot
from .config import Config
from loguru import logger
from enum import Enum

import asyncio

ERROR_ALERT = ":red_circle: {message}"
INFO_ALERT = ":green_circle: {message}"
WARNING_ALERT = ":yellow_circle: {message}"

class AlertTopic(Enum):
    ALERTS = 2

class AlertManager:
    def __init__(self):
        self.bot: Bot = Bot(token=Config.Telegram.TOKEN)


    async def __aenter__(self):
        return self

    async def send_alert(self, message: str):
        logger.debug("Sending alert: {message}")
        await self.bot.send_message(
            chat_id=Config.Telegram.CHAT_ID,
            text=message,
            message_thread_id=Config.Telegram.TOPIC_ID,
        )

    async def info_alert(self, message: str):
        await self.send_alert(INFO_ALERT.format(message=message))

    async def warning_alert(self, message: str):
        await self.send_alert(WARNING_ALERT.format(message=message))

    async def error_alert(self, message: str):
        await self.send_alert(ERROR_ALERT.format(message=message))

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        logger.info("Closing bot")
        await self.bot.session.close()
