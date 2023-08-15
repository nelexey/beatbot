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