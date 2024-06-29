# from typing import Final
# from aiogram.types import InlineKeyboardButton
# from .keyboards.inline.kb import KB_MENU

# # Глобальные константы для кнопок
# UNDO_BUTTON = InlineKeyboardButton("Назад", callback_data='go_back')
# NATIVE_BUTTON = InlineKeyboardButton("Platinum v2", callback_data='gen1')
# BEATFUSION_BUTTON = InlineKeyboardButton("BeatFusion v1", callback_data='gen2')

# # Создание клавиатур

# KB_BALANCE: Final = InlineKeyboardMarkup()
# KB_MODELS: Final = InlineKeyboardMarkup()

# KB_ABOUT: Final = InlineKeyboardMarkup()

# KB_ABOUT.row(UNDO_BUTTON)

# KB_BALANCE.row(InlineKeyboardButton("Пополнить", callback_data='fill_balance'))
# KB_BALANCE.row(InlineKeyboardButton("Безлимит на месяц", callback_data='enable_subscription'))
# KB_BALANCE.row(UNDO_BUTTON)

# KB_MODELS.row(BEATFUSION_BUTTON)
# KB_MODELS.row(NATIVE_BUTTON)
# KB_MODELS.row(UNDO_BUTTON)
