from typing import Final
from aiogram.types import callback_query
from aiogram.types import InlineKeyboardButton

BTN_BALANCE: Final = InlineKeyboardButton(text='Баланс', callback_data='menu:balance')
BTN_ABOUT_US: Final = InlineKeyboardButton(text='О нас', callback_data='menu:about_us')
BTN_GENERATION: Final = InlineKeyboardButton(text='Генерация', callback_data='menu:generation')
BTN_FREE_OPTIONS: Final = InlineKeyboardButton(text='Бесплатные опции', callback_data='menu:options')

menu_markup = [
    [BTN_BALANCE, BTN_ABOUT_US],
    [BTN_GENERATION],
    [BTN_FREE_OPTIONS],
]
