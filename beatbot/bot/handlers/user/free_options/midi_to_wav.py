import asyncio

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from asyncio.exceptions import TimeoutError

from bot.states.free_option import Midi_To_Wav
from bot.keyboards.inline import KB_MIDI_TO_WAV
from bot.misc.messages import MIDI_TO_WAV_MESSAGE
from bot.misc.free_options_settings import is_supported_format
from bot.misc import save_audio, save_msg_doc, SubChecker, validate_msg_file, get_msg_doc_format
from bot.web.requests.Service import free_option_req

midi_to_wav_router = Router()


@midi_to_wav_router.callback_query(F.data == 'options:midi_to_wav')
async def midi_to_wav(c: CallbackQuery,
                      state: FSMContext,
                      user):
    if not await SubChecker.is_member(c.message.chat.id):
        return await c.message.reply('Бесплатные опции доступны только подписчикам @beatbotnews')

    await state.set_state(Midi_To_Wav.midi)
    await c.message.edit_text(MIDI_TO_WAV_MESSAGE, reply_markup=KB_MIDI_TO_WAV)


@midi_to_wav_router.message(Midi_To_Wav.midi)
async def get_audio(message: Message,
                    state: FSMContext,
                    user):
    if is_supported_format(message, 'midi_to_wav'):

        f_size = 5  # MB
        if not await validate_msg_file(message, f_size):
            return message.answer(f'🔊 Файл слишком большой. Пожалуйста, загрузите файл размером до {f_size}мб.')

        if await get_msg_doc_format(message) == 'mid':
            await state.update_data(midi_msg_id=message)
        else:
            await state.update_data(sound_msg_id=message)

        data = await state.get_data()

        if 'midi_msg_id' in data and \
                'sound_msg_id' in data:

            try:
                midi_path = await save_msg_doc(data['midi_msg_id'], str(message.chat.id), random_filename=True)
                sound_path = await save_audio(data['sound_msg_id'], str(message.chat.id), random_filename=True)

                await free_option_req('midi_to_wav', message.chat.id, sound_path, data={'midi': midi_path})

            except TimeoutError:
                await message.reply('Не удалось сохранить отправленные файлы')
                await asyncio.sleep(4)

            await state.clear()
    else:
        await message.answer('Неподдерживаемый формат')
        await message.delete()
