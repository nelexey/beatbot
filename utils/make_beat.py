
from pydub import AudioSegment
from random import choice
from glob import glob
from utils.audio_action import Audio_Action

class Make_Beat():

    # Функция для инициализации генерации.
    @staticmethod
    def make_beat(style, filename, extension, bpm, lead_path, bass_path):
        if style=='Jersey Club':
            Make_Beat._jersey_club(filename, lead_path, bass_path, bpm, extension)
        elif style=='Trap':
            Make_Beat._trap(filename, lead_path, bass_path, bpm, extension)
        elif style=='Drill':
            Make_Beat._drill(filename, lead_path, bass_path, bpm, extension)
        elif style=='Plug':
            Make_Beat._plug(filename, lead_path, bass_path, bpm, extension)
        elif style=='Old School':
            Make_Beat._old_school(filename, lead_path, bass_path, bpm, extension)
        elif style=='Opium':
            Make_Beat._opium(filename, lead_path, bass_path, bpm, extension)
        elif style=='NewJazz':
            Make_Beat._newjazz(filename, lead_path, bpm, extension)
    
    # Методы стилей.

    @staticmethod
    def _jersey_club(filename, lead_path, bass_path, bpm, extension='wav'):
        hi_hat = choice([AudioSegment.from_wav(file) for file in glob("sounds/style_JC/hi-hat/*.wav")])
        kick = choice([AudioSegment.from_wav(file) for file in glob("sounds/style_JC/kick/*.wav")])
        voicetag = AudioSegment.from_wav('sounds/voicetags/beatbot_voicetag_145bpm.wav')

        lead = AudioSegment.from_wav(lead_path)
        bass = AudioSegment.from_wav(bass_path)

        ##### ТАКТЫ #####

        ## 1 ##
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

        ## 2 ##

        sandwich2 = lead
        sandwich2 = sandwich2.overlay(hi_hat, position=0)

        overlay = overlay.append(sandwich2, crossfade=0)

        ## 3 ##
        sandwich3 = lead
        sandwich3 = sandwich3.overlay(hi_hat, position=0)
        sandwich3 = sandwich3.overlay(kick, position=0)
        sandwich3 = sandwich3.overlay(bass, position=0)

        overlay = overlay.append(sandwich3, crossfade=0)

        ## 4 ##
        sandwich4 = lead
        sandwich4 = sandwich4.overlay(hi_hat, position=0)
        # Наложение не сразу после начала.
        sandwich4 = sandwich4.overlay(kick[3300:], position=3300)
        sandwich4 = sandwich4.overlay(bass[3300:], position=3300)
        
        overlay = overlay.append(sandwich4, crossfade=0)

        ## 5 ##
        sandwich5 = lead
        sandwich5 = sandwich5.overlay(hi_hat, position=0)
        sandwich5 = sandwich5.overlay(kick, position=0)
        sandwich5 = sandwich5.overlay(bass, position=0)
    
        overlay = overlay.append(sandwich5, crossfade=0)

        ## 6 ##
        sandwich6 = lead
        sandwich6 = sandwich6.overlay(hi_hat, position=0)
        # Наложение не сразу после начала.
        sandwich6 = sandwich6.overlay(kick[3300:], position=3300)
        sandwich6 = sandwich6.overlay(bass[3300:], position=3300)

        overlay = overlay.append(sandwich6, crossfade=0)

        ## 7 ##
        sandwich7 = lead
        sandwich7 = sandwich7.overlay(hi_hat, position=0)
        sandwich7 = sandwich7.overlay(kick, position=0)
        sandwich7 = sandwich7.overlay(bass, position=0)

        overlay = overlay.append(sandwich7, crossfade=0)

        ## 8 ##
        sandwich8 = lead
        sandwich8 = sandwich8.overlay(hi_hat, position=0)
        
        overlay = overlay.append(sandwich8, crossfade=0)

        ## 9 ##
        sandwich9 = lead
        
        overlay = overlay.append(sandwich9, crossfade=0)

        bpm = int(bpm.split('b')[0])

        overlay = Audio_Action.change_bpm(overlay, bpm/145)

        # Максимальная амплитуда для клиппера (в децибелах)
        threshold = 0.5 # Здесь можно настроить желаемую амплитуду

        # Применение клиппера ко всему оверлею
        overlay = Audio_Action.apply_clipper(overlay, threshold)
        
        overlay.export(f"output_beats/{filename}.{extension}", format=extension)

        return True
    
    @staticmethod
    def _trap(filename, lead_path, bass_path, bpm, extension='wav'):
        clap = choice([AudioSegment.from_wav(file) for file in glob("sounds/style_Trap/clap/*.wav")])
        kick = choice([AudioSegment.from_wav(file) for file in glob("sounds/style_Trap/kick/*.wav")])
        hi_hat = choice([AudioSegment.from_wav(file) for file in glob("sounds/style_Trap/hi-hat/*.wav")])
        voicetag = AudioSegment.from_wav('sounds/voicetags/beatbot_voicetag_130bpm.wav')

        lead = AudioSegment.from_wav(lead_path)
        bass = AudioSegment.from_wav(bass_path)

        ##### ТАКТЫ #####

        ## 1 ##
        sandwich1 = lead
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
        sandwich3 = sandwich3.overlay(clap, position=0)
        sandwich3 = sandwich3.overlay(hi_hat, position=0)
        sandwich3 = sandwich3.overlay(kick, position=0)
        sandwich3 = sandwich3.overlay(bass, position=0)

        overlay = overlay.append(sandwich3, crossfade=0)

        ## 4 ##
        sandwich4 = lead
        sandwich4 = sandwich4.overlay(clap, position=0)
        sandwich4 = sandwich4.overlay(hi_hat, position=0)
        sandwich4 = sandwich4.overlay(kick[:-920], position=-920)
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
            overlay = Audio_Action.change_bpm(overlay, bpm/130)

        # Максимальная амплитуда для клиппера (в децибелах)
        threshold = 0.5 # Здесь можно настроить желаемую амплитуду

        # Применение клиппера ко всему оверлею
        overlay = Audio_Action.apply_clipper(overlay, threshold)

        overlay.export(f"output_beats/{filename}.{extension}", format=f"{extension}")
        
        return True

    @staticmethod
    def _drill(filename, lead_path, bass_path, bpm, extension='wav'):
        clap = choice([AudioSegment.from_wav(file) for file in glob("sounds/style_Drill/clap/*.wav")])
        hi_hat = choice([AudioSegment.from_wav(file) for file in glob("sounds/style_Drill/hi-hat/*.wav")])
        kick = choice([AudioSegment.from_wav(file) for file in glob("sounds/style_Drill/kick/*.wav")])
        voicetag = AudioSegment.from_wav('sounds/voicetags/beatbot_voicetag_130bpm.wav')
    
        lead = AudioSegment.from_wav(lead_path)
        bass = AudioSegment.from_wav(bass_path)

        ##### ТАКТЫ #####

        ## 1 ##
        sandwich1 = lead
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
        sandwich3 = sandwich3.overlay(clap, position=0)
        sandwich3 = sandwich3.overlay(hi_hat, position=0)
        sandwich3 = sandwich3.overlay(kick, position=0)
        sandwich3 = sandwich3.overlay(bass, position=0)

        overlay = overlay.append(sandwich3, crossfade=0)

        ## 4 ##
        sandwich4 = lead
        sandwich4 = sandwich4.overlay(clap, position=0)
        sandwich4 = sandwich4.overlay(hi_hat, position=0)
        sandwich4 = sandwich4.overlay(kick[:-920], position=-920)
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
            overlay = Audio_Action.change_bpm(overlay, bpm/130)

        # Максимальная амплитуда для клиппера (в децибелах)
        threshold = 0.5 # Здесь можно настроить желаемую амплитуду

        # Применение клиппера ко всему оверлею
        overlay = Audio_Action.apply_clipper(overlay, threshold)

        overlay.export(f"output_beats/{filename}.{extension}", format=f"{extension}")
        
        return True

    @staticmethod
    def _plug(filename, lead_path, bass_path, bpm, extension='wav'):
        clap = choice([AudioSegment.from_wav(file) for file in glob("sounds/style_Plug/clap/*.wav")])
        hi_hat = choice([AudioSegment.from_wav(file) for file in glob("sounds/style_Plug/hi-hat/*.wav")])
        kick = choice([AudioSegment.from_wav(file) for file in glob("sounds/style_Plug/kick/*.wav")])
        voicetag = AudioSegment.from_wav('sounds/voicetags/beatbot_voicetag_145bpm.wav')
    
        lead = AudioSegment.from_wav(lead_path)
        bass = AudioSegment.from_wav(bass_path)

        ##### ТАКТЫ #####

        ## 1 ##
        sandwich1 = lead
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
        sandwich3 = sandwich3.overlay(clap, position=0)
        sandwich3 = sandwich3.overlay(hi_hat, position=0)
        sandwich3 = sandwich3.overlay(kick, position=0)
        sandwich3 = sandwich3.overlay(bass, position=0)

        overlay = overlay.append(sandwich3, crossfade=0)

        ## 4 ##
        sandwich4 = lead
        sandwich4 = sandwich4.overlay(clap, position=0)
        sandwich4 = sandwich4.overlay(hi_hat, position=0)
        sandwich4 = sandwich4.overlay(kick[:-920], position=-920)
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

        overlay = Audio_Action.change_bpm(overlay, bpm/145)

        # Максимальная амплитуда для клиппера (в децибелах)
        threshold = 0.5 # Здесь можно настроить желаемую амплитуду

        # Применение клиппера ко всему оверлею
        overlay = Audio_Action.apply_clipper(overlay, threshold)
        
        overlay.export(f"output_beats/{filename}.{extension}", format=f"{extension}")

        return True

    @staticmethod
    def _old_school(filename, lead_path, bass_path, bpm, extension='wav'):
        clap = choice([AudioSegment.from_wav(file) for file in glob("sounds/style_OldSchool/clap/*.wav")])
        hi_hat = choice([AudioSegment.from_wav(file) for file in glob("sounds/style_OldSchool/hi-hat/*.wav")])
        kick = choice([AudioSegment.from_wav(file) for file in glob("sounds/style_OldSchool/kick/*.wav")])
        voicetag = AudioSegment.from_wav('sounds/voicetags/beatbot_voicetag_170bpm.wav')

        lead = AudioSegment.from_wav(lead_path)
        bass = AudioSegment.from_wav(bass_path)
       
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
        sandwich3 = sandwich3.overlay(clap, position=0)
        sandwich3 = sandwich3.overlay(hi_hat, position=0)
        sandwich3 = sandwich3.overlay(kick, position=0)
        sandwich3 = sandwich3.overlay(bass, position=0)

        overlay = overlay.append(sandwich3, crossfade=0)

        ## 4 ##
        sandwich4 = lead
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
        sandwich6 = sandwich6.overlay(clap, position=0)
        sandwich6 = sandwich6.overlay(hi_hat, position=0)
        sandwich6 = sandwich6.overlay(kick, position=0)
        sandwich6 = sandwich6.overlay(bass, position=0)

        overlay = overlay.append(sandwich6, crossfade=0)

        ## 7 ##
        sandwich7 = lead
        sandwich7 = sandwich7.overlay(clap, position=0)
        sandwich7 = sandwich7.overlay(hi_hat, position=0)
        sandwich7 = sandwich7.overlay(kick, position=0)
        sandwich7 = sandwich7.overlay(bass, position=0)

        overlay = overlay.append(sandwich7, crossfade=0)

        ## 8 ##
        sandwich8 = lead
        sandwich8 = sandwich8.overlay(clap, position=0)
        sandwich8 = sandwich8.overlay(hi_hat, position=0)
        sandwich8 = sandwich8.overlay(kick, position=0)
        sandwich8 = sandwich8.overlay(bass, position=0)

        overlay = overlay.append(sandwich8, crossfade=0)

        ## 9 ##
        sandwich9 = lead
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
            overlay = Audio_Action.change_bpm(overlay, bpm/170)
        
        # Максимальная амплитуда для клиппера (в децибелах)
        threshold = 0.5 # Здесь можно настроить желаемую амплитуду

        # Применение клиппера ко всему оверлею
        overlay = Audio_Action.apply_clipper(overlay, threshold)

        overlay.export(f"output_beats/{filename}.{extension}", format=f"{extension}")

        return True

    @staticmethod
    def _opium(filename, lead_path, bass_path, bpm, extension='wav'):
        clap = choice([AudioSegment.from_wav(file) for file in glob("sounds/style_Opium/clap/*.wav")])
        hi_hat = choice([AudioSegment.from_wav(file) for file in glob("sounds/style_Opium/hi-hat/*.wav")])
        kick = choice([AudioSegment.from_wav(file) for file in glob("sounds/style_Opium/kick/*.wav")])
        voicetag = AudioSegment.from_wav('sounds/voicetags/beatbot_voicetag_145bpm.wav')

        lead = AudioSegment.from_wav(lead_path)
        bass = AudioSegment.from_wav(bass_path)

        ##### ТАКТЫ #####

        ## 1 ##
        sandwich1 = lead
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
        sandwich3 = sandwich3.overlay(clap, position=0)
        sandwich3 = sandwich3.overlay(hi_hat, position=0)
        sandwich3 = sandwich3.overlay(kick, position=0)
        sandwich3 = sandwich3.overlay(bass, position=0)

        overlay = overlay.append(sandwich3, crossfade=0)

        ## 4 ##
        sandwich4 = lead
        sandwich4 = sandwich4.overlay(clap, position=0)
        sandwich4 = sandwich4.overlay(hi_hat, position=0)
        sandwich4 = sandwich4.overlay(kick[:-920], position=-920)
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
            overlay = Audio_Action.change_bpm(overlay, bpm/145)

        # Максимальная амплитуда для клиппера (в децибелах)
        threshold = 0.5 # Здесь можно настроить желаемую амплитуду

        # Применение клиппера ко всему оверлею
        overlay = Audio_Action.apply_clipper(overlay, threshold)

        overlay.export(f"output_beats/{filename}.{extension}", format=f"{extension}")
        
        return True

    @staticmethod
    def _newjazz(filename, lead_path, bpm, extension='wav'):
        clap = choice([AudioSegment.from_wav(file) for file in glob("sounds/style_NewJazz/clap/*.wav")])
        hi_hat = choice([AudioSegment.from_wav(file) for file in glob("sounds/style_NewJazz/hi-hat/*.wav")])
        kick = choice([AudioSegment.from_wav(file) for file in glob("sounds/style_NewJazz/kick/*.wav")])
        voicetag = AudioSegment.from_wav('sounds/voicetags/beatbot_voicetag_130bpm.wav')

        lead = AudioSegment.from_wav(lead_path)

        ##### ТАКТЫ #####

        ## 1 ##
        sandwich1 = lead
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

        sandwich3 = sandwich3.overlay(clap, position=0)
        sandwich3 = sandwich3.overlay(hi_hat, position=0)
        sandwich3 = sandwich3.overlay(kick, position=0)

        overlay = overlay.append(sandwich3, crossfade=0)

        ## 4 ##
        sandwich4 = lead
        sandwich4 = sandwich4.overlay(clap, position=0)
        sandwich4 = sandwich4.overlay(hi_hat, position=0)
        sandwich4 = sandwich4.overlay(kick[:-920], position=-920)
        
        overlay = overlay.append(sandwich4, crossfade=0)

        ## 5 ##
        sandwich5 = lead
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
            overlay = Audio_Action.change_bpm(overlay, bpm/130)

        # Максимальная амплитуда для клиппера (в децибелах)
        threshold = 0.5 # Здесь можно настроить желаемую амплитуду

        # Применение клиппера ко всему оверлею
        overlay = Audio_Action.apply_clipper(overlay, threshold)
        
        overlay.export(f"output_beats/{filename}.{extension}", format=f"{extension}")
        
        return True