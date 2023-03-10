from glob import glob
from pydub import AudioSegment, silence
import random

import config

def speed_change(sound, speed=1.0):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })

    # convert the sound with altered frame rate to a standard frame rate
    # so that regular playback programs will work right. They often only
    # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

def jersey_club(chat_id, bpm):
    

    bass = random.choice([AudioSegment.from_wav(file) for file in glob("style_JC/bass/*.wav")])
    hi_hat = random.choice([AudioSegment.from_wav(file) for file in glob("style_JC/hi-hat/*.wav")])
    kick = random.choice([AudioSegment.from_wav(file) for file in glob("style_JC/kick/*.wav")])
    clap = random.choice([AudioSegment.from_wav(file) for file in glob("style_JC/clap/*.wav")])
    
    ## sync leads and help_leads ON
    leads_sync = random.randint(1, len(glob("style_JC/lead/*.wav")))
    lead = random.choice([AudioSegment.from_wav(file) for file in glob(f"style_JC/lead/lead{leads_sync}.wav")])
    help_lead = random.choice([AudioSegment.from_wav(file) for file in glob(f"style_JC/helplead/helplead{leads_sync}.wav")])
    
    ## sync leads and help_leads OFF
    # lead = random.choice([AudioSegment.from_wav(file) for file in glob(f"style_JC/lead/*.wav")])
    # help_lead = random.choice([AudioSegment.from_wav(file) for file in glob(f"style_JC/helplead/*.wav")])

    ##### ТАКТЫ #####

    # 14 sec 76 milisec

    #150bpm 4sandwich 51sec 20milisec
    #130bpm 4sandwich 59sec 07milisec

    ## 1 ##
    sandwich1 = lead
    sandwich1 = sandwich1

    overlay = sandwich1

    ## 2 ##
    sandwich2 = lead
    sandwich2 = sandwich2.overlay(help_lead, position=0)
    sandwich2 = sandwich2.overlay(clap, position=0)
    sandwich2 = sandwich2.overlay(hi_hat, position=0)


    overlay = overlay.append(sandwich2, crossfade=0)

    ## 3 ##
    sandwich3 = lead
    sandwich3 = sandwich3.overlay(help_lead, position=0)
    sandwich3 = sandwich3.overlay(clap, position=0)
    sandwich3 = sandwich3.overlay(hi_hat, position=0)
    sandwich3 = sandwich3.overlay(kick, position=0)
    sandwich3 = sandwich3.overlay(bass, position=0)

    
    overlay = overlay.append(sandwich3, crossfade=0)

    ## 4 ##
    sandwich4 = lead
    sandwich4 = sandwich4.overlay(help_lead, position=0)
    sandwich4 = sandwich4.overlay(clap, position=0)
    sandwich4 = sandwich4.overlay(hi_hat, position=0)
    sandwich4 = sandwich4.overlay(kick, position=0)
    sandwich4 = sandwich4.overlay(bass, position=0)

    
    overlay = overlay.append(sandwich4, crossfade=0)

    ## 5 ##
    sandwich5 = lead
    sandwich5 = sandwich5.overlay(clap, position=0)
    sandwich5 = sandwich5.overlay(hi_hat, position=0)
    sandwich5 = sandwich5.overlay(kick, position=0)
    sandwich5 = sandwich5.overlay(bass, position=0)


    overlay = overlay.append(sandwich5, crossfade=0)

    ## 6 ##
    sandwich6 = lead
    sandwich6 = sandwich6.overlay(help_lead, position=0)
    sandwich6 = sandwich6.overlay(clap, position=0)
    sandwich6 = sandwich6.overlay(hi_hat, position=0)
    sandwich6 = sandwich6.overlay(kick, position=0)
    sandwich6 = sandwich6.overlay(bass, position=0)


    overlay = overlay.append(sandwich6, crossfade=0)

    ## 7 ##
    sandwich7 = lead
    sandwich7 = sandwich2.overlay(help_lead, position=0)
    

    overlay = overlay.append(sandwich7, crossfade=0)


    bpm = int(bpm.split('b')[0])

    if bpm == 130:
        pass  
    elif bpm < 130:
        overlay = speed_change(overlay, bpm/130)
    else:
        overlay = overlay.speedup(bpm/130)
        
    file_handle = overlay.export(f"output_beats/{chat_id}.wav", format="wav")

def plug():
    pass