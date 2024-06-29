from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from asyncio import sleep

from bot.states.free_option import Rhymes
from bot.keyboards.inline import KB_GO_FREE_OPTIONS
from bot.misc.messages import RHYMES_MESSAGE
from bot.misc.free_options_settings import is_supported_format
from bot.misc import SubChecker
from bot.web.requests.Service import free_option_req

rhymes_router = Router()


@rhymes_router.callback_query(F.data == 'options:rhymes')
async def rhymes(c: CallbackQuery,
                 state: FSMContext,
                 user):
    if not await SubChecker.is_member(c.message.chat.id):
        return await c.message.reply('Бесплатные опции доступны только подписчикам @beatbotnews')

    await state.set_state(Rhymes.text)
    await c.message.edit_text(RHYMES_MESSAGE, reply_markup=KB_GO_FREE_OPTIONS)


@rhymes_router.message(Rhymes.text)
async def get_audio(message: Message,
                    state: FSMContext,
                    user):

    if is_supported_format(message, 'rhymes'):
        try:
            await free_option_req('rhymes', message.chat.id, data={'text': message.text})
        except:
            await message.answer('⏳ Опция временно не работает')
    else:
        await message.answer('Дання опция принимает только текст')
