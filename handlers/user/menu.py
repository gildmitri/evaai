from aiogram import types
from aiogram.filters import Command
from loguru import logger

# --- Импорт основного диспетчера ---
from loader import dp

# --- Тексты для команд меню ---
MSG_IN_DEVELOPMENT = "Раздел находится в разработке ⚙️"
MSG_HELP = "Техническая поддержка — @gildmitri"


# --- Хэндлер на команду /sub (Управление подпиской) ---
@dp.message(Command("sub"))
async def cmd_sub(message: types.Message):
    user_id = message.from_user.id
    logger.info(f"user_id={user_id} | /sub | Пользователь запросил управление подпиской")
    await message.answer(MSG_IN_DEVELOPMENT)


# --- Хэндлер на команду /ref (Поделиться с друзьями) ---
@dp.message(Command("ref"))
async def cmd_ref(message: types.Message):
    user_id = message.from_user.id
    logger.info(f"user_id={user_id} | /ref | Пользователь запросил реферальную ссылку")
    await message.answer(MSG_IN_DEVELOPMENT)


# --- Хэндлер на команду /gift (Подарить близким) ---
@dp.message(Command("gift"))
async def cmd_gift(message: types.Message):
    user_id = message.from_user.id
    logger.info(f"user_id={user_id} | /gift | Пользователь хочет подарить подписку")
    await message.answer(MSG_IN_DEVELOPMENT)


# --- Хэндлер на команду /help (Поддержка) ---
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    user_id = message.from_user.id
    logger.info(f"user_id={user_id} | /help | Пользователь запросил помощь")
    await message.answer(MSG_HELP)
