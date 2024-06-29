from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from bot.database.methods.create import create_user
from bot.database.methods.get import get_user
from bot.keyboards import KB_MENU
from bot.misc.messages import MENU_MESSAGE_TEXT, START_MESSAGE_TEXT

commands_router = Router()


@commands_router.message(CommandStart())
async def start(msg: Message):
    create_user(msg.from_user.username,
                msg.from_user.first_name,
                msg.from_user.last_name,
                msg.chat.id)

    await msg.answer(START_MESSAGE_TEXT, parse_mode='html')
    await msg.delete()


@commands_router.message(Command('menu'))
async def menu(msg: Message):
    await msg.answer(MENU_MESSAGE_TEXT, parse_mode='html', reply_markup=KB_MENU)
    await msg.delete()
