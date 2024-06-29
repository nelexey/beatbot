from typing import Final
from aiogram.types import InlineKeyboardMarkup

from bot.keyboards.inline.navigate import BTN_GO_MENU, BTN_GO_FREE_OPTIONS, BTN_END

from .menu import menu_markup
from .balance import balance_markup
from .about_us import about_us_markup
from .styles import generation_markup
from .options.free_options_menu import free_options_markup
from .options.midi_to_wav import midi_to_wav_markup

KB_MENU: Final = InlineKeyboardMarkup(inline_keyboard=menu_markup)
KB_BALANCE: Final = InlineKeyboardMarkup(inline_keyboard=balance_markup)
KB_ABOUT_US: Final = InlineKeyboardMarkup(inline_keyboard=about_us_markup)
KB_GENERATION: Final = InlineKeyboardMarkup(inline_keyboard=generation_markup)
KB_FREE_OPTIONS: Final = InlineKeyboardMarkup(inline_keyboard=free_options_markup)
KB_GO_MENU: Final = InlineKeyboardMarkup(inline_keyboard=[[BTN_GO_MENU]])
KB_GO_FREE_OPTIONS: Final = InlineKeyboardMarkup(inline_keyboard=[[BTN_GO_FREE_OPTIONS]])
KB_MIDI_TO_WAV: Final = InlineKeyboardMarkup(inline_keyboard=midi_to_wav_markup)
KB_END: Final = InlineKeyboardMarkup(inline_keyboard=[[BTN_END]])