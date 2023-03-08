from glob import glob
from pydub import AudioSegment
import random

import config

def jersey_club(chat_id, bpm):
    print(bpm)
    bass = random.choice([AudioSegment.from_wav(file) for file in glob("style_JC/basses/*.wav")])
    hi_hat = random.choice([AudioSegment.from_wav(file) for file in glob("style_JC/hi-hats/*.wav")])
    kick = random.choice([AudioSegment.from_wav(file) for file in glob("style_JC/kicks/*.wav")])
    clap = random.choice([AudioSegment.from_wav(file) for file in glob("style_JC/claps/*.wav")])
    
    ## sync leads and help_leads ON
    # leads_sync = random.randint(1, len(glob("style_JC/leads/*.wav")))
    # lead = random.choice([AudioSegment.from_wav(file) for file in glob(f"style_JC/leads/lead{leads_sync}.wav")])
    # help_lead = random.choice([AudioSegment.from_wav(file) for file in glob(f"style_JC/help_leads/helplead{leads_sync}.wav")])
    
    ## sync leads and help_leads OFF
    lead = random.choice([AudioSegment.from_wav(file) for file in glob(f"style_JC/leads/*.wav")])
    help_lead = random.choice([AudioSegment.from_wav(file) for file in glob(f"style_JC/help_leads/*.wav")])

    ##### ТАКТЫ #####

    ## 1 ##
    sandwich1 = lead
    overlay = sandwich1

    ## 2 ##
    sandwich2 = sandwich1
    sandwich2 = sandwich2.overlay(help_lead, position=0)
    sandwich2 = sandwich2.overlay(clap, position=0)
    sandwich2 = sandwich2.overlay(hi_hat, position=0)

    overlay = overlay.append(sandwich2)

    ## 3 ##
    sandwich3 = sandwich2
    sandwich3 = sandwich3.overlay(kick, position=0)
    sandwich3 = sandwich3.overlay(bass, position=0)
    
    overlay = overlay.append(sandwich3)

    ## 4 ##

    ## 5 ##

    ## 6 ##

    file_handle = overlay.export(f"output_beats/{chat_id}.wav", format="wav")

def plug():
    pass
