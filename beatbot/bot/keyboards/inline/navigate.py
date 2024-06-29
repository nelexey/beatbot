from typing import Final
from aiogram.types import InlineKeyboardButton

BTN_GO_BACK: Final = InlineKeyboardButton(text='Назад', callback_data='nav:menu')
BTN_GO_MENU: Final = InlineKeyboardButton(text='В меню', callback_data='nav:menu')
BTN_GO_FREE_OPTIONS: Final = InlineKeyboardButton(text='К Бесплатным опциям', callback_data='menu:options')
BTN_END: Final = InlineKeyboardButton(text='⬅️ Закончить', callback_data='nav:end')
