from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot.middlewares import UserDataMiddleware
from bot.keyboards.reply.balance import reply_pricing
from bot.states.balance import FillBalance
from bot.services import create_payment
from bot.database.methods.update import update_user
from bot.misc import RELOAD_MESSAGE_TEXT, BALANCE_FILL_MESSAGE, ALERT_FILL_BALANCE

balance_router = Router()

balance_router.callback_query.outer_middleware(UserDataMiddleware())
balance_router.message.outer_middleware(UserDataMiddleware())


@balance_router.callback_query(F.data == 'balance:fill')
async def fill_balance(c: CallbackQuery,
                       state: FSMContext,
                       user):
    await state.set_state(FillBalance.amount)
    await c.message.answer(BALANCE_FILL_MESSAGE, reply_markup=await reply_pricing())


@balance_router.message(FillBalance.amount)
async def enter_balance(msg: Message,
                        state: FSMContext,
                        user):
    """
    Проверить существование пользователя.

    Валидировать введённые данные и создать ссылку на оплату.
    """

    amount = int(msg.text)

    if 10 < amount < 1_000_000:
        await state.update_data(name=amount)
        await state.clear()

        if payment := await create_payment(user.chat_id, amount):
            confirmation_url = payment['confirmation']['confirmation_url']
            await msg.answer(text=f'Перейдите по ссылке для оплаты: {confirmation_url}')
        else:
            await msg.answer(text=f'Ошибка оплаты')
        # update_user(chat_id=user.chat_id, balance=user.balance + amount)
    else:
        await msg.answer(text=ALERT_FILL_BALANCE)

    await msg.delete()
