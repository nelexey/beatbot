
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot.states.free_option import Normalize_Sound
from bot.keyboards.inline import KB_GO_FREE_OPTIONS
from bot.misc.messages import NORMALIZE_SOUND_MESSAGE
from bot.misc.free_options_settings import is_supported_format
from bot.misc import save_audio, SubChecker, validate_msg_file
from bot.web.requests.Service import free_option_req

normalize_sound_router = Router()


@normalize_sound_router.callback_query(F.data == 'options:normalize_sound')
async def normalize_sound(c: CallbackQuery,
                   state: FSMContext,
                   user):
    if not await SubChecker.is_member(c.message.chat.id):
        return await c.message.reply('Бесплатные опции доступны только подписчикам @beatbotnews')

    await state.set_state(Normalize_Sound.audio)
    await c.message.edit_text(NORMALIZE_SOUND_MESSAGE, reply_markup=KB_GO_FREE_OPTIONS)


@normalize_sound_router.message(Normalize_Sound.audio)
async def get_audio(message: Message,
                    state: FSMContext,
                    user):
    if is_supported_format(message, 'normalize_sound'):
        await state.clear()

        save_path = await save_audio(message, str(message.chat.id), random_filename=True)
        await free_option_req('normalize_sound', message.chat.id, save_path)

    else:
        await message.answer('Неподдерживаемый формат')
        await message.delete()
