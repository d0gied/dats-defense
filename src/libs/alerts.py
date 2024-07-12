from aiogram import Bot
from config import Config

import asyncio

bot = Bot(token=Config.Telegram.TOKEN)

async def async_send_alert(message: str):
    await bot.send_message(
        chat_id=Config.Telegram.CHAT_ID,
        message_thread_id=Config.Telegram.TOPIC_ID,
        text=message
    )

def send_alert(message: str):
    asyncio.run(async_send_alert(message))
