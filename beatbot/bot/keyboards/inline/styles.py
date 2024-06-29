from typing import Final
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .buttons.nav import BTN_GO_BACK

BTN_MODEL_V1: Final = InlineKeyboardButton(text='Platinum v2.0', callback_data='generation:platinum')
BTN_MODEL_V2: Final = InlineKeyboardButton(text='BeatFusion v1.0', callback_data='generation:beatfusion')

generation_markup = [
    [BTN_MODEL_V1],
    [BTN_MODEL_V2],
    [BTN_GO_BACK]
    ]