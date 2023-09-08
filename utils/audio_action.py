import librosa
from utils.keyfinder import Tonal_Fragment
from pydub import AudioSegment
from os import path
import numpy as np

class Audio_Action():

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

    # Обрезать аудио на демо-версии в формате mp3 и сохранить.
    @staticmethod
    def trimmed_audio(file_path):
        sound = AudioSegment.from_file(file_path)
        trimmed = sound[35000:50000]
        new_file_path = f"{path.splitext(file_path)[0]}_short.mp3"
        trimmed.export(new_file_path, format=f"mp3")
    
    # Изменить темп аудио
    @staticmethod
    def change_bpm(sound, speed=1.0):
        # Установка частоты кадров вручную. Это говорит компьютеру, сколько
        # образцов воспроизводить в секунду
        sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * speed)
        })

        # Преобразование звука с измененной частотой кадров в стандартную частоту кадров,
        # чтобы обычные программы воспроизведения работали правильно. Они часто умеют
        # воспроизводить звук только на стандартной частоте кадров (например, 44,1 кГц)
        return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

    # Применение клиппера к оверлею
    @staticmethod
    def apply_clipper(x, threshold):
        #TODO

        # if isinstance(x, AudioSegment):
        #     # Преобразование AudioSegment в массив NumPy
        #     x = np.array(x.get_array_of_samples(), dtype=np.float64)
        
        # # Применение клиппера к массиву NumPy
        # x = np.clip(x, -threshold, threshold) - (x - np.clip(x, -1, 1)) * threshold
        
        # if isinstance(x, np.ndarray):
        #     # Преобразование обратно в AudioSegment
        #     x = AudioSegment(x.tobytes(), frame_rate=44100, sample_width=x.dtype.itemsize, channels=1)
        return x