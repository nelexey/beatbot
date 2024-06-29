from aiogram.fsm.state import StatesGroup, State


class Speed_Up(StatesGroup):
    audio = State()
    format = State()


class Slow_Down(StatesGroup):
    audio = State()
    format = State()


class Midi_To_Wav(StatesGroup):
    midi_msg_id = State()
    sound_msg_id = State()
    midi = State()
    sound = State()
    sound_format = State()


class Remove_Vocal(StatesGroup):
    audio = State()
    format = State()


class Rhymes(StatesGroup):
    text = State()


class Find_Key(StatesGroup):
    audio = State()
    format = State()


class Find_Tempo(StatesGroup):
    audio = State()
    format = State()


class Normalize_Sound(StatesGroup):
    audio = State()
    format = State()


class Bassboost(StatesGroup):
    audio = State()
    format = State()
