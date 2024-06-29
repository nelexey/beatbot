from typing import Final
from aiogram.types import InlineKeyboardButton

BTN_GO_BACK: Final = InlineKeyboardButton(text='Назад', callback_data='nav:menu')
BTN_GO_MENU: Final = InlineKeyboardButton(text='В меню', callback_data='nav:menu')
