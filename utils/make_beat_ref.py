
import librosa
from pydub import AudioSegment
from random import choice
from glob import glob

class Make_Beat():

    # Изменить темп аудио
    @staticmethod
    def _change_bpm(sound, speed=1.0):
        # Установка частоты кадров вручную. Это говорит компьютеру, сколько
        # образцов воспроизводить в секунду
        sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * speed)
        })

        # Преобразование звука с измененной частотой кадров в стандартную частоту кадров,
        # чтобы обычные программы воспроизведения работали правильно. Они часто умеют
        # воспроизводить звук только на стандартной частоте кадров (например, 44,1 кГц)
        return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

    # Методы стилей.

    @staticmethod
    def jersey_club(chat_id, bpm, file_corr=0, sample_preset=None, bass_preset=None, extension='wav'):
        hi_hat = choice([AudioSegment.from_wav(file) for file in glob("style_JC/hi-hat/*.wav")])
        kick = choice([AudioSegment.from_wav(file) for file in glob("style_JC/kick/*.wav")])
        voicetag = AudioSegment.from_wav('voicetags/beatbot_voicetag_145bpm.wav')

        # bass preset
        if bass_preset is None:
            bass = choice([AudioSegment.from_wav(file) for file in glob("style_JC/bass/*.wav")])
        else:
            bass = AudioSegment.from_wav(f"style_JC/bass/{bass_preset}")
    
        ## sync leads and help_leads ON
        if sample_preset is None: 
            lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_JC/lead/*.wav")])
        else:
            lead = AudioSegment.from_wav(f"style_JC/lead/{sample_preset}")

        ##### ТАКТЫ #####

        # 13240

        ## 1 ##
        sandwich1 = lead
        # sandwich1 = sandwich1.overlay(help_lead, position=0)
        sandwich1 = sandwich1.overlay(voicetag, position=0)
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
        # sandwich2 = sandwich2.overlay(help_lead, position=0)
        sandwich2 = sandwich2.overlay(hi_hat, position=0)

        overlay = overlay.append(sandwich2, crossfade=0)

        ## 3 ##
        sandwich3 = lead
        # sandwich3 = sandwich3.overlay(help_lead, position=0)
        sandwich3 = sandwich3.overlay(hi_hat, position=0)
        sandwich3 = sandwich3.overlay(kick, position=0)
        sandwich3 = sandwich3.overlay(bass, position=0)

        overlay = overlay.append(sandwich3, crossfade=0)

        ## 4 ##
        sandwich4 = lead
        # sandwich4 = sandwich4.overlay(help_lead, position=0)
        sandwich4 = sandwich4.overlay(hi_hat, position=0)
        # Наложение не сразу после начала
        sandwich4 = sandwich4.overlay(kick[3300:], position=3300)
        sandwich4 = sandwich4.overlay(bass[3300:], position=3300)
        
        overlay = overlay.append(sandwich4, crossfade=0)

        ## 5 ##
        sandwich5 = lead
        # sandwich5 = sandwich5.overlay(help_lead, position=0)
        sandwich5 = sandwich5.overlay(hi_hat, position=0)
        sandwich5 = sandwich5.overlay(kick, position=0)
        sandwich5 = sandwich5.overlay(bass, position=0)
    
        overlay = overlay.append(sandwich5, crossfade=0)

        ## 6 ##
        sandwich6 = lead
        # sandwich6 = sandwich6.overlay(help_lead, position=0)
        sandwich6 = sandwich6.overlay(hi_hat, position=0)
        # Наложение не сразу после начала
        sandwich6 = sandwich6.overlay(kick[3300:], position=3300)
        sandwich6 = sandwich6.overlay(bass[3300:], position=3300)

        overlay = overlay.append(sandwich6, crossfade=0)

        ## 7 ##
        sandwich7 = lead
        # sandwich7 = sandwich7.overlay(help_lead, position=0)
        sandwich7 = sandwich7.overlay(hi_hat, position=0)
        sandwich7 = sandwich7.overlay(kick, position=0)
        sandwich7 = sandwich7.overlay(bass, position=0)

        overlay = overlay.append(sandwich7, crossfade=0)

        ## 8 ##
        sandwich8 = lead
        # sandwich8 = sandwich8.overlay(help_lead, position=0)
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
    
    @staticmethod
    def old_school(chat_id, bpm, file_corr=0, sample_preset=None, bass_preset=None, extension='wav'):
        clap = choice([AudioSegment.from_wav(file) for file in glob("style_OldSchool/clap/*.wav")])
        hi_hat = choice([AudioSegment.from_wav(file) for file in glob("style_OldSchool/hi-hat/*.wav")])
        kick = choice([AudioSegment.from_wav(file) for file in glob("style_OldSchool/kick/*.wav")])
        voicetag = AudioSegment.from_wav('voicetags/beatbot_voicetag_170bpm.wav')

        # bass preset
        if bass_preset is None:
            bass = choice([AudioSegment.from_wav(file) for file in glob("style_OldSchool/bass/*.wav")])
        else:
            bass = AudioSegment.from_wav(f"style_OldSchool/bass/{bass_preset}")

        ## sync leads and help_leads ON
        if sample_preset is None: 
            lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_OldSchool/lead/*.wav")])
        else:
            lead = AudioSegment.from_wav(f"style_OldSchool/lead/{sample_preset}")


        # 11290
        ##### ТАКТЫ #####

        ## 1 ##
        sandwich1 = lead

        overlay = sandwich1

        ## 2 ##
        sandwich2 = lead
        sandwich1 = sandwich1.overlay(voicetag, position=0)
        sandwich2 = sandwich2.overlay(hi_hat, position=0)
        sandwich2 = sandwich2.overlay(kick, position=0)

        overlay = overlay.append(sandwich2, crossfade=0)

        ## 3 ##
        sandwich3 = lead
        # sandwich3 = sandwich3.overlay(help_lead, position=0)
        sandwich3 = sandwich3.overlay(clap, position=0)
        sandwich3 = sandwich3.overlay(hi_hat, position=0)
        sandwich3 = sandwich3.overlay(kick, position=0)
        sandwich3 = sandwich3.overlay(bass, position=0)

        overlay = overlay.append(sandwich3, crossfade=0)

        ## 4 ##
        sandwich4 = lead
        # sandwich4 = sandwich4.overlay(help_lead, position=0)
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
        # sandwich6 = sandwich6.overlay(help_lead, position=0)
        sandwich6 = sandwich6.overlay(clap, position=0)
        sandwich6 = sandwich6.overlay(hi_hat, position=0)
        sandwich6 = sandwich6.overlay(kick, position=0)
        sandwich6 = sandwich6.overlay(bass, position=0)

        overlay = overlay.append(sandwich6, crossfade=0)

        ## 7 ##
        sandwich7 = lead
        # sandwich7 = sandwich7.overlay(help_lead, position=0)
        sandwich7 = sandwich7.overlay(clap, position=0)
        sandwich7 = sandwich7.overlay(hi_hat, position=0)
        sandwich7 = sandwich7.overlay(kick, position=0)
        sandwich7 = sandwich7.overlay(bass, position=0)

        overlay = overlay.append(sandwich7, crossfade=0)

        ## 8 ##
        sandwich8 = lead
        # sandwich8 = sandwich8.overlay(help_lead, position=0)
        sandwich8 = sandwich8.overlay(clap, position=0)
        sandwich8 = sandwich8.overlay(hi_hat, position=0)
        sandwich8 = sandwich8.overlay(kick, position=0)
        sandwich8 = sandwich8.overlay(bass, position=0)

        overlay = overlay.append(sandwich8, crossfade=0)

        ## 9 ##
        sandwich9 = lead
        # sandwich9 = sandwich9.overlay(help_lead, position=0)
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

    @staticmethod
    def drill(chat_id, bpm, file_corr=0, sample_preset=None, bass_preset=None, extension='wav'):
        clap = choice([AudioSegment.from_wav(file) for file in glob("style_Drill/clap/*.wav")])
        hi_hat = choice([AudioSegment.from_wav(file) for file in glob("style_Drill/hi-hat/*.wav")])
        kick = choice([AudioSegment.from_wav(file) for file in glob("style_Drill/kick/*.wav")])
        voicetag = AudioSegment.from_wav('voicetags/beatbot_voicetag_130bpm.wav')
    
        # bass preset
        if bass_preset is None:
            bass = choice([AudioSegment.from_wav(file) for file in glob("style_Drill/bass/*.wav")])
        else:
            bass = AudioSegment.from_wav(f"style_Drill/bass/{bass_preset}")
        
        ## sync leads and help_leads ON
        if sample_preset is None: 
            lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_Drill/lead/*.wav")])
        else:
            lead = AudioSegment.from_wav(f"style_Drill/lead/{sample_preset}")

        ## sync leads and help_leads OFF
        # lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_Drill/lead/*.wav")])
        # help_lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_Drill/helplead/*.wav")])

        ##### ТАКТЫ #####

        # 14 sec 76 milisec

        ## 1 ##
        sandwich1 = lead
        # sandwich1 = sandwich1.overlay(help_lead, position=0)
        sandwich1 = sandwich1.overlay(voicetag, position=0)
        sandwich1 = sandwich1.overlay(hi_hat[:-1840], position=-1840)
        sandwich1 = sandwich1.overlay(clap[:-1840], position=-1840)

        overlay = sandwich1

        ## 2 ##
        sandwich2 = lead
        sandwich2 = sandwich2.overlay(bass, position=0)
        sandwich2 = sandwich2.overlay(clap, position=0)
        sandwich2 = sandwich2.overlay(hi_hat[:-460], position=0)
        sandwich2 = sandwich2.overlay(kick[920:], position=920)

        overlay = overlay.append(sandwich2, crossfade=0)

        ## 3 ##
        sandwich3 = lead
        # sandwich3 = sandwich3.overlay(help_lead, position=0)
        sandwich3 = sandwich3.overlay(clap, position=0)
        sandwich3 = sandwich3.overlay(hi_hat, position=0)
        sandwich3 = sandwich3.overlay(kick, position=0)
        sandwich3 = sandwich3.overlay(bass, position=0)

        overlay = overlay.append(sandwich3, crossfade=0)

        ## 4 ##
        sandwich4 = lead
        # sandwich4 = sandwich4.overlay(help_lead, position=0)
        sandwich4 = sandwich4.overlay(clap, position=0)
        sandwich4 = sandwich4.overlay(hi_hat, position=0)
        sandwich4 = sandwich4.overlay(kick[:-920], position=-920)
        sandwich4 = sandwich4.overlay(bass, position=0)
        
        overlay = overlay.append(sandwich4, crossfade=0)

        ## 5 ##
        sandwich5 = lead
        # sandwich5 = sandwich5.overlay(help_lead, position=0)
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
        sandwich7 = sandwich7.overlay(clap, position=0)
        sandwich7 = sandwich7.overlay(hi_hat[:-460], position=0)
        sandwich7 = sandwich7.overlay(kick[:-460], position=0)
        sandwich7 = sandwich7.overlay(bass, position=0)

        overlay = overlay.append(sandwich7, crossfade=0)

        ## 8 ##
        sandwich8 = lead
        sandwich8 = sandwich8.overlay(bass[2300:], position=2300)
        sandwich8 = sandwich8.overlay(hi_hat, position=0)
        sandwich8 = sandwich8.overlay(clap, position=0)
        sandwich8 = sandwich8.overlay(kick, position=0)

        overlay = overlay.append(sandwich8, crossfade=0)

        ## 9 ##
        sandwich9 = lead
        sandwich9 = sandwich9.overlay(bass, position=0)
        sandwich9 = sandwich9.overlay(hi_hat[:-460], position=0)
        sandwich9 = sandwich9.overlay(clap[:-460], position=0)
        sandwich9 = sandwich9.overlay(kick[:-460], position=0)

        overlay = overlay.append(sandwich9, crossfade=0)

        ## 10 ##
        sandwich10 = lead
        sandwich10 = sandwich10.overlay(voicetag, position=0)

        overlay = overlay.append(sandwich10, crossfade=0)

        bpm = int(bpm.split('b')[0])

        if bpm == 130:
            pass       
        else:
            overlay = speed_change(overlay, bpm/130)

        # Максимальная амплитуда для клиппера (в децибелах)
        max_amplitude = -3  # Здесь можно настроить желаемую амплитуду

        # Применение клиппера ко всему оверлею
        overlay = apply_clipper(overlay, max_amplitude)

        
        if file_corr!=0:
            file_handle = overlay.export(f"output_beats/{chat_id}_{str(file_corr)}.{extension}", format=f"{extension}")
        else:
            file_handle = overlay.export(f"output_beats/{chat_id}.{extension}", format=f"{extension}")
        
        return True

    @staticmethod
    def plug(chat_id, bpm, file_corr=0, sample_preset=None, bass_preset=None, extension='wav'):
        clap = choice([AudioSegment.from_wav(file) for file in glob("style_Plug/clap/*.wav")])
        hi_hat = choice([AudioSegment.from_wav(file) for file in glob("style_Plug/hi-hat/*.wav")])
        kick = choice([AudioSegment.from_wav(file) for file in glob("style_Plug/kick/*.wav")])
        voicetag = AudioSegment.from_wav('voicetags/beatbot_voicetag_145bpm.wav')
    
        # bass preset
        if bass_preset is None:
            bass = choice([AudioSegment.from_wav(file) for file in glob("style_Plug/bass/*.wav")])
        else:
            bass = AudioSegment.from_wav(f"style_Plug/bass/{bass_preset}")
        
        # sync leads and help_leads ON
        if sample_preset is None: 
            lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_Plug/lead/*.wav")])
        else:
            lead = AudioSegment.from_wav(f"style_Plug/lead/{sample_preset}")

        ## sync leads and help_leads OFF
        # lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_Plug/lead/*.wav")])
        # help_lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_Plug/helplead/*.wav")])

        ##### ТАКТЫ #####

        # 14 sec 76 milisec

        ## 1 ##
        sandwich1 = lead
        # sandwich1 = sandwich1.overlay(help_lead, position=0)
        sandwich1 = sandwich1.overlay(voicetag, position=0)
        sandwich1 = sandwich1.overlay(hi_hat[:-1840], position=-1840)
        sandwich1 = sandwich1.overlay(clap[:-1840], position=-1840)

        overlay = sandwich1

        ## 2 ##
        sandwich2 = lead
        sandwich2 = sandwich2.overlay(bass, position=0)
        sandwich2 = sandwich2.overlay(clap, position=0)
        sandwich2 = sandwich2.overlay(hi_hat[:-460], position=0)
        sandwich2 = sandwich2.overlay(kick[920:], position=920)

        overlay = overlay.append(sandwich2, crossfade=0)

        ## 3 ##
        sandwich3 = lead
        # sandwich3 = sandwich3.overlay(help_lead, position=0)
        sandwich3 = sandwich3.overlay(clap, position=0)
        sandwich3 = sandwich3.overlay(hi_hat, position=0)
        sandwich3 = sandwich3.overlay(kick, position=0)
        sandwich3 = sandwich3.overlay(bass, position=0)

        overlay = overlay.append(sandwich3, crossfade=0)

        ## 4 ##
        sandwich4 = lead
        # sandwich4 = sandwich4.overlay(help_lead, position=0)
        sandwich4 = sandwich4.overlay(clap, position=0)
        sandwich4 = sandwich4.overlay(hi_hat, position=0)
        sandwich4 = sandwich4.overlay(kick[:-920], position=-920)
        sandwich4 = sandwich4.overlay(bass, position=0)
        
        overlay = overlay.append(sandwich4, crossfade=0)

        ## 5 ##
        sandwich5 = lead
        # sandwich5 = sandwich5.overlay(help_lead, position=0)
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
        sandwich7 = sandwich7.overlay(clap, position=0)
        sandwich7 = sandwich7.overlay(hi_hat[:-460], position=0)
        sandwich7 = sandwich7.overlay(kick[:-460], position=0)
        sandwich7 = sandwich7.overlay(bass, position=0)

        overlay = overlay.append(sandwich7, crossfade=0)

        ## 8 ##
        sandwich8 = lead
        sandwich8 = sandwich8.overlay(bass[2300:], position=2300)
        sandwich8 = sandwich8.overlay(hi_hat, position=0)
        sandwich8 = sandwich8.overlay(clap, position=0)
        sandwich8 = sandwich8.overlay(kick, position=0)

        overlay = overlay.append(sandwich8, crossfade=0)

        ## 9 ##
        sandwich9 = lead
        sandwich9 = sandwich9.overlay(bass, position=0)
        sandwich9 = sandwich9.overlay(hi_hat[:-460], position=0)
        sandwich9 = sandwich9.overlay(clap[:-460], position=0)
        sandwich9 = sandwich9.overlay(kick[:-460], position=0)

        overlay = overlay.append(sandwich9, crossfade=0)

        ## 10 ##
        sandwich10 = lead
        sandwich10 = sandwich10.overlay(voicetag, position=0)

        overlay = overlay.append(sandwich10, crossfade=0)

        bpm = int(bpm.split('b')[0])

        overlay = speed_change(overlay, bpm/145)
        
        if file_corr!=0:
            file_handle = overlay.export(f"output_beats/{chat_id}_{str(file_corr)}.{extension}", format=f"{extension}")
        else:
            file_handle = overlay.export(f"output_beats/{chat_id}.{extension}", format=f"{extension}")

        return True

    @staticmethod
    def trap(harmony, key, chat_id, bpm, file_corr=None, sample_preset=None, bass_preset=None, extension='wav'):
        clap = choice([AudioSegment.from_wav(file) for file in glob("style_Trap/clap/*.wav")])
        kick = choice([AudioSegment.from_wav(file) for file in glob("style_Trap/kick/*.wav")])
        hi_hat = choice([AudioSegment.from_wav(file) for file in glob("style_Trap/hi-hat/*.wav")])
        voicetag = AudioSegment.from_wav('voicetags/beatbot_voicetag_130bpm.wav')

        bass = AudioSegment.from_wav(f"style_Trap/bass/{harmony}/{bass_preset}")
        lead = AudioSegment.from_wav(f"style_Trap/lead/{harmony}/{sample_preset}")

        print(sample_preset, bass_preset)

        ##### ТАКТЫ #####

        # 14 sec 76 milisec

        ## 1 ##
        sandwich1 = lead
        # sandwich1 = sandwich1.overlay(help_lead, position=0)
        sandwich1 = sandwich1.overlay(voicetag, position=0)
        sandwich1 = sandwich1.overlay(hi_hat[:-1840], position=-1840)
        sandwich1 = sandwich1.overlay(clap[:-1840], position=-1840)

        overlay = sandwich1

        ## 2 ##
        sandwich2 = lead
        sandwich2 = sandwich2.overlay(bass, position=0)
        sandwich2 = sandwich2.overlay(clap, position=0)
        sandwich2 = sandwich2.overlay(hi_hat[:-460], position=0)
        sandwich2 = sandwich2.overlay(kick[920:], position=920)

        overlay = overlay.append(sandwich2, crossfade=0)

        ## 3 ##
        sandwich3 = lead
        # sandwich3 = sandwich3.overlay(help_lead, position=0)
        sandwich3 = sandwich3.overlay(clap, position=0)
        sandwich3 = sandwich3.overlay(hi_hat, position=0)
        sandwich3 = sandwich3.overlay(kick, position=0)
        sandwich3 = sandwich3.overlay(bass, position=0)

        overlay = overlay.append(sandwich3, crossfade=0)

        ## 4 ##
        sandwich4 = lead
        # sandwich4 = sandwich4.overlay(help_lead, position=0)
        sandwich4 = sandwich4.overlay(clap, position=0)
        sandwich4 = sandwich4.overlay(hi_hat, position=0)
        sandwich4 = sandwich4.overlay(kick[:-920], position=-920)
        sandwich4 = sandwich4.overlay(bass, position=0)
        
        overlay = overlay.append(sandwich4, crossfade=0)

        ## 5 ##
        sandwich5 = lead
        # sandwich5 = sandwich5.overlay(help_lead, position=0)
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
        sandwich7 = sandwich7.overlay(clap, position=0)
        sandwich7 = sandwich7.overlay(hi_hat[:-460], position=0)
        sandwich7 = sandwich7.overlay(kick[:-460], position=0)
        sandwich7 = sandwich7.overlay(bass, position=0)

        overlay = overlay.append(sandwich7, crossfade=0)

        ## 8 ##
        sandwich8 = lead
        sandwich8 = sandwich8.overlay(bass[2300:], position=2300)
        sandwich8 = sandwich8.overlay(hi_hat, position=0)
        sandwich8 = sandwich8.overlay(clap, position=0)
        sandwich8 = sandwich8.overlay(kick, position=0)

        overlay = overlay.append(sandwich8, crossfade=0)

        ## 9 ##
        sandwich9 = lead
        sandwich9 = sandwich9.overlay(bass, position=0)
        sandwich9 = sandwich9.overlay(hi_hat[:-460], position=0)
        sandwich9 = sandwich9.overlay(clap[:-460], position=0)
        sandwich9 = sandwich9.overlay(kick[:-460], position=0)

        overlay = overlay.append(sandwich9, crossfade=0)

        ## 10 ##
        sandwich10 = lead
        sandwich10 = sandwich10.overlay(voicetag, position=0)

        overlay = overlay.append(sandwich10, crossfade=0)

        bpm = int(bpm.split('b')[0])

        if bpm == 130:
            pass       
        else:
            overlay = speed_change(overlay, bpm/130)

        # Максимальная амплитуда для клиппера (в децибелах)
        max_amplitude = -3  # Здесь можно настроить желаемую амплитуду

        # Применение клиппера ко всему оверлею
        overlay = apply_clipper(overlay, max_amplitude)

        
        if file_corr!=0:
            file_handle = overlay.export(f"output_beats/{chat_id}_{str(file_corr)}.{extension}", format=f"{extension}")
        else:
            file_handle = overlay.export(f"output_beats/{chat_id}.{extension}", format=f"{extension}")
        
        return True

    @staticmethod
    def opium(chat_id, bpm, file_corr=0, sample_preset=None, bass_preset=None, extension='wav'):
        clap = choice([AudioSegment.from_wav(file) for file in glob("style_Opium/clap/*.wav")])
        hi_hat = choice([AudioSegment.from_wav(file) for file in glob("style_Opium/hi-hat/*.wav")])
        kick = choice([AudioSegment.from_wav(file) for file in glob("style_Plug/kick/*.wav")])
        voicetag = AudioSegment.from_wav('voicetags/beatbot_voicetag_145bpm.wav')

        # bass preset
        if bass_preset is None:
            bass = choice([AudioSegment.from_wav(file) for file in glob("style_Opium/bass/*.wav")])
        else:
            bass = AudioSegment.from_wav(f"style_Opium/bass/{bass_preset}")
        
        ## sync leads and help_leads ON
        if sample_preset is None: 
            lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_Opium/lead/*.wav")])
        else:
            lead = AudioSegment.from_wav(f"style_Opium/lead/{sample_preset}")

            ##### ТАКТЫ #####

        # 14 sec 76 milisec

        ## 1 ##
        sandwich1 = lead
        # sandwich1 = sandwich1.overlay(help_lead, position=0)
        sandwich1 = sandwich1.overlay(voicetag, position=0)
        sandwich1 = sandwich1.overlay(hi_hat[:-1840], position=-1840)
        sandwich1 = sandwich1.overlay(clap[:-1840], position=-1840)

        overlay = sandwich1

        ## 2 ##
        sandwich2 = lead
        sandwich2 = sandwich2.overlay(bass, position=0)
        sandwich2 = sandwich2.overlay(clap, position=0)
        sandwich2 = sandwich2.overlay(hi_hat[:-460], position=0)
        sandwich2 = sandwich2.overlay(kick[920:], position=920)

        overlay = overlay.append(sandwich2, crossfade=0)

        ## 3 ##
        sandwich3 = lead
        # sandwich3 = sandwich3.overlay(help_lead, position=0)
        sandwich3 = sandwich3.overlay(clap, position=0)
        sandwich3 = sandwich3.overlay(hi_hat, position=0)
        sandwich3 = sandwich3.overlay(kick, position=0)
        sandwich3 = sandwich3.overlay(bass, position=0)

        overlay = overlay.append(sandwich3, crossfade=0)

        ## 4 ##
        sandwich4 = lead
        # sandwich4 = sandwich4.overlay(help_lead, position=0)
        sandwich4 = sandwich4.overlay(clap, position=0)
        sandwich4 = sandwich4.overlay(hi_hat, position=0)
        sandwich4 = sandwich4.overlay(kick[:-920], position=-920)
        sandwich4 = sandwich4.overlay(bass, position=0)
        
        overlay = overlay.append(sandwich4, crossfade=0)

        ## 5 ##
        sandwich5 = lead
        # sandwich5 = sandwich5.overlay(help_lead, position=0)
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
        sandwich7 = sandwich7.overlay(clap, position=0)
        sandwich7 = sandwich7.overlay(hi_hat[:-460], position=0)
        sandwich7 = sandwich7.overlay(kick[:-460], position=0)
        sandwich7 = sandwich7.overlay(bass, position=0)

        overlay = overlay.append(sandwich7, crossfade=0)

        ## 8 ##
        sandwich8 = lead
        sandwich8 = sandwich8.overlay(bass[2300:], position=2300)
        sandwich8 = sandwich8.overlay(hi_hat, position=0)
        sandwich8 = sandwich8.overlay(clap, position=0)
        sandwich8 = sandwich8.overlay(kick, position=0)

        overlay = overlay.append(sandwich8, crossfade=0)

        ## 9 ##
        sandwich9 = lead
        sandwich9 = sandwich9.overlay(bass, position=0)
        sandwich9 = sandwich9.overlay(hi_hat[:-460], position=0)
        sandwich9 = sandwich9.overlay(clap[:-460], position=0)
        sandwich9 = sandwich9.overlay(kick[:-460], position=0)

        overlay = overlay.append(sandwich9, crossfade=0)

        ## 10 ##
        sandwich10 = lead
        sandwich10 = sandwich10.overlay(voicetag, position=0)

        overlay = overlay.append(sandwich10, crossfade=0)

        bpm = int(bpm.split('b')[0])

        if bpm == 145:
            pass       
        else:
            overlay = speed_change(overlay, bpm/145)

        # Максимальная амплитуда для клиппера (в децибелах)
        max_amplitude = -3  # Здесь можно настроить желаемую амплитуду

        # Применение клиппера ко всему оверлею
        overlay = apply_clipper(overlay, max_amplitude)

        
        if file_corr!=0:
            file_handle = overlay.export(f"output_beats/{chat_id}_{str(file_corr)}.{extension}", format=f"{extension}")
        else:
            file_handle = overlay.export(f"output_beats/{chat_id}.{extension}", format=f"{extension}")
        
        return True

    @staticmethod
    def newjazz(chat_id, bpm, file_corr=0, sample_preset=None, extension='wav'):
        clap = choice([AudioSegment.from_wav(file) for file in glob("style_NewJazz/clap/*.wav")])
        hi_hat = choice([AudioSegment.from_wav(file) for file in glob("style_NewJazz/hi-hat/*.wav")])
        kick = choice([AudioSegment.from_wav(file) for file in glob("style_NewJazz/kick/*.wav")])
        voicetag = AudioSegment.from_wav('voicetags/beatbot_voicetag_130bpm.wav')

        ## sync leads and help_leads ON
        if sample_preset is None: 
            lead = choice([AudioSegment.from_wav(file) for file in glob(f"style_NewJazz/lead/*.wav")])
        else:
            lead = AudioSegment.from_wav(f"style_NewJazz/lead/{sample_preset}")

        ##### ТАКТЫ #####

        # 14 sec 76 milisec

        ## 1 ##
        sandwich1 = lead
        # sandwich1 = sandwich1.overlay(help_lead, position=0)
        sandwich1 = sandwich1.overlay(voicetag, position=0)
        sandwich1 = sandwich1.overlay(hi_hat[:-1840], position=-1840)
        sandwich1 = sandwich1.overlay(clap[:-1840], position=-1840)

        overlay = sandwich1

        ## 2 ##
        sandwich2 = lead
        sandwich2 = sandwich2.overlay(clap, position=0)
        sandwich2 = sandwich2.overlay(hi_hat[:-460], position=0)
        sandwich2 = sandwich2.overlay(kick[920:], position=920)

        overlay = overlay.append(sandwich2, crossfade=0)

        ## 3 ##
        sandwich3 = lead
        # sandwich3 = sandwich3.overlay(help_lead, position=0)
        sandwich3 = sandwich3.overlay(clap, position=0)
        sandwich3 = sandwich3.overlay(hi_hat, position=0)
        sandwich3 = sandwich3.overlay(kick, position=0)

        overlay = overlay.append(sandwich3, crossfade=0)

        ## 4 ##
        sandwich4 = lead
        # sandwich4 = sandwich4.overlay(help_lead, position=0)
        sandwich4 = sandwich4.overlay(clap, position=0)
        sandwich4 = sandwich4.overlay(hi_hat, position=0)
        sandwich4 = sandwich4.overlay(kick[:-920], position=-920)
        
        overlay = overlay.append(sandwich4, crossfade=0)

        ## 5 ##
        sandwich5 = lead
        # sandwich5 = sandwich5.overlay(help_lead, position=0)
        sandwich5 = sandwich5.overlay(clap, position=0)
        sandwich5 = sandwich5.overlay(hi_hat, position=0)
        sandwich5 = sandwich5.overlay(kick, position=0)

        overlay = overlay.append(sandwich5, crossfade=0)

        ## 6 ##
        sandwich6 = lead
        sandwich6 = sandwich6.overlay(clap, position=0)
        sandwich6 = sandwich6.overlay(hi_hat, position=0)
        sandwich6 = sandwich6.overlay(kick, position=0)

        overlay = overlay.append(sandwich6, crossfade=0)

        ## 7 ##
        sandwich7 = lead
        sandwich7 = sandwich7.overlay(clap, position=0)
        sandwich7 = sandwich7.overlay(hi_hat[:-460], position=0)
        sandwich7 = sandwich7.overlay(kick[:-460], position=0)

        overlay = overlay.append(sandwich7, crossfade=0)

        ## 8 ##
        sandwich8 = lead
        sandwich8 = sandwich8.overlay(hi_hat, position=0)
        sandwich8 = sandwich8.overlay(clap, position=0)
        sandwich8 = sandwich8.overlay(kick, position=0)

        overlay = overlay.append(sandwich8, crossfade=0)

        ## 9 ##
        sandwich9 = lead
        sandwich9 = sandwich9.overlay(hi_hat[:-460], position=0)
        sandwich9 = sandwich9.overlay(clap[:-460], position=0)
        sandwich9 = sandwich9.overlay(kick[:-460], position=0)

        overlay = overlay.append(sandwich9, crossfade=0)

        ## 10 ##
        sandwich10 = lead
        sandwich10 = sandwich10.overlay(voicetag, position=0)

        overlay = overlay.append(sandwich10, crossfade=0)

        bpm = int(bpm.split('b')[0])

        if bpm == 130:
            pass       
        else:
            overlay = speed_change(overlay, bpm/130)

        # Максимальная амплитуда для клиппера (в децибелах)
        max_amplitude = -3  # Здесь можно настроить желаемую амплитуду

        # Применение клиппера ко всему оверлею
        overlay = apply_clipper(overlay, max_amplitude)

        
        if file_corr!=0:
            file_handle = overlay.export(f"output_beats/{chat_id}_{str(file_corr)}.{extension}", format=f"{extension}")
        else:
            file_handle = overlay.export(f"output_beats/{chat_id}.{extension}", format=f"{extension}")
        
        return True