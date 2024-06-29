import os
import aiofiles
import json
from aiogram import Router
from aiogram.types import CallbackQuery, BufferedInputFile
from aiogram.methods import DeleteMessage

from bot.middlewares import UserDataMiddleware
from bot.database.methods.update import reduce_user_balance, remove_user_beats_credit
from bot.database.methods.get import get_user_credits
from bot.misc import create_user_dir, delete_files_and_directory, parameters, convert_to_flac

full_version_router = Router()

full_version_router.callback_query.outer_middleware(UserDataMiddleware())


@full_version_router.callback_query(lambda c: c.data.startswith('beat:'))
async def send_full_version(c: CallbackQuery,
                            user):
    chat_id = str(c.message.chat.id)
    data = c.data.split(':')
    file, session_dir, model = data[-1], data[-2], data[-3]
    session_dir = f'{await create_user_dir(chat_id)}/{session_dir}'
    audio_path = f'{session_dir}/{file}'

    user_credits = get_user_credits(int(chat_id))
    if user.balance < parameters.BEAT_PRICE[model] and user_credits.beats < 1:
        return await c.message.answer(
            'На вашем балансе недостаточно средств. Пополните баланс для продолжения работы')

    if not os.path.isdir(session_dir):
        return await c.message.answer('Время действия сессии окончено')

    if os.path.getsize(audio_path) / 1024 / 1024 > 50:
        audio_path = await convert_to_flac(session_dir, file)

    async with aiofiles.open(audio_path, 'rb') as audio_file:

        msg_to_edit = await c.message.answer('отправляю')

        file = BufferedInputFile(await audio_file.read(), filename=file)

        try:
            from bot.main import bot

            title = f'{model} | tg:@NeuralBeatBot'
            await c.message.answer_audio(audio=file, title=title)

            await bot.edit_message_text('отправлено!', message_id=msg_to_edit.message_id, chat_id=chat_id)

            if os.path.splitext(audio_path)[1] == '.flac':
                await c.message.answer('Конвертировано во FLAC')

            with open(f'{session_dir}/session.json', 'r') as f:
                messages_ids = json.load(f)['messages_ids']

                for msg in messages_ids:
                    await bot(DeleteMessage(chat_id=chat_id, message_id=msg))

                if user_credits.beats > 0:
                    remove_user_beats_credit(int(chat_id))
                else:
                    reduce_user_balance(int(chat_id), parameters.BEAT_PRICE[model])
        finally:
            await delete_files_and_directory(f'{session_dir}/')
