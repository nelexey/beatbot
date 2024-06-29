import librosa
import asyncio

from generator.helpers import delete_file


def find_tempo(data):
    file_path = data['file_path']
    try:
        y, sr = librosa.load(file_path)

        # Определение BPM
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        return {'tempo': tempo[0]}

    except Exception as e:
        print(e)
        return {'tempo': None}

    finally:
        asyncio.run(delete_file(file_path))
