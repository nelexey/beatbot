from aiogram.types import InlineKeyboardButton

from ..navigate import BTN_GO_FREE_OPTIONS

BTN_LINK_MIDI = InlineKeyboardButton(text="МИДИ", url=f"https://t.me/beatbotnews/58")
BTN_LINK_WAV = InlineKeyboardButton(text="ЗВУКИ", url=f"https://t.me/beatbotnews/67")


midi_to_wav_markup = [
    [BTN_LINK_MIDI, BTN_LINK_WAV],
    [BTN_GO_FREE_OPTIONS],
]