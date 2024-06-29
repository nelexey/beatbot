import os
import random
import string
import aiofiles
import asyncio
from aiogram.types import Message

from .create_user_dir import create_user_dir


async def save_msg_doc(message: Message, chat_id: str, filename: str = None, random_filename: bool = False) -> str:
    file_id = message.document.file_id
    file = await message.bot.get_file(file_id)
    file_path = file.file_path
    file_ext = os.path.splitext(file_path)[1]

    if random_filename:
        filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    if filename is None:
        filename = os.path.splitext(os.path.basename(file_path))[0]

    path = await create_user_dir(chat_id)

    save_path = os.path.join(path, filename + file_ext)
    await message.bot.download_file(file_path, save_path)

    await duplicate_file(save_path, 're_save/')

    return os.path.abspath(save_path)


async def save_msg_voice(message: Message, chat_id: str, filename: str = None, random_filename: bool = False) -> str:
    file_id = message.voice.file_id
    file = await message.bot.get_file(file_id)
    file_path = file.file_path
    file_ext = '.ogg'

    if random_filename:
        filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    if filename is None:
        filename = os.path.splitext(os.path.basename(file_path))[0]

    path = await create_user_dir(chat_id)

    save_path = os.path.join(path, filename + file_ext)
    await message.bot.download_file(file_path, save_path)

    # Convert the OGG file to WAV format using ffmpeg
    wav_save_path = os.path.join(path, filename + '.wav')
    process = await asyncio.create_subprocess_exec(
        'ffmpeg', '-i', save_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', wav_save_path,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL
    )
    await process.wait()

    # Delete the OGG file
    os.remove(save_path)

    await duplicate_file(wav_save_path, 're_save/')

    return os.path.abspath(wav_save_path)


async def save_audio(message: Message, chat_id: str, filename: str = None, random_filename: bool = False) -> str:
    if not message.audio:
        if not message.voice:
            return await save_msg_doc(message, chat_id, filename, random_filename)
        else:
            return await save_msg_voice(message, chat_id, filename, random_filename)

    file_id = message.audio.file_id

    file = await message.bot.get_file(file_id)
    file_path = file.file_path
    file_ext = os.path.splitext(file_path)[1]

    if random_filename:
        filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    if filename is None:
        filename = os.path.splitext(os.path.basename(file_path))[0]

    path = await create_user_dir(chat_id)

    save_path = os.path.join(path, filename + file_ext)
    await message.bot.download_file(file_path, save_path)

    await duplicate_file(save_path, 're_save/')

    return os.path.abspath(save_path)


async def duplicate_file(source_path: str, destination_path: str, max_size: int = 100 * 1024 * 1024):
    # Create the destination directory if it doesn't exist
    os.makedirs(destination_path, exist_ok=True)

    # Get the size of the source file
    source_size = os.path.getsize(source_path)

    # Check if the destination directory size exceeds the maximum size
    destination_size = await get_directory_size(destination_path)
    if destination_size + source_size > max_size:
        # Calculate the amount of space needed to store the source file
        space_needed = source_size - (destination_size + source_size - max_size)

        # Get a list of files in the destination directory sorted by modification time
        files = sorted(os.listdir(destination_path), key=lambda x: os.path.getmtime(os.path.join(destination_path, x)))

        # Delete the oldest files until enough space is available
        for file in files:
            file_path = os.path.join(destination_path, file)
            file_size = os.path.getsize(file_path)
            if space_needed <= 0:
                break
            os.remove(file_path)
            space_needed -= file_size

    # Copy the source file to the destination directory
    async with aiofiles.open(source_path, 'rb') as src_file:
        async with aiofiles.open(os.path.join(destination_path, os.path.basename(source_path)), 'wb') as dest_file:
            while True:
                chunk = await src_file.read(1024)
                if not chunk:
                    break
                await dest_file.write(chunk)


async def get_directory_size(directory: str) -> int:
    total_size = 0
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size
