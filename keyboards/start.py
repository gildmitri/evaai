from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

# --- Шаг 1: Приветствие ---
kb_onboarding_step_1 = InlineKeyboardBuilder()
kb_onboarding_step_1.row(
    types.InlineKeyboardButton(
        text="Что мы можем обсудить?",
        callback_data="onboarding_step_2"
    )
)
kb_onboarding_step_1.row(
    types.InlineKeyboardButton(
        text="Пропустить знакомство",
        callback_data="start_forecast"
    )
)

# ----------------------------------------------------------------------------------------------------------------------

# --- Шаг 2: Темы для обсуждения ---
kb_onboarding_step_2 = InlineKeyboardBuilder()
kb_onboarding_step_2.row(
    types.InlineKeyboardButton(
        text="По каким методикам ты работаешь?",
        callback_data="onboarding_step_3"
    )
)
kb_onboarding_step_2.row(
    types.InlineKeyboardButton(
        text="Пропустить",
        callback_data="start_forecast"
    )
)

# ----------------------------------------------------------------------------------------------------------------------

# --- Шаг 3: Методики ---
kb_onboarding_step_3 = InlineKeyboardBuilder()
kb_onboarding_step_3.row(
    types.InlineKeyboardButton(
        text="А откуда ты всё это знаешь?",
        callback_data="onboarding_step_4"
    )
)
kb_onboarding_step_3.row(
    types.InlineKeyboardButton(
        text="Пропустить",
        callback_data="start_forecast"
    )
)

# ----------------------------------------------------------------------------------------------------------------------

# --- Шаг 4: База знаний ---
kb_onboarding_step_4 = InlineKeyboardBuilder()
kb_onboarding_step_4.row(
    types.InlineKeyboardButton(
        text="Есть ситуации с которыми ты не работаешь?",
        callback_data="onboarding_step_5"
    )
)
kb_onboarding_step_4.row(
    types.InlineKeyboardButton(
        text="Пропустить",
        callback_data="start_forecast"
    )
)

# ----------------------------------------------------------------------------------------------------------------------

# --- Шаг 5: Ограничения ---
kb_onboarding_step_5 = InlineKeyboardBuilder()
kb_onboarding_step_5.row(
    types.InlineKeyboardButton(
        text="Моя информация в безопасности?",
        callback_data="onboarding_step_6"
    )
)
kb_onboarding_step_5.row(
    types.InlineKeyboardButton(
        text="Пропустить",
        callback_data="start_forecast"
    )
)

# ----------------------------------------------------------------------------------------------------------------------

# --- Шаг 6: Конфиденциальность ---
kb_onboarding_step_6 = InlineKeyboardBuilder()
kb_onboarding_step_6.row(
    types.InlineKeyboardButton(
        text="Принято!",
        callback_data="onboarding_step_7"
    )
)

# ----------------------------------------------------------------------------------------------------------------------

# --- Шаг 7: Обратная связь ---
kb_onboarding_step_7 = InlineKeyboardBuilder()
kb_onboarding_step_7.row(
    types.InlineKeyboardButton(
        text="Приступить к прогнозу",
        callback_data="start_forecast"
    )
)
