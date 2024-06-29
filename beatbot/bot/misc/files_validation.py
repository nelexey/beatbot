from aiogram.types import Message


async def validate_msg_file(message: Message, size: int) -> bool:
    """
    :param message: aiogram.types.Message
    :param size: valid message file size limit in Mb
    :return: bool
    """

    file = message.audio or message.document or message.voice

    if file.file_size > size * 1024 * 1024:
        return False
    return True
