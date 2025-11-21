from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from data.config_reader import Settings

from loguru import logger

config = Settings()

bot = Bot(
    token=config.BOT_TOKEN.get_secret_value(),
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)
dp = Dispatcher(storage=MemoryStorage())

logger.add(
    "logs/{time:DD-MM-YYYY}.log",
    format="[{time:DD.MM.YYYY HH:mm:ss}] {message}",
    level="INFO",
    rotation="00:00",
    buffering=True
)

N8N_ROUTER_URL = "https://citouloniquu.beget.app/webhook/eva-router"
N8N_CHECK_STATUS_URL = "https://citouloniquu.beget.app/webhook/db-access"
