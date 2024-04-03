"""Конвертировать разметку в аудио"""

from random import choice
from glob import glob
from os import remove, path

from pydub import AudioSegment
import soundfile as sf
import pyrubberband as pyrb
import librosa

from .utils import fade_audio_segment
from .utility_data import instruments as instruments_params

def change_note(offset, sound_path, output_path):

    if glob(output_path):
        print('Sound already exists:', output_path)
    else:
        # Load the input .wav file
        y, sr = librosa.load(sound_path)

        # Change the pitch of the audio signal by the given offset
        # The second argument is the pitch factor, which is 2.0 for a 1 octave increase
        # The third argument is the hop length, which determines the time resolution of the pitch shifting
        # The fourth argument is the win_length, which determines the frequency resolution of the pitch shifting
        y_pitched = librosa.effects.pitch_shift(y, sr=sr, n_steps=offset)

        # Save the pitched audio to a new .wav file
        sf.write(output_path, y_pitched, sr)

        print('New note:', output_path)

class Convert:

    def __init__(self, audiolize, track) -> None:
        self.input_dir = track.input_dir
        self.convert_dir = audiolize.convert_dir
        self.fragments_dir = audiolize.fragments_dir

        self.s_length = track.s_length
        self.markup = audiolize.markup

        self.paths = {}

        return

    def convert_to_wav(self,
                       instrument,
                       markup,
                       sounds,
                       just_replace=False):
        
        
        track = AudioSegment.silent(duration=self.s_length)

        sound = choice(sounds)

        if just_replace:
            # track = AudioSegment.from_wav(sound)
            # track.export(f"{self.convert_dir}/{instrument}{1}.wav", format='wav')
            self.paths[instrument] = f"{self.convert_dir}/{instrument}{1}.wav"
            return
        
        for n in markup[0]:
            note, start, duration = n[0], n[1], n[2]

            notes_offset = (note - 72)

            output_path = f'{self.fragments_dir}/{notes_offset}.wav'

            change_note(notes_offset, sound, output_path)

            sample = AudioSegment.from_wav(output_path)

            sample = fade_audio_segment(sample[:duration], instruments_params[instrument]['duration'])

            track = track.overlay(sample, position=start)

        for file in glob(f'{self.fragments_dir}/*'):
            remove(file)
            
        track.export(f"{self.convert_dir}/{instrument}{1}.wav", format='wav')

        self.paths[instrument] = f"{self.convert_dir}/{instrument}{1}.wav"
            
    def wav_to_mp3(self, file_path, output_dir):
        # Check if the file is a .wav file
        if not file_path.endswith(".wav"):
            raise ValueError(f"Input file must be a .wav file, not {path.splitext(file_path)[1]}")
        
        # Load the .wav file
        audio = AudioSegment.from_wav(file_path)

        # Set the output file path
        output_path = f"{output_dir}/output.mp3"

        # Export the audio to .mp3 format
        audio.export(output_path, format="mp3")

