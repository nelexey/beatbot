import db_handler
import asyncio
import make_beat
from pydub import AudioSegment # Для обрезки битов на их демо-версии
from os import path
from glob import glob
from launch import beats

# Ключи - названия стилей на кнопках, значения - названия папок style_*
aliases = {
    'Jersey Club': 'JC',
    'Trap': 'Trap',
    'Drill': 'Drill',
    'Plug': 'Plug',
    'Old School': 'OldSchool'
}

class Handler():

    
    async def cheking():
        while True:
            query = db_handler.get_query()
            if query is not None:
                # style - стиль бита, num - сколько битов сделать
                print(query)
               
                def generate_beats(aliases, num, style, chat_id, bpm, extension):
                    status = make_beat.generate_some_beats(aliases, num, style, chat_id, bpm, extension)
                    if status:
                        return True
                    else:
                        return False
                # Обрезать аудио на демо-версии и отправить пользователю, добавить id демо версии в бд
                def trimmed_audio(files_list):
                    for file_path in files_list:
                        
                        sound = AudioSegment.from_file(file_path)
                        trimmed = sound[45000:55000]
                        new_file_path = f"{path.splitext(file_path)[0]}_short.mp3"
                        trimmed.export(new_file_path, format=f"mp3")

                generate_beats(aliases, beats, query[1], query[0], query[2], query[3])
                trimmed_audio(sorted(glob(f'output_beats/{query[0]}_[1-{beats}].*'), key=lambda x: int(x.split('_')[-1].split('.')[0])))
                db_handler.del_query()
            await asyncio.sleep(6)

asyncio.run(Handler.cheking())