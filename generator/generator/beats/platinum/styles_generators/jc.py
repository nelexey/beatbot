from random import choice
from pydub import AudioSegment
from glob import glob
from generator.helpers import change_bpm


def jersey_club(filename: str,
                lead_path: str,
                bass_path: str,
                style_dir: str,
                user_dir: str,
                bpm: int,
                ext: str) -> str:
    hi_hat = choice([AudioSegment.from_wav(file) for file in glob(f"{style_dir}/hi-hat/*.wav")])
    kick = choice([AudioSegment.from_wav(file) for file in glob(f"{style_dir}/kick/*.wav")])
    voicetag = AudioSegment.from_wav(f'{style_dir}/../voicetags/beatbot_voicetag_145bpm.wav')

    lead = AudioSegment.from_wav(lead_path)
    bass = AudioSegment.from_wav(bass_path)

    """ ТАКТЫ """

    # 1 #
    sandwich1 = lead
    sandwich1 = sandwich1.overlay(voicetag, position=0)
    sandwich1 = sandwich1.overlay(kick, position=0)
    sandwich1 = sandwich1.overlay(hi_hat, position=0)
    sandwich1 = sandwich1.overlay(bass, position=0)

    sandwich1 = sandwich1[:6620]
    octaves = -1
    new_sample_rate = int(sandwich1.frame_rate * (2.0 ** octaves))
    sandwich1 = sandwich1._spawn(sandwich1.raw_data, overrides={'frame_rate': new_sample_rate})

    overlay = sandwich1

    # 2 #
    sandwich2 = lead
    sandwich2 = sandwich2.overlay(hi_hat, position=0)

    overlay = overlay.append(sandwich2, crossfade=0)

    # 3 #
    sandwich3 = lead
    sandwich3 = sandwich3.overlay(hi_hat, position=0)
    sandwich3 = sandwich3.overlay(kick, position=0)
    sandwich3 = sandwich3.overlay(bass, position=0)

    overlay = overlay.append(sandwich3, crossfade=0)

    # 4 #
    sandwich4 = lead
    sandwich4 = sandwich4.overlay(hi_hat, position=0)
    sandwich4 = sandwich4.overlay(kick[3300:], position=3300)
    sandwich4 = sandwich4.overlay(bass[3300:], position=3300)

    overlay = overlay.append(sandwich4, crossfade=0)

    # 5 #
    sandwich5 = lead
    sandwich5 = sandwich5.overlay(hi_hat, position=0)
    sandwich5 = sandwich5.overlay(kick, position=0)
    sandwich5 = sandwich5.overlay(bass, position=0)

    overlay = overlay.append(sandwich5, crossfade=0)

    # 6 #
    sandwich6 = lead
    sandwich6 = sandwich6.overlay(hi_hat, position=0)
    sandwich6 = sandwich6.overlay(kick[3300:], position=3300)
    sandwich6 = sandwich6.overlay(bass[3300:], position=3300)

    overlay = overlay.append(sandwich6, crossfade=0)

    # 7 #
    sandwich7 = lead
    sandwich7 = sandwich7.overlay(hi_hat, position=0)
    sandwich7 = sandwich7.overlay(kick, position=0)
    sandwich7 = sandwich7.overlay(bass, position=0)

    overlay = overlay.append(sandwich7, crossfade=0)

    # 8 #
    sandwich8 = lead
    sandwich8 = sandwich8.overlay(hi_hat, position=0)

    overlay = overlay.append(sandwich8, crossfade=0)

    # 9 #
    sandwich9 = lead

    overlay = overlay.append(sandwich9, crossfade=0)

    if bpm == 145:
        pass
    else:
        overlay = change_bpm(overlay, bpm / 145)

    audio_path = f"{user_dir}/{filename}.{ext}"

    overlay.export(audio_path, format=ext)

    return audio_path
