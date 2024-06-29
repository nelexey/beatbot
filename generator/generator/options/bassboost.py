import os
import asyncio
from pydub import AudioSegment
from generator.helpers import generate_random_filename, delete_file


def bassboost(data):
    file_path = data['file_path']
    format = os.path.splitext(file_path)[1].lower()[1:]

    audio = AudioSegment.from_file(file_path, format=format)

    attenuate_db = 0
    accentuate_db = 8
    filtered = audio.low_pass_filter(50)
    combined = (audio - attenuate_db).overlay(filtered + accentuate_db)

    new_file_path = os.path.join(os.path.dirname(file_path),
                                 f"{generate_random_filename()}.{format}")

    combined.export(new_file_path, format=format)

    asyncio.run(delete_file(file_path))

    return {'file_path': new_file_path}
