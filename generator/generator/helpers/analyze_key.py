import librosa
from generator.helpers.keyfinder import Tonal_Fragment


def analyze_key(audio_file):
    try:
        y, sr = librosa.load(audio_file)
        y_harmonic, y_percussive = librosa.effects.hpss(y)

        unebarque_fsharp_maj = Tonal_Fragment(y_harmonic, sr, tend=22)
        keyfinder_result = unebarque_fsharp_maj.print_key_simple()
        key, lad = keyfinder_result.split(' ')

        return key, lad

    except Exception as e:
        print(e)
        return None, None
