from random import choice
from pydub import AudioSegment
from glob import glob
from generator.helpers import change_bpm


def newjazz(filename: str,
            lead_path: str,
            bass_path: str,
            style_dir: str,
            user_dir: str,
            bpm: int,
            ext: str) -> str:
    clap = choice([AudioSegment.from_wav(file) for file in glob(f"{style_dir}/clap/*.wav")])
    hi_hat = choice([AudioSegment.from_wav(file) for file in glob(f"{style_dir}/hi-hat/*.wav")])
    kick = choice([AudioSegment.from_wav(file) for file in glob(f"{style_dir}/kick/*.wav")])
    voicetag = AudioSegment.from_wav(f'{style_dir}/../voicetags/beatbot_voicetag_130bpm.wav')

    lead = AudioSegment.from_wav(lead_path)

    """ ТАКТЫ """

    # 1 #
    sandwich1 = lead
    sandwich1 = sandwich1.overlay(voicetag, position=0)
    sandwich1 = sandwich1.overlay(hi_hat[:-1840], position=-1840)
    sandwich1 = sandwich1.overlay(clap[:-1840], position=-1840)

    overlay = sandwich1

    # 2-9 #
    for i in range(2, 10):
        sandwich = lead
        sandwich = sandwich.overlay(clap, position=0)
        sandwich = sandwich.overlay(hi_hat, position=0)

        if i == 2:
            sandwich = sandwich.overlay(hi_hat[:-460], position=0)
            sandwich = sandwich.overlay(kick[920:], position=920)
        elif i == 4:
            sandwich = sandwich.overlay(kick[:-920], position=-920)
        elif i in [3, 5, 6, 8]:
            sandwich = sandwich.overlay(kick, position=0)
        elif i == 7:
            sandwich = sandwich.overlay(hi_hat[:-460], position=0)
            sandwich = sandwich.overlay(kick[:-460], position=0)
        elif i == 9:
            sandwich = sandwich.overlay(hi_hat[:-460], position=0)
            sandwich = sandwich.overlay(clap[:-460], position=0)
            sandwich = sandwich.overlay(kick[:-460], position=0)

        overlay = overlay.append(sandwich, crossfade=0)

    # 10 #
    sandwich10 = lead
    sandwich10 = sandwich10.overlay(voicetag, position=0)

    overlay = overlay.append(sandwich10, crossfade=0)

    if bpm != 130:
        overlay = change_bpm(overlay, bpm / 130)

    audio_path = f"{user_dir}/{filename}.{ext}"
    overlay.export(audio_path, format=ext)

    return audio_path
