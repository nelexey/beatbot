from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from asyncio import sleep

from bot.misc.messages import MENU_MESSAGE_TEXT
from bot.keyboards.inline import KB_MENU

other_router = Router()


@other_router.message()
async def please_use_commands(msg: Message):
    await msg.answer('Для взаимодействия используйте команды', reply_markup=ReplyKeyboardRemove())


@other_router.callback_query(F.data == 'empty')
async def inline_empty(c: CallbackQuery):
    await c.message.answer('Здесь ничего нет', show_alert=True)


@other_router.callback_query(F.data == 'nav:end')
async def end_and_go_menu(c: CallbackQuery,
                          state: FSMContext):
    m = await c.message.answer('Заканчиваю...', reply_markup=ReplyKeyboardRemove())
    await state.clear()
    await sleep(2)
    await m.delete()
    return await c.message.answer(MENU_MESSAGE_TEXT, reply_markup=KB_MENU)
