from typing import Final
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..navigate import BTN_GO_BACK, BTN_GO_MENU
from bot.misc.parameters import STYLES


async def styles_markup(model: str = 'platinum'):
    keyboard = InlineKeyboardBuilder()

    if model not in STYLES:
        return keyboard.as_markup()  # Возвращаем пустую клавиатуру, если модель не найдена

    for style_key, style_info in STYLES[model].items():
        style_name = style_info[0]
        bpm_min, bpm_default, bpm_max = style_info[1]
        keyboard.button(
            text=style_name,
            callback_data=f'{style_key}:{bpm_min}:{bpm_default}:{bpm_max}'
        )
    keyboard.row(BTN_GO_MENU)

    return keyboard.adjust(2).as_markup()


async def bpm_markup(current_bpm: int):
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='Подтвердить', callback_data=f'submit:{current_bpm}'))
    keyboard.row(*[InlineKeyboardButton(text=offset, callback_data=f'bpm:{current_bpm}:{offset}') for offset in
                   ['-10', '-5', '-1', '+1', '+5', '+10']])
    keyboard.row(BTN_GO_MENU)

    return keyboard.as_markup()


BTN_LAD_MINOR: Final = InlineKeyboardButton(text='Minor', callback_data='lad:minor')
BTN_LAD_MAJOR: Final = InlineKeyboardButton(text='Major', callback_data='lad:major')

KB_LAD = InlineKeyboardMarkup(inline_keyboard=[
    [BTN_LAD_MINOR, BTN_LAD_MAJOR],
    [BTN_GO_MENU]
])

BTN_EXT_MP3: Final = InlineKeyboardButton(text='.mp3', callback_data='ext:mp3')
BTN_EXT_WAV: Final = InlineKeyboardButton(text='.wav', callback_data='ext:wav')

KB_EXT = InlineKeyboardMarkup(inline_keyboard=[
    [BTN_EXT_MP3, BTN_EXT_WAV],
    [BTN_GO_MENU]
])
