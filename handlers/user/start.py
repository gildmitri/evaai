import aiohttp
from aiogram import types, F
from aiogram.filters import CommandStart

from loguru import logger

from loader import dp, N8N_ROUTER_URL, N8N_CHECK_STATUS_URL
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
    await send_to_n8n(data_to_send, user_id, callback.message)


@dp.callback_query(F.data == "user_forecast")
async def handler_user_forecast(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    logger.info(f"user_id={user_id} | Запрос прогноза (user_forecast)")

    await callback.answer()

    data_to_send = {
        "event_type": "user_forecast",
        "user_data": {
            "user_id": user_id,
            "chat_id": callback.message.chat.id,
            "first_name": callback.from_user.first_name,
            "username": callback.from_user.username or "",
            "message_id": callback.message.message_id
        },
        "payload": {}
    }

    # Отправляем в Ева-Роутер
    await send_to_n8n(data_to_send, user_id, callback.message)


@dp.callback_query(F.data == "not_now")
async def handler_not_now(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    logger.info(f"user_id={user_id} | Нажал(а) на кнопку: Не сейчас")

    await callback.answer()

    data_to_send = {
        "event_type": "start_eva_chat",
        "user_data": {
            "user_id": user_id,
            "chat_id": callback.message.chat.id,
            "first_name": callback.from_user.first_name,
            "username": callback.from_user.username or "",
            "message_id": callback.message.message_id
        },
        "payload": {}
    }

    # Отправляем в Ева-Роутер
    await send_to_n8n(data_to_send, user_id, callback.message)


# --- Хэндлер для ЛЮБОГО текста (Router logic) ---
@dp.message()
async def forward_any_message_to_n8n(message: types.Message):
    user_id = message.from_user.id
    logger.info(f"user_id={user_id} | Получено сообщение: '{message.text[:30]}...'")

    # 1. Определяем статус пользователя через n8n (db-access)
    current_event_type = "eva_chat"  # Значение по умолчанию - обычный чат

    try:
        async with aiohttp.ClientSession() as session:
            # Отправляем user_id, чтобы узнать статус
            check_payload = {"user_id": user_id}

            async with session.post(N8N_CHECK_STATUS_URL, json=check_payload) as response:
                if response.status == 200:
                    # Ожидаем ответ от n8n вида: {"status": "interview"} или {"status": "completed"}
                    result = await response.json()
                    # --- ЗАЩИТА ОТ None ---
                    if result is None:
                        logger.warning(f"user_id={user_id} | n8n вернул null. Считаем статус completed.")
                        result = {}
                    # ----------------------
                    status = result.get("status", "completed")

                    if status == "interview":
                        current_event_type = "user_answer"
                        logger.info(f"user_id={user_id} | Статус: Интервью. Тип события: user_answer")
                    else:
                        current_event_type = "eva_chat"
                        logger.info(f"user_id={user_id} | Статус: Чат. Тип события: eva_chat")
                else:
                    logger.warning(f"user_id={user_id} | Не удалось проверить статус. Используем eva_chat")

    except Exception as e:
        logger.error(f"user_id={user_id} | Ошибка проверки статуса: {e}")
        # Если ошибка проверки - считаем, что это чат, чтобы не ломать логику
        current_event_type = "eva_chat"

    # 2. Формируем основной пакет данных
    data_to_send = {
        "event_type": current_event_type,  # <--- Подставляем определенный тип
        "user_data": {
            "user_id": message.from_user.id,
            "chat_id": message.chat.id,
            "first_name": message.from_user.first_name,
            "username": message.from_user.username or "",
            "message_id": message.message_id
        },
        "payload": {
            "text": message.text
        }
    }

    # 3. Отправляем в основной роутер
    await send_to_n8n(data_to_send, user_id, message)


async def send_to_n8n(data, user_id, message_obj):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(N8N_ROUTER_URL, json=data) as response:
                if response.status == 200:
                    logger.success(f"user_id={user_id} | Успешно отправлено в n8n ({data['event_type']})")
                else:
                    text_resp = await response.text()
                    logger.error(f"user_id={user_id} | Ошибка n8n {response.status}: {text_resp}")
    except aiohttp.ClientConnectorError as e:
        logger.critical(f"user_id={user_id} | Ошибка подключения к n8n: {e}")
