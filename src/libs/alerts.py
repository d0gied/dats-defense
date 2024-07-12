from aiogram import Bot
from config import Config

import asyncio


class AlertManager:
    def __init__(self):
        self.bot: Bot
