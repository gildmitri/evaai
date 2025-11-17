import aiohttp
from aiogram import types, F
from aiogram.filters import CommandStart

from loguru import logger

from loader import dp, N8N_ONBOARDING_WEBHOOK_URL
from data.texts import (
    MSG_STEP_1, MSG_STEP_2, MSG_STEP_3, MSG_STEP_4,
    MSG_STEP_5, MSG_STEP_6, MSG_STEP_7, MSG_START_FORECAST
)
from keyboards.start import (
    kb_onboarding_step_1, kb_onboarding_step_2, kb_onboarding_step_3,
    kb_onboarding_step_4, kb_onboarding_step_5, kb_onboarding_step_6,
    kb_onboarding_step_7
)


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    logger.info(f"user_id={message.from_user.id} | /start")

    await message.answer(
        MSG_STEP_1.format(name=message.from_user.first_name),
        reply_markup=kb_onboarding_step_1.as_markup()
    )


@dp.callback_query(F.data == "onboarding_step_2")
async def step_1_to_2(callback: types.CallbackQuery):
    logger.info(f"user_id={callback.from_user.id} | Онбординг: перешел на шаг 2")

    await callback.message.edit_text(
        MSG_STEP_2,
        reply_markup=kb_onboarding_step_2.as_markup()
    )

    await callback.answer()


@dp.callback_query(F.data == "onboarding_step_3")
async def step_2_to_3(callback: types.CallbackQuery):
    logger.info(f"user_id={callback.from_user.id} | Онбординг: перешел на шаг 3")

    await callback.message.edit_text(
        MSG_STEP_3,
        reply_markup=kb_onboarding_step_3.as_markup()
    )

    await callback.answer()


@dp.callback_query(F.data == "onboarding_step_4")
async def step_3_to_4(callback: types.CallbackQuery):
    logger.info(f"user_id={callback.from_user.id} | Онбординг: перешел на шаг 4")

    await callback.message.edit_text(
        MSG_STEP_4,
        reply_markup=kb_onboarding_step_4.as_markup()
    )

    await callback.answer()


@dp.callback_query(F.data == "onboarding_step_5")
async def step_4_to_5(callback: types.CallbackQuery):
    logger.info(f"user_id={callback.from_user.id} | Онбординг: перешел на шаг 5")

    await callback.message.edit_text(
        MSG_STEP_5,
        reply_markup=kb_onboarding_step_5.as_markup()
    )

    await callback.answer()


@dp.callback_query(F.data == "onboarding_step_6")
async def step_5_to_6(callback: types.CallbackQuery):
    logger.info(f"user_id={callback.from_user.id} | Онбординг: перешел на шаг 6")

    await callback.message.edit_text(
        MSG_STEP_6,
        reply_markup=kb_onboarding_step_6.as_markup()
    )

    await callback.answer()


@dp.callback_query(F.data == "onboarding_step_7")
async def step_6_to_7(callback: types.CallbackQuery):
    logger.info(f"user_id={callback.from_user.id} | Онбординг: перешел на шаг 7")

    await callback.message.edit_text(
        MSG_STEP_7,
        reply_markup=kb_onboarding_step_7.as_markup()
    )

    await callback.answer()


# --- Финальный обработчик: запуск прогноза (опроса в n8n) ---
@dp.callback_query(F.data == "start_forecast")
async def start_forecast(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    logger.info(f"user_id={user_id} | Запуск опроса | Передача управления в n8n")

    # 1. Отправляем финальное сообщение пользователю
    await callback.message.edit_text(MSG_START_FORECAST, reply_markup=None)
    await callback.answer()

    # 2. Формируем JSON для n8n
    data_to_send = {
        "event_type": "start_quiz",
        "user_data": {
            "user_id": callback.from_user.id,
            "chat_id": callback.message.chat.id,
            "first_name": callback.from_user.first_name,
            "username": callback.from_user.username if callback.from_user.username else "",
            "message_id": callback.message.message_id
        },
        "payload": {}
    }

    # 3. Отправляем вебхук в n8n
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(N8N_ONBOARDING_WEBHOOK_URL, json=data_to_send) as response:
                if response.status == 200:
                    logger.success(f"user_id={user_id} | Успешная передача в n8n")
                else:
                    logger.error(
                        f"user_id={user_id} | Ошибка от n8n. Статус: {response.status}, Ответ: {await response.text()}"
                    )
                    await callback.message.answer(
                        "Произошла небольшая ошибка на сервере. Попробуйте начать заново: /start"
                    )
    except aiohttp.ClientConnectorError as e:
        logger.critical(f"user_id={user_id} | Ошибка подключения к n8n: {e}")
        await callback.message.answer(
            "Не удалось связаться с сервером для начала опроса. Пожалуйста, попробуйте позже, нажав /start."
        )


# ----------------------------------------------------------------------------------------------------------------------
# ВАЖНО: Этот хэндлер должен быть последним в цепочке обработчиков сообщений,
# так как он ловит ЛЮБОЕ текстовое сообщение.
# ----------------------------------------------------------------------------------------------------------------------
@dp.message()
async def forward_any_message_to_n8n(message: types.Message):
    """
    Этот хэндлер перехватывает любое текстовое сообщение, которое не было обработано ранее,
    и пересылает его в n8n для дальнейшей обработки (например, как ответ на вопрос).
    """
    user_id = message.from_user.id
    # Логируем только часть сообщения для краткости
    logger.info(f"user_id={user_id} | Пересылка сообщения в n8n: '{message.text[:30]}...'")

    # 1. Формируем JSON для n8n в формате "ответ пользователя"
    data_to_send = {
        "event_type": "user_answer",
        "user_data": {
            "user_id": message.from_user.id,
            "chat_id": message.chat.id,
            "first_name": message.from_user.first_name,
            "username": message.from_user.username if message.from_user.username else "",
            "message_id": message.message_id
        },
        "payload": {
            "text": message.text
        }
    }

    # 2. Отправляем вебхук в n8n
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(N8N_ONBOARDING_WEBHOOK_URL, json=data_to_send) as response:
                if response.status == 200:
                    logger.success(f"user_id={user_id} | Сообщение успешно переслано в n8n")
                else:
                    logger.error(
                        f"user_id={user_id} | Ошибка от n8n при пересылке. Статус: {response.status}, Ответ: {await response.text()}"
                    )
    except aiohttp.ClientConnectorError as e:
        logger.critical(f"user_id={user_id} | Ошибка подключения к n8n при пересылке сообщения: {e}")
