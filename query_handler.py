

import time
from pydub import AudioSegment # Для обрезки битов на их демо-версии
from os import path
from glob import glob

from data.utility_data import keys, beats
import utils.db_connect as db_connect
import utils.make_beat as make_beat
from utils.keyboards import aliases

class Handler():

    def checking():
        while True:
            query = db_connect.get_query()
            if query is not None:

                chat_id, style, bpm, harmony, extension = query[0], query[1], query[2], query[3], query[4]

                db_connect.del_beats_ready(chat_id)
                
                print(query)

                if path.exists(f'style_{style}/lead/{harmony}'):

                    filled_keys = []

                    for key in keys:
                        leads_list = sorted(glob(f'style_{style}/lead/{harmony}/{key}/*.wav'))
                        bass_list = sorted(glob(f'style_{style}/bass/{harmony}/{key}/*.wav'))
                        if len(leads_list) >= 3 and len(bass_list) >= 3 :
                            filled_keys.append(key)

                    if filled_keys != []:
                        for key in keys:
                            leads_list = sorted(glob(f'style_{style}/lead/{harmony}/{key}/*.wav'))
                            bass_list = sorted(glob(f'style_{style}/bass/{harmony}/{key}/*.wav'))
                            if len(leads_list) >= 1 and len(bass_list) >= 1 :
                                filled_keys.append(key)
                        
                else:
                    key = None

                def generate_beats(aliases, num, style, chat_id, bpm, extension, harmony, keys=None):
                    status = make_beat.generate_some_beats(aliases, num, style, chat_id, bpm, extension, harmony, keys)
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

                generate_beats(aliases, beats, style, chat_id, bpm, extension, harmony, filled_keys)
                trimmed_audio(sorted(glob(f'output_beats/{query[0]}_[1-{beats}].*'), key=lambda x: int(x.split('_')[-1].split('.')[0])))
                
                db_connect.del_query()

                db_connect.set_beats_ready(chat_id)

            time.sleep(3)

Handler.checking()