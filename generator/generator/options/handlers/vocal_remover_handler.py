import os
import subprocess
from pydub import AudioSegment
from pydub.utils import make_chunks

from generator.helpers.rd_filename import generate_random_filename


def remove_vocal_handler(audio_path):
    # Create a fragments directory if it doesn't exist
    fragments_dir = os.path.join(os.path.dirname(audio_path), "fragments")
    os.makedirs(fragments_dir, exist_ok=True)

    # Convert to wav if the file is mp3
    if audio_path.endswith('.mp3'):
        audio = AudioSegment.from_mp3(audio_path)
        new_audio_path = audio_path.replace('.mp3', '.wav')
        audio.export(new_audio_path, format="wav")

    # Split audio into 30 sec fragments
    audio = AudioSegment.from_file(audio_path)
    chunks = make_chunks(audio, 30000)

    # Process each chunk
    vocals = []
    accompaniment = []
    for i, chunk in enumerate(chunks):
        # Export chunk to a file
        fragment_filename = os.path.join(fragments_dir, f"{i}.wav")
        chunk.export(fragment_filename, format="wav")

        # Run spleeter on the fragment
        subprocess.run(
            f'python3 -m spleeter separate {fragment_filename} -p spleeter:2stems -o {fragments_dir} --filename_format "{i}_{{instrument}}.{{codec}}"',
            shell=True)

        # Add the vocal and accompaniment files to the lists
        vocals.append(os.path.join(fragments_dir, f"{i}_vocals.wav"))
        accompaniment.append(os.path.join(fragments_dir, f"{i}_accompaniment.wav"))

    # Combine the vocal and accompaniment files
    combined_vocals = AudioSegment.empty()
    combined_accompaniment = AudioSegment.empty()
    for vocal_file, accompaniment_file in zip(vocals, accompaniment):
        combined_vocals += AudioSegment.from_file(vocal_file)
        combined_accompaniment += AudioSegment.from_file(accompaniment_file)

    # Export the combined files
    vocals_output_path = os.path.join(os.path.dirname(audio_path), f"{generate_random_filename()}_vocals.wav")
    accompaniment_output_path = os.path.join(os.path.dirname(audio_path), f"{generate_random_filename()}_accompaniment.wav")
    combined_vocals.export(vocals_output_path, format="wav")
    combined_accompaniment.export(accompaniment_output_path, format="wav")

    # Clean up
    for i in range(len(chunks)):
        os.remove(os.path.join(fragments_dir, f"{i}.wav"))
        os.remove(os.path.join(fragments_dir, f"{i}_vocals.wav"))
        os.remove(os.path.join(fragments_dir, f"{i}_accompaniment.wav"))
    os.rmdir(fragments_dir)
    os.remove(audio_path)
    os.remove(new_audio_path)

    return vocals_output_path, accompaniment_output_path
