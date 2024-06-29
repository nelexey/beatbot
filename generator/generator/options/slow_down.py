import os
import asyncio
from pydub import AudioSegment

from generator.helpers import generate_random_filename, delete_file


def slow_down(data):
    file_path = data['file_path']
    format = os.path.splitext(file_path)[1].lower()[1:]

    audio = AudioSegment.from_file(file_path, format=format)

    octaves = -0.3

    new_sample_rate = int(audio.frame_rate * (2.0 ** octaves))

    slow_down_audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_sample_rate})

    new_file_path = os.path.join(os.path.dirname(file_path),
                                 f"{generate_random_filename()}.{format}")

    slow_down_audio.export(new_file_path, format=format)

    asyncio.run(delete_file(file_path))

    return {'file_path': new_file_path}
