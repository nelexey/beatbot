from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import Router, F

from bot.middlewares import UserDataMiddleware
from bot.keyboards import KB_ABOUT_US, KB_MENU, KB_BALANCE, KB_GENERATION
from bot.database.methods.get import get_user
from bot.misc.messages import MENU_MESSAGE_TEXT, ABOUT_MESSAGE_TEXT

menu_router = Router()

menu_router.callback_query.outer_middleware(UserDataMiddleware())


@menu_router.callback_query(F.data == 'menu:generation')
async def generation_menu(c: CallbackQuery):
    await c.message.edit_text('Выберите модель генерации', reply_markup=KB_GENERATION)


@menu_router.callback_query(F.data == 'menu:balance')
async def balance_menu(c: CallbackQuery):
    user = get_user(c.message.chat.id)
    if user:
        await c.message.edit_text(f'Ваш баланс: {user.balance}', reply_markup=KB_BALANCE)


@menu_router.callback_query(F.data == 'nav:menu')
async def return_to_menu(c: CallbackQuery,
                         state: FSMContext):
    await state.clear()
    user = get_user(c.message.chat.id)
    if user:
        await c.message.edit_text(MENU_MESSAGE_TEXT, reply_markup=KB_MENU)


@menu_router.callback_query(F.data == 'menu:about_us')
async def about_menu(c: CallbackQuery):
    user = get_user(c.message.chat.id)
    if user:
        await c.message.edit_text(ABOUT_MESSAGE_TEXT, reply_markup=KB_ABOUT_US)

# free_options_menu отдельно в файле options.py
