from pydub import AudioSegment


def change_bpm(sound: AudioSegment, speed=1.0):
    # Установка частоты кадров вручную. Это говорит компьютеру, сколько
    # образцов воспроизводить в секунду
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })

    # Преобразование звука с измененной частотой кадров в стандартную частоту кадров,
    # чтобы обычные программы воспроизведения работали правильно. Они часто умеют
    # воспроизводить звук только на стандартной частоте кадров (например, 44,1 кГц)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)
