from pydub import AudioSegment


def trimmed_audio_mp3(filename, file, output_path):
    sound = AudioSegment.from_file(file)
    trimmed = sound[35000:50000]
    new_file_path = f"{output_path}/{filename}.mp3"
    trimmed.export(new_file_path, format=f"mp3")

    return new_file_path
