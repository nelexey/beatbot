from pydub import AudioSegment

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