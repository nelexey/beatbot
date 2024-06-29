from aiogram.types import Message


async def get_msg_doc_format(message: Message) -> str | None:
    """Determine the format of a message's audio or document.

    Args:
        message (types.Message): The message containing the audio or document.

    Returns:
        str | None: The format of the audio or document, or None if the message doesn't contain an audio or document.
    """
    if message.audio:
        file_id = message.audio.file_id
    elif message.document:
        file_id = message.document.file_id
    else:
        return None

    file = await message.bot.get_file(file_id)
    file_path = file.file_path

    # Get the file extension
    file_extension = file_path.split('.')[-1]

    return file_extension
