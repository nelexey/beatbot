import os
import json
import aiofiles
import aiofiles.os
from aiohttp import web
from aiogram import Bot
from aiogram.types import BufferedInputFile, ReplyKeyboardMarkup
from aiogram.methods import DeleteMessage

from bot.database.methods.update import remove_user_options_credit, update_user_statistic
from bot.database.methods.get import get_user
from bot.keyboards.inline.beats import build_versions_keyboard
from bot.misc import create_user_dir


async def handle_send_beat(request, bot: Bot):
    data = await request.json()

    chat_id = data['chat_id']
    model = data['model']
    session_dir = data['session_directory'].split('/')[-2]
    beats = data['result']['paths']['beat']
    shorts = data['result']['paths']['short']

    print(session_dir)

    messages_ids = list()

    last = list(shorts.keys())[-1]
    for i in shorts.keys():
        async with aiofiles.open(shorts[i], 'rb') as audio_file:
            file = BufferedInputFile(await audio_file.read(), filename=shorts[i])
            title = f'version {i} | tg:@NeuralBeatBot'

            if i == last:
                msg = await bot.send_audio(chat_id,
                                           audio=file,
                                           title=title,
                                           reply_markup=build_versions_keyboard(beats, model, session_dir))
            else:
                msg = await bot.send_audio(chat_id,
                                           audio=file,
                                           title=title)

            messages_ids.append(msg.message_id)

    session = f'{await create_user_dir(chat_id)}/{session_dir}/session.json'
    with open(session, 'w') as f:
        json.dump({'messages_ids': messages_ids}, f)

    return web.Response()
