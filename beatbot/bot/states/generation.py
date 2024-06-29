from aiogram.fsm.state import StatesGroup, State


class Platinum(StatesGroup):
    style = State()
    min_bpm = State()
    max_bpm = State()
    bpm = State()
    lad = State()
    ext = State()


class Beatfusion(StatesGroup):
    style = State()
    min_bpm = State()
    max_bpm = State()
    bpm = State()
    lad = State()
    tonality = State()
    main_instrument = State()
    ext = State()
