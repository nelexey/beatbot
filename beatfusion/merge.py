from .utility_data import styles_instruments

from pydub import AudioSegment

#TODO DELETE
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


class Merge:
    """
    Класс для посторения аудиодорожек из семплов и наложения их на друг друга.
    """

    def __init__(self, audiolize, track) -> None:
        self.audiolize = audiolize
        self.markup = audiolize.markup
        self.style = track.style
        self.filename = track.filename
        self.ext = track.ext
        
        self.s_length = track.s_length

        self.paths = {}
    
    #TODO bpm, change_speed
    def merge_samples(self, 
                      instrument, 
                      sample_path, 
                      bpm, 
                      change_speed=False):
     
        params = styles_instruments.style_instruments[self.style][instrument]

        print(instrument, params)

        start_at = params['start']
        silents = params['silents']
        samples_count = params['samples']
        print(samples_count)

        sample = AudioSegment.from_wav(sample_path)
        
        #TODO
        if change_speed:
            sample = change_bpm(sample, bpm/150)

        track = AudioSegment.empty()

        for i in range(samples_count):

            if i < start_at: 
                track = track.append(AudioSegment.silent(self.s_length), crossfade=0)
                continue

            # s_sample = AudioSegment.from_wav(sample_path)
            s_sample = sample

            if i in silents.keys():
                for s in silents[i]:

                    start_time = self.s_length * s[0] / 100 if s[0]!=0 else 0
                    end_time = self.s_length * s[1] / 100 if s[1]!=0 else 0

                    if start_time == 0:
                        silence_duration = self.s_length - (self.s_length - end_time)
                    elif end_time == 0:
                        silence_duration = 0
                    else:
                        silence_duration = (self.s_length - start_time) - (self.s_length - end_time)
                    
                    # Создание сегмента тишины
                    silence = AudioSegment.silent(silence_duration)
                    
                    # Замена выбранного фрагмента на тишину 
                    silenced = s_sample[:start_time] + silence + s_sample[end_time:]

                    # print(f'silence_duration: {silence_duration}\n before: {len(s_sample[:start_time])}\nafter: {len(s_sample[end_time:])}\ns_length: {len(silenced)}')
                    # print(len(silenced))
                    
                    s_sample = silenced

                track = track.append(s_sample, crossfade=0)
            else:
                track = track.append(s_sample, crossfade=0)


        save_path = f'{self.audiolize.merge_dir}/merged_{instrument}.wav'
        print(len(track))
        track.export(save_path, format='wav')

        self.paths[instrument] = save_path

    def merge_lines(self, sounds, output_dir):
        sounds = sorted([AudioSegment.from_wav(i) for i in sounds], key=lambda sound: len(sound), reverse=True)
        track = sounds[0]
        for sound in sounds[1:]:
            track = track.overlay(sound)
        print(f'final length {len(track)}')
        output_path = f'{output_dir}/{self.filename}.{self.ext}'
        track.export(output_path, format=self.ext)
        return output_path



