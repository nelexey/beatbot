from random import choice
from pydub import AudioSegment
from glob import glob
from generator.helpers import change_bpm


def old_school(filename: str,
               lead_path: str,
               bass_path: str,
               style_dir: str,
               user_dir: str,
               bpm: int,
               ext: str) -> str:
    clap = choice([AudioSegment.from_wav(file) for file in glob(f"{style_dir}/clap/*.wav")])
    hi_hat = choice([AudioSegment.from_wav(file) for file in glob(f"{style_dir}/hi-hat/*.wav")])
    kick = choice([AudioSegment.from_wav(file) for file in glob(f"{style_dir}/kick/*.wav")])
    voicetag = AudioSegment.from_wav(f'{style_dir}/../voicetags/beatbot_voicetag_170bpm.wav')

    lead = AudioSegment.from_wav(lead_path)
    bass = AudioSegment.from_wav(bass_path)

    """ ТАКТЫ """

    # 1 #
    sandwich1 = lead
    overlay = sandwich1

    # 2 #
    sandwich2 = lead
    sandwich2 = sandwich2.overlay(voicetag, position=0)
    sandwich2 = sandwich2.overlay(hi_hat, position=0)
    sandwich2 = sandwich2.overlay(kick, position=0)

    overlay = overlay.append(sandwich2, crossfade=0)

    # 3-9 #
    for _ in range(3, 10):
        sandwich = lead
        sandwich = sandwich.overlay(clap, position=0)
        sandwich = sandwich.overlay(hi_hat, position=0)
        sandwich = sandwich.overlay(kick, position=0)
        sandwich = sandwich.overlay(bass, position=0)
        overlay = overlay.append(sandwich, crossfade=0)

    # 10 #
    sandwich10 = lead
    sandwich10 = sandwich10.overlay(hi_hat, position=0)
    sandwich10 = sandwich10.overlay(kick, position=0)

    overlay = overlay.append(sandwich10, crossfade=0)

    # 11 #
    sandwich11 = lead
    overlay = overlay.append(sandwich11, crossfade=0)

    if bpm != 170:
        overlay = change_bpm(overlay, bpm / 170)

    audio_path = f"{user_dir}/{filename}.{ext}"
    overlay.export(audio_path, format=ext)

    return audio_path
