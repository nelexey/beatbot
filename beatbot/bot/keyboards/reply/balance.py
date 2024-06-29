from typing import Final
from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardBuilder

beatv1 = 249
beatv2 = 199
sub = 89

prices = [199, 199*2, 199*3, 249, 249*2, 249*3, 89]

async def reply_pricing():
    keyboard = ReplyKeyboardBuilder()
    for price in prices:
        keyboard.add(KeyboardButton(text=str(price)))
    keyboard.adjust(3)
    return keyboard.as_markup(resize_keyboard=True)
