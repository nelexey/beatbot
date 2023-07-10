from glob import glob
from pydub import AudioSegment
from random import choice, randint, sample
import re

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

def generate_some_beats(aliases, num, style, chat_id, bpm, extension):
    # Выбрать случайные неповторяющиеся лиды 

    get_leads = sample(glob(f"style_{aliases[style]}/lead/*.wav"), 3)
    
    sample_presets = []
    for file in get_leads:
        match = re.search(r'\d+', file)
        if match:
            sample_presets.append(int(match.group())) 
    print(sample_presets)
    for i in range(1, num+1):
        # ОБЯЗАТЕЛЬНО УКАЗЫВАТЬ SAMPLE_PRESET ЕСЛИ ЗВУКИ НЕ ИДУТ В ТОЧНОМ ЧИСЛОВОМ ПОРЯДКЕ
        if style == 'Jersey Club':
            status = jersey_club(chat_id, bpm, i, sample_presets[i-1], extension)
        elif style == 'Trap':
            status = trap(chat_id, bpm, i, sample_presets[i-1], extension)
        elif style == 'Drill':
            status = drill(chat_id, bpm, i, sample_presets[i-1], extension)
        elif style == 'Plug':
            status = plug(chat_id, bpm, i, sample_presets[i-1], extension)
        elif style == 'Old School':
            status = old_school(chat_id, bpm, i, sample_presets[i-1], extension)
    if status:
        return True
    else:
        return False

def jersey_club(chat_id, bpm, file_corr=0, sample_preset=0, extension='wav'):
    bass = choice([AudioSegment.from_wav(file) for file in glob("style_JC/bass/*.wav")])
    hi_hat = choice([AudioSegment.from_wav(file) for file in glob("style_JC/hi-hat/*.wav")])
    kick = choice([AudioSegment.from_wav(file) for file in glob("style_JC/kick/*.wav")])
   
    ## sync leads and help_leads ON
    if sample_preset==0: 
   
        leads_sync = randint(1, len(glob("style_JC/lead/*.wav"))+1)
        
    else:
        leads_sync = sample_preset

    lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_JC/lead/lead{leads_sync}.wav")])
    help_lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_JC/helplead/helplead{leads_sync}.wav")])

    ## sync leads and help_leads OFF
    # lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_JC/lead/*.wav")])
    # help_lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_JC/helplead/*.wav")])

    ##### ТАКТЫ #####

    # 13240

    ## 1 ##
    sandwich1 = lead
    sandwich1 = sandwich1.overlay(help_lead, position=0)
    sandwich1 = sandwich1.overlay(kick, position=0)
    sandwich1 = sandwich1.overlay(hi_hat, position=0)
    sandwich1 = sandwich1.overlay(bass, position=0)

    sandwich1 = sandwich1[:6620]
    octaves = -1
    new_sample_rate = int(sandwich1.frame_rate * (2.0 ** octaves))
    sandwich1 = sandwich1._spawn(sandwich1.raw_data, overrides={'frame_rate': new_sample_rate})

    overlay = sandwich1

    ## 2 ##

    sandwich2 = lead
    sandwich2 = sandwich2.overlay(help_lead, position=0)
    sandwich2 = sandwich2.overlay(hi_hat, position=0)

    overlay = overlay.append(sandwich2, crossfade=0)

    ## 3 ##
    sandwich3 = lead
    sandwich3 = sandwich3.overlay(help_lead, position=0)
    sandwich3 = sandwich3.overlay(hi_hat, position=0)
    sandwich3 = sandwich3.overlay(kick, position=0)
    sandwich3 = sandwich3.overlay(bass, position=0)

    overlay = overlay.append(sandwich3, crossfade=0)

    ## 4 ##
    sandwich4 = lead
    sandwich4 = sandwich4.overlay(help_lead, position=0)
    sandwich4 = sandwich4.overlay(hi_hat, position=0)
    # Наложение не сразу после начала
    sandwich4 = sandwich4.overlay(kick[3300:], position=3300)
    sandwich4 = sandwich4.overlay(bass[3300:], position=3300)
    
    overlay = overlay.append(sandwich4, crossfade=0)

    ## 5 ##
    sandwich5 = lead
    sandwich5 = sandwich5.overlay(help_lead, position=0)
    sandwich5 = sandwich5.overlay(hi_hat, position=0)
    sandwich5 = sandwich5.overlay(kick, position=0)
    sandwich5 = sandwich5.overlay(bass, position=0)
  
    overlay = overlay.append(sandwich5, crossfade=0)

    ## 6 ##
    sandwich6 = lead
    sandwich6 = sandwich6.overlay(help_lead, position=0)
    sandwich6 = sandwich6.overlay(hi_hat, position=0)
    # Наложение не сразу после начала
    sandwich6 = sandwich6.overlay(kick[3300:], position=3300)
    sandwich6 = sandwich6.overlay(bass[3300:], position=3300)

    overlay = overlay.append(sandwich6, crossfade=0)

    ## 7 ##
    sandwich7 = lead
    sandwich7 = sandwich7.overlay(help_lead, position=0)
    sandwich7 = sandwich7.overlay(hi_hat, position=0)
    sandwich7 = sandwich7.overlay(kick, position=0)
    sandwich7 = sandwich7.overlay(bass, position=0)

    overlay = overlay.append(sandwich7, crossfade=0)

    ## 8 ##
    sandwich8 = lead
    sandwich8 = sandwich8.overlay(help_lead, position=0)
    sandwich8 = sandwich8.overlay(hi_hat, position=0)
    
    overlay = overlay.append(sandwich8, crossfade=0)

    ## 9 ##
    sandwich9 = lead
    
    overlay = overlay.append(sandwich9, crossfade=0)

    bpm = int(bpm.split('b')[0])

    overlay = speed_change(overlay, bpm/145)
    
    if file_corr!=0:
        file_handle = overlay.export(f"output_beats/{chat_id}_{str(file_corr)}.{extension}", format=extension)
    else:
        file_handle = overlay.export(f"output_beats/{chat_id}.{extension}", format=extension)

    return True

def old_school(chat_id, bpm, file_corr=0, sample_preset=0, extension='wav'):
    clap = choice([AudioSegment.from_wav(file) for file in glob("style_OldSchool/clap/*.wav")])
    bass = choice([AudioSegment.from_wav(file) for file in glob("style_OldSchool/bass/*.wav")])
    hi_hat = choice([AudioSegment.from_wav(file) for file in glob("style_OldSchool/hi-hat/*.wav")])
    kick = choice([AudioSegment.from_wav(file) for file in glob("style_OldSchool/kick/*.wav")])
   
    ## sync leads and help_leads ON
    if sample_preset==0: 
        
        leads_sync = randint(1, len(glob("style_OldSchool/lead/*.wav"))+1)
        
    else:
        leads_sync = sample_preset

    lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_OldSchool/lead/lead{leads_sync}.wav")])
    help_lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_OldSchool/helplead/helplead{leads_sync}.wav")])

    ## sync leads and help_leads OFF
    # lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_OldSchool/lead/*.wav")])
    # help_lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_OldSchool/helplead/*.wav")])

    # 11290
    ##### ТАКТЫ #####

    ## 1 ##
    sandwich1 = lead

    overlay = sandwich1

    ## 2 ##
    sandwich2 = lead
    sandwich2 = sandwich2.overlay(hi_hat, position=0)
    sandwich2 = sandwich2.overlay(kick, position=0)

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
    sandwich5 = sandwich5.overlay(hi_hat, position=0)
    sandwich5 = sandwich5.overlay(kick, position=0)
 
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
    sandwich7 = sandwich7.overlay(help_lead, position=0)
    sandwich7 = sandwich7.overlay(clap, position=0)
    sandwich7 = sandwich7.overlay(hi_hat, position=0)
    sandwich7 = sandwich7.overlay(kick, position=0)
    sandwich7 = sandwich7.overlay(bass, position=0)

    overlay = overlay.append(sandwich7, crossfade=0)

    ## 8 ##
    sandwich8 = lead
    sandwich8 = sandwich8.overlay(help_lead, position=0)
    sandwich8 = sandwich8.overlay(clap, position=0)
    sandwich8 = sandwich8.overlay(hi_hat, position=0)
    sandwich8 = sandwich8.overlay(kick, position=0)
    sandwich8 = sandwich8.overlay(bass, position=0)

    overlay = overlay.append(sandwich8, crossfade=0)

    ## 9 ##
    sandwich9 = lead
    sandwich9 = sandwich9.overlay(help_lead, position=0)
    sandwich9 = sandwich9.overlay(clap, position=0)
    sandwich9 = sandwich9.overlay(hi_hat, position=0)
    sandwich9 = sandwich9.overlay(kick, position=0)
    sandwich9 = sandwich9.overlay(bass, position=0)

    overlay = overlay.append(sandwich9, crossfade=0)

    ## 10 ##
    sandwich10 = lead
    sandwich10 = sandwich10.overlay(hi_hat, position=0)
    sandwich10 = sandwich10.overlay(kick, position=0)
    
    overlay = overlay.append(sandwich10, crossfade=0)

    ## 11 ##
    sandwich11 = lead
    
    overlay = overlay.append(sandwich11, crossfade=0)

    bpm = int(bpm.split('b')[0])

    if bpm == 170:
        pass       
    else:
        overlay = speed_change(overlay, bpm/170)
    
    
    if file_corr!=0:
        file_handle = overlay.export(f"output_beats/{chat_id}_{str(file_corr)}.{extension}", format=f"{extension}")
    else:
        file_handle = overlay.export(f"output_beats/{chat_id}.{extension}", format=f"{extension}")

    return True

def drill(chat_id, bpm, file_corr=0, sample_preset=0, extension='wav'):
    clap = choice([AudioSegment.from_wav(file) for file in glob("style_Drill/clap/*.wav")])
    bass = choice([AudioSegment.from_wav(file) for file in glob("style_Drill/bass/*.wav")])
    hi_hat = choice([AudioSegment.from_wav(file) for file in glob("style_Drill/hi-hat/*.wav")])
    kick = choice([AudioSegment.from_wav(file) for file in glob("style_Drill/kick/*.wav")])
   
    ## sync leads and help_leads ON
    if sample_preset==0: 
        
        leads_sync = randint(1, len(glob("style_Drill/lead/*.wav"))+1)
        
    else:
        leads_sync = sample_preset

    lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_Drill/lead/lead{leads_sync}.wav")])
    help_lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_Drill/helplead/helplead{leads_sync}.wav")])

    ## sync leads and help_leads OFF
    # lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_Drill/lead/*.wav")])
    # help_lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_Drill/helplead/*.wav")])


    ##### ТАКТЫ #####

    # 14 sec 76 milisec

    #150bpm 4sandwich 51sec 20milisec
    #130bpm 4sandwich 59sec 07milisec

    ## 1 ##
    sandwich1 = lead
    sandwich1 = sandwich1.overlay(help_lead, position=0)
    sandwich1 = sandwich1.overlay(clap, position=0)
    sandwich1 = sandwich1.overlay(hi_hat, position=0)
    sandwich1 = sandwich1.overlay(kick, position=0)
    sandwich1 = sandwich1.overlay(bass, position=0)

    sandwich1 = sandwich1[:7380] 
    octaves = -1
    new_sample_rate = int(sandwich1.frame_rate * (2.0 ** octaves))
    sandwich1 = sandwich1._spawn(sandwich1.raw_data, overrides={'frame_rate': new_sample_rate})

    overlay = sandwich1

    ## 2 ##
    sandwich2 = lead

    overlay = overlay.append(sandwich2, crossfade=0)

    ## 3 ##
    sandwich3 = lead
    sandwich3 = sandwich3.overlay(help_lead, position=0)
    sandwich3 = sandwich3.overlay(clap, position=0)
    sandwich3 = sandwich3.overlay(hi_hat, position=0)

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
    sandwich5 = sandwich5.overlay(help_lead, position=0)
    sandwich5 = sandwich5.overlay(clap, position=0)
    sandwich5 = sandwich5.overlay(hi_hat, position=0)
    sandwich5 = sandwich5.overlay(kick, position=0)
    sandwich5 = sandwich5.overlay(bass, position=0)
    
    overlay = overlay.append(sandwich5, crossfade=0)

    ## 6 ##
    sandwich6 = lead
    sandwich6 = sandwich6.overlay(clap, position=0)
    sandwich6 = sandwich6.overlay(hi_hat, position=0)
    sandwich6 = sandwich6.overlay(kick, position=0)
    sandwich6 = sandwich6.overlay(bass, position=0)

    overlay = overlay.append(sandwich6, crossfade=0)

    ## 7 ##
    sandwich7 = lead
    sandwich7 = sandwich7.overlay(help_lead, position=0)
    sandwich7 = sandwich7.overlay(clap, position=0)
    sandwich7 = sandwich7.overlay(hi_hat, position=0)
    sandwich7 = sandwich7.overlay(kick, position=0)
    sandwich7 = sandwich7.overlay(bass, position=0)

    overlay = overlay.append(sandwich7, crossfade=0)

    ## 8 ##
    sandwich8 = lead
    sandwich8 = sandwich8.overlay(help_lead, position=0)

    overlay = overlay.append(sandwich8, crossfade=0)

    bpm = int(bpm.split('b')[0])

    if bpm == 130:
        pass       
    else:
        overlay = speed_change(overlay, bpm/130)
    
    if file_corr!=0:
        file_handle = overlay.export(f"output_beats/{chat_id}_{str(file_corr)}.{extension}", format=f"{extension}")
    else:
        file_handle = overlay.export(f"output_beats/{chat_id}.{extension}", format=f"{extension}")

    return True

def plug(chat_id, bpm, file_corr=0, sample_preset=0, extension='wav'):
    clap = choice([AudioSegment.from_wav(file) for file in glob("style_Plug/clap/*.wav")])
    bass = choice([AudioSegment.from_wav(file) for file in glob("style_Plug/bass/*.wav")])
    hi_hat = choice([AudioSegment.from_wav(file) for file in glob("style_Plug/hi-hat/*.wav")])
    kick = choice([AudioSegment.from_wav(file) for file in glob("style_Plug/kick/*.wav")])
   
    ## sync leads and help_leads ON
    if sample_preset==0: 
        
        leads_sync = randint(1, len(glob("style_Plug/lead/*.wav"))+1)
        
    else:
        leads_sync = sample_preset

    lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_Plug/lead/lead{leads_sync}.wav")])
    help_lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_Plug/helplead/helplead{leads_sync}.wav")])

    ## sync leads and help_leads OFF
    # lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_Plug/lead/*.wav")])
    # help_lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_Plug/helplead/*.wav")])

    ##### ТАКТЫ #####

    # 14 sec 76 milisec

    #150bpm 4sandwich 51sec 20milisec
    #130bpm 4sandwich 59sec 07milisec

    ## 1 ##
    sandwich1 = lead
    sandwich1 = sandwich1.overlay(help_lead, position=0)
    sandwich1 = sandwich1.overlay(clap, position=0)
    sandwich1 = sandwich1.overlay(hi_hat, position=0)
    sandwich1 = sandwich1.overlay(kick, position=0)
    sandwich1 = sandwich1.overlay(bass, position=0)

    sandwich1 = sandwich1[:6620] 
    octaves = -1
    new_sample_rate = int(sandwich1.frame_rate * (2.0 ** octaves))
    sandwich1 = sandwich1._spawn(sandwich1.raw_data, overrides={'frame_rate': new_sample_rate})

    overlay = sandwich1

    ## 2 ##
    sandwich2 = lead

    overlay = overlay.append(sandwich2, crossfade=0)

    ## 3 ##
    sandwich3 = lead
    sandwich3 = sandwich3.overlay(help_lead, position=0)
    sandwich3 = sandwich3.overlay(clap, position=0)
    sandwich3 = sandwich3.overlay(hi_hat, position=0)

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
    sandwich5 = sandwich5.overlay(help_lead, position=0)
    sandwich5 = sandwich5.overlay(clap, position=0)
    sandwich5 = sandwich5.overlay(hi_hat, position=0)
    sandwich5 = sandwich5.overlay(kick, position=0)
    sandwich5 = sandwich5.overlay(bass, position=0)
 
    overlay = overlay.append(sandwich5, crossfade=0)

    ## 6 ##
    sandwich6 = lead
    sandwich6 = sandwich6.overlay(clap, position=0)
    sandwich6 = sandwich6.overlay(hi_hat, position=0)
    sandwich6 = sandwich6.overlay(kick, position=0)
    sandwich6 = sandwich6.overlay(bass, position=0)

    overlay = overlay.append(sandwich6, crossfade=0)

    ## 7 ##
    sandwich7 = lead
    sandwich7 = sandwich7.overlay(help_lead, position=0)
    sandwich7 = sandwich7.overlay(clap, position=0)
    sandwich7 = sandwich7.overlay(hi_hat, position=0)
    sandwich7 = sandwich7.overlay(kick, position=0)
    sandwich7 = sandwich7.overlay(bass, position=0)

    overlay = overlay.append(sandwich7, crossfade=0)

    ## 8 ##
    sandwich8 = lead
    sandwich8 = sandwich8.overlay(help_lead, position=0)
    
    overlay = overlay.append(sandwich8, crossfade=0)

    bpm = int(bpm.split('b')[0])

    overlay = speed_change(overlay, bpm/145)
    
    if file_corr!=0:
        file_handle = overlay.export(f"output_beats/{chat_id}_{str(file_corr)}.{extension}", format=f"{extension}")
    else:
        file_handle = overlay.export(f"output_beats/{chat_id}.{extension}", format=f"{extension}")

    return True

def trap(chat_id, bpm, file_corr=0, sample_preset=0, extension='wav'):
    clap = choice([AudioSegment.from_wav(file) for file in glob("style_Trap/clap/*.wav")])
    bass = choice([AudioSegment.from_wav(file) for file in glob("style_Trap/bass/*.wav")])
    hi_hat = choice([AudioSegment.from_wav(file) for file in glob("style_Trap/hi-hat/*.wav")])
    kick = choice([AudioSegment.from_wav(file) for file in glob("style_Trap/kick/*.wav")])
   
    ## sync leads and help_leads ON
    if sample_preset==0: 
        
        leads_sync = randint(1, len(glob("style_Trap/lead/*.wav"))+1)
        
    else:
        leads_sync = sample_preset

    lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_Trap/lead/lead{leads_sync}.wav")])
    help_lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_Trap/helplead/helplead{leads_sync}.wav")])

    ## sync leads and help_leads OFF
    # lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_Trap/lead/*.wav")])
    # help_lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_Trap/helplead/*.wav")])

    ##### ТАКТЫ #####

    # 14 sec 76 milisec

    #150bpm 4sandwich 51sec 20milisec
    #130bpm 4sandwich 59sec 07milisec

    ## 1 ##
    sandwich1 = lead
    sandwich1 = sandwich1.overlay(help_lead, position=0)
    sandwich1 = sandwich1.overlay(clap, position=0)
    sandwich1 = sandwich1.overlay(hi_hat, position=0)
    sandwich1 = sandwich1.overlay(kick, position=0)
    sandwich1 = sandwich1.overlay(bass, position=0)

    sandwich1 = sandwich1[:7380]
    octaves = -1
    new_sample_rate = int(sandwich1.frame_rate * (2.0 ** octaves))
    sandwich1 = sandwich1._spawn(sandwich1.raw_data, overrides={'frame_rate': new_sample_rate})

    overlay = sandwich1

    ## 2 ##
    sandwich2 = lead

    overlay = overlay.append(sandwich2, crossfade=0)

    ## 3 ##
    sandwich3 = lead
    sandwich3 = sandwich3.overlay(help_lead, position=0)
    sandwich3 = sandwich3.overlay(clap, position=0)
    sandwich3 = sandwich3.overlay(hi_hat, position=0)


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
    sandwich5 = sandwich5.overlay(help_lead, position=0)
    sandwich5 = sandwich5.overlay(clap, position=0)
    sandwich5 = sandwich5.overlay(hi_hat, position=0)
    sandwich5 = sandwich5.overlay(kick, position=0)
    sandwich5 = sandwich5.overlay(bass, position=0)

    overlay = overlay.append(sandwich5, crossfade=0)

    ## 6 ##
    sandwich6 = lead
    sandwich6 = sandwich6.overlay(clap, position=0)
    sandwich6 = sandwich6.overlay(hi_hat, position=0)
    sandwich6 = sandwich6.overlay(kick, position=0)
    sandwich6 = sandwich6.overlay(bass, position=0)

    overlay = overlay.append(sandwich6, crossfade=0)

    ## 7 ##
    sandwich7 = lead
    sandwich7 = sandwich7.overlay(help_lead, position=0)
    sandwich7 = sandwich7.overlay(clap, position=0)
    sandwich7 = sandwich7.overlay(hi_hat, position=0)
    sandwich7 = sandwich7.overlay(kick, position=0)
    sandwich7 = sandwich7.overlay(bass, position=0)

    overlay = overlay.append(sandwich7, crossfade=0)

    ## 8 ##
    sandwich8 = lead
    sandwich8 = sandwich8.overlay(help_lead, position=0)
    
    overlay = overlay.append(sandwich8, crossfade=0)

    bpm = int(bpm.split('b')[0])

    if bpm == 130:
        pass       
    else:
        overlay = speed_change(overlay, bpm/130)
    
    if file_corr!=0:
        file_handle = overlay.export(f"output_beats/{chat_id}_{str(file_corr)}.{extension}", format=f"{extension}")
    else:
        file_handle = overlay.export(f"output_beats/{chat_id}.{extension}", format=f"{extension}")
    
    return True