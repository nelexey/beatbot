import librosa
import asyncio

from generator.helpers.keyfinder import Tonal_Fragment
from generator.helpers import delete_file


def find_key(data):
    file_path = data['file_path']
    try:
        y, sr = librosa.load(file_path)

        y_harmonic, y_percussive = librosa.effects.hpss(y)

        tonal_fragment = Tonal_Fragment(y_harmonic, sr, tend=22)

        result = tonal_fragment.print_key_str()

        return {'key': result[0],
                'corr': result[1],
                'altkey': result[2],
                'altcorr': result[3]}

    except Exception as e:
        print(e)
        return {'key': None,
                'corr': None,
                'altkey': None,
                'altcorr': None}

    finally: asyncio.run(delete_file(file_path))
