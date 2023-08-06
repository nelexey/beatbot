import db_handler
import time
import make_beat
from keyboards import aliases, options
import random
from pydub import AudioSegment # Для обрезки битов на их демо-версии
from os import path
from glob import glob

beats = 3

# Ключи - названия стилей на кнопках, значения - названия папок style_*

# Тональности
keys = [
    'A',
    'B',
    'C',
    'C#',
    'E',
    'F',
    'F#',
    'G',
]

class Handler():

    def cheking():
        while True:
            query = db_handler.get_query()
            if query is not None:

                chat_id, style, bpm, harmony, extension = query[0], query[1], query[2], query[3], query[4]

                db_handler.del_beats_ready(chat_id)
                
                print(query)

                if path.exists(f'style_{style}/lead/{harmony}'):

                    filled_keys = []

                    for key in keys:
                        leads_list = sorted(glob(f'style_{style}/lead/{harmony}/{key}/*.wav'))
                        bass_list = sorted(glob(f'style_{style}/bass/{harmony}/{key}/*.wav'))
                        if len(leads_list) >= 3 and len(bass_list) >= 3 :
                            filled_keys.append(key)

                    print(filled_keys)

                    key = random.choice(filled_keys)
                else:
                    key = None

                def generate_beats(aliases, num, style, chat_id, bpm, extension, harmony, key=None):
                    status = make_beat.generate_some_beats(aliases, num, style, chat_id, bpm, extension, harmony, key)
                    if status:
                        return True
                    else:
                        return False
                # Обрезать аудио на демо-версии и отправить пользователю, добавить id демо версии в бд
                def trimmed_audio(files_list):
                    for file_path in files_list:
                        
                        sound = AudioSegment.from_file(file_path)
                        trimmed = sound[35000:50000]
                        new_file_path = f"{path.splitext(file_path)[0]}_short.mp3"
                        trimmed.export(new_file_path, format=f"mp3")

                generate_beats(aliases, beats, style, chat_id, bpm, extension, harmony, key)
                trimmed_audio(sorted(glob(f'output_beats/{query[0]}_[1-{beats}].*'), key=lambda x: int(x.split('_')[-1].split('.')[0])))
                
                db_handler.del_query()

                db_handler.set_beats_ready(chat_id)

            time.sleep(3)

Handler.cheking()