import librosa
from utils.keyfinder import Tonal_Fragment
from pydub import AudioSegment
from pydub.silence import split_on_silence
from os import path
import mido

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

    # Обрезать аудио на демо-версии в формате mp3 и сохранить.
    @staticmethod
    def crop_audio(input_path, duration_seconds):
        # Загрузите аудиофайл
        audio = AudioSegment.from_file(input_path)
        
        # Определите сколько миллисекунд нужно обрезать
        crop_duration = duration_seconds * 1000
        
        # Обрежьте аудиофайл
        cropped_audio = audio[:crop_duration]
        
        # Получите имя файла и путь из исходного пути
        file_name = path.basename(input_path)
        file_path = path.dirname(input_path)
        
        # Сгенерируйте путь для сохранения обрезанного файла
        output_path = path.join(file_path, f"{file_name}")
        
        # Сохраните обрезанный файл по новому пути
        cropped_audio.export(output_path, format=input_path.split('.')[-1])

    # Обрезать аудио на демо-версии в формате mp3 и сохранить.
    @staticmethod
    def cut_from_start(file_path):
        sound = AudioSegment.from_file(file_path)
        trimmed = sound[35000:50000]
        new_file_path = f"{path.splitext(file_path)[0]}_short.mp3"
        trimmed.export(new_file_path, format=f"mp3")

    @staticmethod
    def get_midi_length(file):
        try:
            mid = mido.MidiFile(file)
            
            # Получаем длину в тиках
            ticks = mid.length
            
            # Получаем длину в миллисекундах (предполагая стандартное разрешение тика 480)
            milliseconds = mido.second2tick(mid.length, mid.ticks_per_beat, 500000)  # 500000 микросекунд в секунде
            
            return milliseconds
        except Exception as e:
            print(e)
            return False
    
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
    
    @staticmethod
    def remove_start_silence(audio, silence_thresh = -40):
        try:
            # Найдите индекс первого сегмента, не являющегося тишиной
            start_idx = next((i for i, seg in enumerate(audio) if seg.dBFS > silence_thresh), None)

            if start_idx is not None:
                # Обрежьте тишину в начале аудио
                audio_trimmed = audio[start_idx:]
                print('Silence deleted.')
                return audio_trimmed
            else:
                print('No silence found.')
        except Exception as e:
            print('Unable to delete silence from audio. Returning same audio...')
            return audio