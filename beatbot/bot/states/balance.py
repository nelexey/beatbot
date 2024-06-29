from aiogram.fsm.state import StatesGroup, State

class FillBalance(StatesGroup):
    amount = State()
