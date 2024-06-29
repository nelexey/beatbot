from typing import Final
from aiogram.types import callback_query
from aiogram.types import InlineKeyboardButton

from ..buttons.nav import BTN_GO_BACK

BTN_SPEED_UP: Final = InlineKeyboardButton(text='Speed UP', callback_data='options:speed_up')
BTN_SLOW_DOWN: Final = InlineKeyboardButton(text='Slowed', callback_data='options:slow_down')
BTN_MIDI_TO_WAV: Final = InlineKeyboardButton(text='Музыка из своих звуков', callback_data='options:midi_to_wav')
BTN_REMOVE_VOCAL: Final = InlineKeyboardButton(text='Remove Vocal', callback_data='options:remove_vocal')
BTN_RHYMES: Final = InlineKeyboardButton(text='Подобрать рифму', callback_data='options:rhymes')
BTN_FIND_KEY: Final = InlineKeyboardButton(text='Опр. тональность', callback_data='options:find_key')
BTN_FIND_TEMPO: Final = InlineKeyboardButton(text='Опр. темп', callback_data='options:find_tempo')
BTN_NORMALIZE_SOUND: Final = InlineKeyboardButton(text='Улучшение звука', callback_data='options:normalize_sound')
BTN_BASSBOOST: Final = InlineKeyboardButton(text='BASSBOOST', callback_data='options:bassboost')

free_options_markup = [
    [BTN_SPEED_UP, BTN_SLOW_DOWN],
    [BTN_MIDI_TO_WAV],
    [BTN_REMOVE_VOCAL],
    [BTN_RHYMES],
    [BTN_FIND_KEY, BTN_FIND_TEMPO],
    [BTN_NORMALIZE_SOUND, BTN_BASSBOOST],
    [BTN_GO_BACK]
]
