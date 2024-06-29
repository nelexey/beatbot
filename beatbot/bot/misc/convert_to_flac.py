import os
from pydub import AudioSegment

async def convert_to_flac(session_dir, file):
    audio_path = f'{session_dir}/{file}'
    flac_path = f'{session_dir}/{os.path.splitext(file)[0]}.flac'

    # Convert audio file to .flac format
    sound = AudioSegment.from_file(audio_path)
    sound.export(flac_path, format="flac")

    return flac_path
