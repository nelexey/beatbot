from random import choice
from pydub import AudioSegment
from glob import glob

from generator.helpers import change_bpm


def drill(filename: str,
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
    bass = AudioSegment.from_wav(bass_path)

    """ ТАКТЫ """

    # 1 #
    sandwich1 = lead
    sandwich1 = sandwich1.overlay(voicetag, position=0)
    sandwich1 = sandwich1.overlay(hi_hat[:-1840], position=-1840)
    sandwich1 = sandwich1.overlay(clap[:-1840], position=-1840)

    overlay = sandwich1

    # 2 #
    sandwich2 = lead
    sandwich2 = sandwich2.overlay(bass, position=0)
    sandwich2 = sandwich2.overlay(clap, position=0)
    sandwich2 = sandwich2.overlay(hi_hat[:-460], position=0)
    sandwich2 = sandwich2.overlay(kick[920:], position=920)

    overlay = overlay.append(sandwich2, crossfade=0)

    # 3 #
    sandwich3 = lead
    sandwich3 = sandwich3.overlay(clap, position=0)
    sandwich3 = sandwich3.overlay(hi_hat, position=0)
    sandwich3 = sandwich3.overlay(kick, position=0)
    sandwich3 = sandwich3.overlay(bass, position=0)

    overlay = overlay.append(sandwich3, crossfade=0)

    # 4 #
    sandwich4 = lead
    sandwich4 = sandwich4.overlay(clap, position=0)
    sandwich4 = sandwich4.overlay(hi_hat, position=0)
    sandwich4 = sandwich4.overlay(kick[:-920], position=-920)
    sandwich4 = sandwich4.overlay(bass, position=0)

    overlay = overlay.append(sandwich4, crossfade=0)

    # 5 #
    sandwich5 = lead
    sandwich5 = sandwich5.overlay(clap, position=0)
    sandwich5 = sandwich5.overlay(hi_hat, position=0)
    sandwich5 = sandwich5.overlay(kick, position=0)
    sandwich5 = sandwich5.overlay(bass, position=0)

    overlay = overlay.append(sandwich5, crossfade=0)

    # 6 #
    sandwich6 = lead
    sandwich6 = sandwich6.overlay(clap, position=0)
    sandwich6 = sandwich6.overlay(hi_hat, position=0)
    sandwich6 = sandwich6.overlay(kick, position=0)
    sandwich6 = sandwich6.overlay(bass, position=0)

    overlay = overlay.append(sandwich6, crossfade=0)

    # 7 #
    sandwich7 = lead
    sandwich7 = sandwich7.overlay(clap, position=0)
    sandwich7 = sandwich7.overlay(hi_hat[:-460], position=0)
    sandwich7 = sandwich7.overlay(kick[:-460], position=0)
    sandwich7 = sandwich7.overlay(bass, position=0)

    overlay = overlay.append(sandwich7, crossfade=0)

    # 8 #
    sandwich8 = lead
    sandwich8 = sandwich8.overlay(bass[2300:], position=2300)
    sandwich8 = sandwich8.overlay(hi_hat, position=0)
    sandwich8 = sandwich8.overlay(clap, position=0)
    sandwich8 = sandwich8.overlay(kick, position=0)

    overlay = overlay.append(sandwich8, crossfade=0)

    # 9 #
    sandwich9 = lead
    sandwich9 = sandwich9.overlay(bass, position=0)
    sandwich9 = sandwich9.overlay(hi_hat[:-460], position=0)
    sandwich9 = sandwich9.overlay(clap[:-460], position=0)
    sandwich9 = sandwich9.overlay(kick[:-460], position=0)

    overlay = overlay.append(sandwich9, crossfade=0)

    # 10 #
    sandwich10 = lead
    sandwich10 = sandwich10.overlay(voicetag, position=0)

    overlay = overlay.append(sandwich10, crossfade=0)

    if bpm == 130:
        pass
    else:
        overlay = change_bpm(overlay, bpm / 130)

    audio_path = f"{user_dir}/{filename}.{ext}"

    overlay.export(audio_path, format=f"{ext}")

    return audio_path

