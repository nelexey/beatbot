from pydub import AudioSegment
from keyfinder import Tonal_Fragment
import librosa

import numpy as np
import math

class sound_options:

    @staticmethod
    def speed_up(audio, user_dir):
        # Ускоряем аудио
        audio = AudioSegment.from_mp3(f'{user_dir}/sound.mp3')
        octaves = 0.3
        new_sample_rate = int(audio.frame_rate * (2.0 ** octaves))
        speed_up_audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_sample_rate})

        speed_up_audio.export(f'{user_dir}/sound.mp3', format="mp3")

    @staticmethod
    def slow_down(audio, user_dir):
        # Замедляем аудио
        audio = AudioSegment.from_mp3(f'{user_dir}/sound.mp3')
        octaves = -0.3
        new_sample_rate = int(audio.frame_rate * (2.0 ** octaves))
        speed_up_audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_sample_rate})

        speed_up_audio.export(f'{user_dir}/sound.mp3', format="mp3")

    @staticmethod
    def normalize_sound(file, user_dir):
        # Нормализуем аудио
        audio = AudioSegment.from_file(f'{user_dir}/{file}')
  
        normalized_sound = audio.apply_gain(0)

        # Сохранение результата
        normalized_sound.export(f'{user_dir}/sound.wav', format="wav")

    def analyze_key(path_to_file):
        try:
            y, sr = librosa.load(path_to_file)
            y_harmonic, y_percussive = librosa.effects.hpss(y)

            unebarque_fsharp_maj = Tonal_Fragment(y_harmonic, sr, tend=22)

            return unebarque_fsharp_maj.print_key_str()
        
        except Exception as e:
            print(e)
            return None, None, None, None
    
    def analyze_bpm(path_to_file):
        y, sr = librosa.load(path_to_file)

        # Определение BPM
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        return tempo
    
    def bass_boost(file, user_dir):

        attenuate_db = 0
        accentuate_db = 13

        # Загрузите аудиофайл
        audio = AudioSegment.from_file(f'{user_dir}/{file}')

        filtered = audio.low_pass_filter(50)

        combined = (audio - attenuate_db).overlay(filtered + accentuate_db)

        combined.export(f'{user_dir}/{file}', format=f"{file.split('.')[-1]}")
