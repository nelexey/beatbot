from pedalboard import Pedalboard, Reverb
from pedalboard.io import AudioFile
import math
from pydub import AudioSegment

class Effects:
    """
    Класс для применения vst-плагинов и эффектов на аудио.
    """

    def __init__(self) -> None:
        pass

    def reverb(self, file, **params):
        # Read in a whole file, resampling to our desired sample rate:
        samplerate = 44100.0
        with AudioFile(file).resampled_to(samplerate) as f:
            audio = f.read(f.frames)

        # Make a pretty interesting sounding guitar pedalboard:
        board = Pedalboard([
            Reverb(room_size=params['room_size'],
                wet_level=params['wet_level'],
                ),
        ])

        # Run the audio through this pedalboard!
        effected = board(audio, samplerate)

        # Write the audio back as a wav file:
        with AudioFile(file, 'w', samplerate, effected.shape[0]) as f:
            f.write(effected)
    
    def volume(self, file, **params):
        if not params['volume']: 
            print('No volume parameter in sample')
            return 
        
        sound = AudioSegment.from_file(file)

        dB_change = 20 * math.log10(params['volume'])

        # Уменьшить громкость
        quieter_sound = sound.apply_gain(dB_change)

        # Сохранить новый файл
        quieter_sound.export(file, format="wav")
