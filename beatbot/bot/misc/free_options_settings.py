from aiogram.types import Message

options_supported_formats = {
    'speed_up': ['wav', 'mp3', 'ogg'],
    'slow_down': ['wav', 'mp3', 'ogg'],
    'midi_to_wav': ['mid', 'mp3', 'wav', 'ogg'],
    'remove_vocal': ['wav', 'mp3'],
    'rhymes': ['text'],
    'find_key': ['wav', 'mp3', 'ogg'],
    'find_tempo': ['wav', 'mp3', 'ogg'],
    'normalize_sound': ['wav', 'mp3', 'ogg'],
    'bassboost': ['wav', 'mp3', 'ogg']
}


def is_supported_format(message: Message, option: str) -> bool:
    """
    Check if the message contains a supported format for the given option.

    Args:
        message (aiogram.types.Message): The message to check.
        option (str): The name of the option.

    Returns:
        bool: True if the message contains a supported format, False otherwise.
    """
    supported_formats = options_supported_formats.get(option, [])

    if message.audio:
        file_extension = message.audio.mime_type.split('/')[1]

        if file_extension == 'mpeg': file_extension = 'mp3'
        elif file_extension == 'x-wav': file_extension = 'wav'

        return file_extension in supported_formats

    elif message.voice:
        # Voice messages are always sent as OGG files
        return 'ogg' in supported_formats

    elif message.document:
        file_extension = message.document.file_name.split('.')[-1]

        return file_extension in supported_formats

    elif message.text and 'text' in supported_formats:
        return True

    else:
        return False
