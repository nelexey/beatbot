import os
from pydub import AudioSegment
from glob import glob
import pyrubberband as pyrb
import soundfile as sf

from generator.helpers import create_midi_markup, remove_start_silence, generate_random_filename


def change_pitch(audio_path, cent_change, output_filename):
    if glob(output_filename): return

    audio_data, sample_rate = sf.read(audio_path)

    # Временное изменение pitch с помощью pyrubberband
    shifted_audio = pyrb.pitch_shift(audio_data[:, 0], sample_rate, cent_change / 100)

    # Сохранение измененного звука в новый аудиофайл
    sf.write(output_filename, shifted_audio, sample_rate)


def midi_to_wav_handler(midi_path, audio_path, audio_format):

    fragments_dir = os.path.join(os.path.dirname(audio_path), "fragments")

    os.makedirs(fragments_dir, exist_ok=True)

    midi_markup, time = create_midi_markup(midi_path)

    track = AudioSegment.silent(duration=time)

    for preset in midi_markup:
        note, start_time, duration = preset[0], preset[1], preset[2]
        cent_change = (note - 72) * 100

        output_filename = f'{fragments_dir}/{note}.wav'

        change_pitch(audio_path, cent_change, output_filename)

        instrument = AudioSegment.from_file(output_filename, format='wav')
        instrument = remove_start_silence(instrument)

        track = track.overlay(instrument[:duration], position=start_time)

    for file in glob(f'{fragments_dir}/*'):
        os.remove(file)

    new_audio_path = os.path.join(os.path.dirname(audio_path), f"{generate_random_filename()}.{audio_format}")

    track.export(new_audio_path, format=audio_format)

    return new_audio_path

