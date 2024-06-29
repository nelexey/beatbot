from typing import Final
from aiogram.types import InlineKeyboardButton

from .navigate import BTN_GO_BACK

BTN_FILL_BALANCE: Final = InlineKeyboardButton(text='Пополнить баланс', callback_data='balance:fill')

balance_markup = [
    [BTN_FILL_BALANCE],
    [BTN_GO_BACK]
    ]
