#-------------------------#
# Обработчик очереди на создание битов.
# Работает отдельно, обращается к таблице query для получения очереди.
# Затем обращается к таблице orders, чтобы отметить обработку запроса завершенной.
#-------------------------#

from time import sleep
import datetime
from glob import glob
import random

from utils import db_connect
from utils.audio_action import Audio_Action
from utils.make_beat import Make_Beat
from data.utility_data import harmony_styles, keys, styles_aliases, non_bass_styles, beats

class Handler():

    @staticmethod
    def check_for_query():

        # Получить первый запрос из очереди.
        query = db_connect.get_query()
        
        # Если запросов нет.
        if query is None:
            # Время ожидания между запросами.
            sleep(5)
            return
        
        # Получить текущую дату и время.
        now = datetime.datetime.now()
        
        chat_id, style, bpm, extension, harmony = query[0], query[1], query[2], query[3], query[4]

        print(f'• {now.date()} {now.time()} | Got query: [chat_id: {chat_id}, style: {style}, bpm: {bpm}, harmony: {harmony}, extension: {extension}]')
        
        # Установить готовность битов на 0.
        db_connect.del_beats_ready(chat_id)

        # Если у стиля есть разделение на лады.
        if style in harmony_styles:
            
            non_empty_keys = []
            
            # Создать список папок, в которых есть звуки.
            for key in keys:
                if not glob(f'sounds/style_{styles_aliases[style]}/lead/{harmony}/{key}/*') or not glob(f'sounds/style_{styles_aliases[style]}/bass/{harmony}/{key}/*'):
                    continue
                else:
                    non_empty_keys.append(key)

            print(non_empty_keys)
            
            ## Собрать пары звуков по тональностям и перемешать.

            # Парные списки лидов и басов. Пары находятся под одним индексом.
            leads_presets = []
            basses_presets = []

            for key in non_empty_keys:
                leads = glob(f'sounds/style_{styles_aliases[style]}/lead/{harmony}/{key}/*')
                basses = glob(f'sounds/style_{styles_aliases[style]}/bass/{harmony}/{key}/*')
                while leads and basses:
                    lead = random.choice(leads)
                    bass = random.choice(basses)
                    if lead not in leads_presets and bass not in basses_presets:
                        leads_presets.append(f'{lead}')
                        basses_presets.append(f'{bass}')
                    else:
                        continue
                    leads.remove(lead)
                    basses.remove(bass)

            combined = list(zip(leads_presets, basses_presets))
            random.shuffle(combined)
            leads_presets, basses_presets = zip(*combined)

        else:
            get_all_leads = glob(f"sounds/style_{styles_aliases[style]}/lead/*.wav")

            harmony_correct_leads = []

            # Проанализировать все лиды на выбранный лад и собрать список.
            for lead in get_all_leads:
                key, lead_harmony = Audio_Action.analyze_key(lead)

                if lead_harmony == harmony:
                    harmony_correct_leads.append(lead)

            # Если недостаточно подходящих лидов, то добрать любыми.
            if len(harmony_correct_leads) < beats:
                print(f'Not enough relevant leads: {len(harmony_correct_leads)}')
                while len(harmony_correct_leads) < beats:
                    for lead in get_all_leads:
                        if lead not in harmony_correct_leads:
                            harmony_correct_leads.append(lead)
                
            # Перемешать лиды и собрать пути.
            leads_presets = []
            for file in random.sample(harmony_correct_leads, beats):
                leads_presets.append(file)

            # Перемешать басы и собрать пути.
            basses_presets = []

            # Если у стиля есть басы.
            if style not in non_bass_styles:
                get_all_basses = glob(f"sounds/style_{styles_aliases[style]}/bass/*.wav")

                harmony_correct_basses = []

                for bass in get_all_basses:
                    key, bass_harmony = Audio_Action.analyze_key(bass)

                    if bass_harmony == harmony:
                        harmony_correct_basses.append(bass)

                if len(harmony_correct_basses) < beats:
                    print(f'Not enough relevant basses: {len(harmony_correct_basses)}')
                    while len(harmony_correct_basses) < beats:
                        for bass in get_all_basses:
                            if bass not in harmony_correct_basses:
                                harmony_correct_basses.append(bass)
                    
                basses_presets = []
                for file in random.sample(harmony_correct_basses, beats):
                    basses_presets.append(file)

        for i in range(len(leads_presets)):
            if len(basses_presets) != 0:
                print(f'{leads_presets[i]} | {basses_presets[i]}')
            else:
                print(f'{leads_presets[i]} | -')

        # Создать биты.
        for i in range(beats):

            filename = f'{chat_id}_{i+1}'
            
            lead_path = leads_presets[i]
            if len(basses_presets) != 0:
                bass_path = basses_presets[i]
            else:
                bass_path = None

            Make_Beat.make_beat(style, filename, extension, bpm, lead_path, bass_path)
            Audio_Action.trimmed_audio(glob(f'output_beats/{filename}.*')[0])
 
        
        # Удалить из очереди.
        db_connect.del_query()
        # Установить готовность битов.
        db_connect.set_beats_ready(chat_id)

# Зациклить проверку.
while True:
    Handler.check_for_query()
    