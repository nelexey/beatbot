import os
import asyncio
from pydub import AudioSegment

from generator.helpers import generate_random_filename, delete_file


def normalize_sound(data):
    file_path = data['file_path']
    format = os.path.splitext(file_path)[1].lower()[1:]

    audio = AudioSegment.from_file(file_path, format=format)

    new_file_path = os.path.join(os.path.dirname(file_path),
                                 f"{generate_random_filename()}.{format}")

    audio.export(new_file_path, format='wav')

    asyncio.run(delete_file(file_path))

    return {'file_path': new_file_path}
