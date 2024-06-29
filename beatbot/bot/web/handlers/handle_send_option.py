import os
import aiofiles
import aiofiles.os
from aiohttp import web
from aiogram import Bot
from aiogram.types import BufferedInputFile, ReplyKeyboardMarkup

from bot.keyboards.inline.kb import KB_END
from bot.database.methods.update import remove_user_options_credit, update_user_statistic
from bot.database.methods.get import get_user


async def handle_send_option(request, bot: Bot):
    data = await request.json()
    print(data)
    chat_id = data['chat_id']

    if chat_id is None:
        return web.Response(text="Missing chat_id parameter", status=400)
    try:
        chat_id = int(chat_id)
    except ValueError:
        return web.Response(text="Invalid chat_id parameter", status=400)

    option_name = data['option_name']
    do_remove = True

    try:

        if option_name == 'remove_vocal':
            await send_vocal_remover_result(chat_id, data['result'], bot)
        elif option_name == 'rhymes':
            text = data['result']['text']

            if text is None:
                text = 'Не удалось подобрать рифмы'
                do_remove = False

            await send_text(chat_id, text, bot, reply_markup=KB_END)

        elif option_name == 'find_key':

            result = data['result']
            key = result['key']
            altkey = result['altkey']
            corr = result['corr']
            altcorr = result['altcorr']

            if altkey is not None:
                text = f'<b>{key} - {round(corr * 100, 2)}%></b><br>{altkey} - {round(altcorr * 100, 2)}%'
            elif key is None:
                text = f'😵 Не удалось определить тональность аудиофайла'
                do_remove = False
            else:
                text = f'<b>{key} - {round(corr * 100, 2)}%</b>'

            await send_text(chat_id, text, bot)
        elif option_name == 'find_tempo':

            result = data['result']
            tempo = result['tempo']

            if tempo is not None:
                rounded_bpm = "{:.2f}".format(tempo)
                text = f'<b>{rounded_bpm}bpm</b>'
            else:
                text = f'😵 Не удалось определить темп аудиофайла'
                do_remove = False

            await send_text(chat_id, text, bot)
        else:
            file_path = data['result']['file_path']
            await send_single_sound(chat_id, file_path, option_name, bot)
    except Exception as e:
        await bot.send_message(chat_id, 'Произошла ошибка при обработке')
        print(e)
        do_remove = False

    if do_remove:
        if not get_user(chat_id).has_sub:
            remove_user_options_credit(chat_id)

        update_user_statistic(chat_id, option_name)

    return web.Response()


async def send_single_sound(chat_id: int, file_path: str, option_name: None, bot: Bot):
    async with aiofiles.open(file_path, 'rb') as audio_file:
        input_file = BufferedInputFile(await audio_file.read(), filename=file_path)

        if option_name is not None:
            await bot.send_audio(chat_id, audio=input_file, title=f'{option_name} | tg:@NeuralBeatBot')
        else:
            await bot.send_audio(chat_id, audio=input_file)

    # Delete the file after sending
    await aiofiles.os.remove(file_path)


async def send_vocal_remover_result(chat_id: int, result: dict, bot: Bot):
    async with aiofiles.open(result['vocal_path'], 'rb') as audio_file:
        vocal_file = BufferedInputFile(await audio_file.read(), filename=result['vocal_path'])

        await bot.send_audio(chat_id, audio=vocal_file)

    async with aiofiles.open(result['instrumental_path'], 'rb') as audio_file:
        instrumental_file = BufferedInputFile(await audio_file.read(), filename=result['instrumental_path'])

        await bot.send_audio(chat_id, audio=instrumental_file)

    await aiofiles.os.remove(result['vocal_path'])
    await aiofiles.os.remove(result['instrumental_path'])


async def send_text(chat_id: int, text: str, bot: Bot, file_path=None, option_name=None,
                    reply_markup: ReplyKeyboardMarkup = None):
    if reply_markup:
        await bot.send_message(chat_id, text, reply_markup=reply_markup)
    else:
        await bot.send_message(chat_id, text)
