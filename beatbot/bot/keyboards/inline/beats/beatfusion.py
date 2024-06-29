from typing import Final
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..navigate import BTN_GO_BACK, BTN_GO_MENU
from ..buttons.empty import BTN_EMPTY

STYLES: Final = {
    'beatfusion': (
        ('BB', 'Traap', (120, 180)),
        ('DrAOIAill', 'Driill', (120, 180)),
        ('Joooersey Club', 'JCC', (130, 170)),
    )
}


async def styles_markup(model: str = 'beatfusion'):
    keyboard = InlineKeyboardBuilder()

    model = STYLES['beatfusion']

    for style in model:
        keyboard.button(text=style[0], callback_data=f'{style[1]}:{style[2][0]}:{style[2][1]}')

    return keyboard.adjust(2).as_markup()


async def bpm_markup(current_bpm: int):
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='Подтвердить', callback_data=f'submit:{current_bpm}'))
    keyboard.row(*[InlineKeyboardButton(text=offset, callback_data=f'bpm:{current_bpm}:{offset}') for offset in
                   ['-10', '-5', '-1', '+1', '+5', '+10']])
    keyboard.row(BTN_GO_MENU)

    return keyboard.as_markup()


MAIN_INSTRUMENTS = ['Piano', 'Aguitar', 'Eguitar']


async def main_instruments_markup(model: str = 'beatfusion'):
    keyboard = InlineKeyboardBuilder()

    for instrument in MAIN_INSTRUMENTS:
        keyboard.button(text=instrument, callback_data=f'instrument:{instrument}')

    keyboard.row(BTN_GO_MENU)
    return keyboard.adjust(3).as_markup()


BTN_LAD_MINOR: Final = InlineKeyboardButton(text='Minor', callback_data='lad:minor')
BTN_LAD_MAJOR: Final = InlineKeyboardButton(text='Major', callback_data='lad:major')

KB_LAD: Final = InlineKeyboardMarkup(inline_keyboard=[
    [BTN_LAD_MINOR, BTN_LAD_MAJOR],
    [BTN_GO_MENU]
])

TONALITIES: Final = ['C', 'C#',
                     'D', 'D#',
                     'E',
                     'F', 'F#',
                     'G', 'G#',
                     'A', 'A#',
                     'B'
                     ]

tonality_buttons = [InlineKeyboardButton(text=tonality, callback_data=f'tonality:{tonality}') for tonality in
                    TONALITIES]
rows = [tonality_buttons[i:i + 4] for i in range(0, len(tonality_buttons), 4)]

rows.append([BTN_GO_MENU])

KB_TONALITIES = InlineKeyboardMarkup(inline_keyboard=rows)


BTN_EXT_MP3: Final = InlineKeyboardButton(text='.mp3', callback_data='ext:mp3')
BTN_EXT_WAV: Final = InlineKeyboardButton(text='.wav', callback_data='ext:wav')

KB_EXT: Final = InlineKeyboardMarkup(inline_keyboard=[
    [BTN_EXT_MP3, BTN_EXT_WAV],
    [BTN_GO_MENU]
])
