import librosa
from utils.keyfinder import Tonal_Fragment

class Audio_Analyzer():
    # Определить тональность и лад
    @staticmethod
    def analyze_key(audio_file):
        try:
            y, sr = librosa.load(audio_file)
            y_harmonic, y_percussive = librosa.effects.hpss(y)

            unebarque_fsharp_maj = Tonal_Fragment(y_harmonic, sr, tend=22)
            keyfinder_result = unebarque_fsharp_maj.print_key_simple()
            key, harmony = keyfinder_result.split(' ')

            return key, harmony
        
        except Exception as e:
            print(e)
            return None, None