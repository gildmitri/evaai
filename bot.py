import asyncio
from aiogram import Bot, types

from loader import dp, bot

import handlers

from loguru import logger


async def set_commands(bot: Bot):
    """
    Создает и устанавливает список команд (меню) для бота.
    """
    commands = [
        types.BotCommand(command="start", description="⭐️ Начать"),
        types.BotCommand(command="sub", description="⚙️ Управление подпиской"),
        types.BotCommand(command="ref", description="🫂 Поделиться с друзьями"),
        types.BotCommand(command="gift", description="🎁 Подарить близким"),
        types.BotCommand(command="help", description="⚖️ Поддержка")
    ]
    await bot.set_my_commands(commands)
    logger.info("Команды меню успешно установлены.")


async def main():
    logger.info("Бот запущен!")

    await set_commands(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
