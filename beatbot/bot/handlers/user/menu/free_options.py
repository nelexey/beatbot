from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot.middlewares import UserDataMiddleware
from bot.keyboards.inline import KB_FREE_OPTIONS

free_options_router = Router()

free_options_router.callback_query.outer_middleware(UserDataMiddleware())
free_options_router.message.outer_middleware(UserDataMiddleware())


@free_options_router.callback_query(F.data == 'menu:options')
async def free_options_menu(c: CallbackQuery,
                            state: FSMContext,
                            user):
    await c.message.edit_text('Выберите бесплатную опцию', reply_markup=KB_FREE_OPTIONS)
