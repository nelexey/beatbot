import db_handler
import time
from pydub import AudioSegment
from os import path, makedirs, remove
from subprocess import run
from glob import glob

class Handler():

    @staticmethod
    def checking():
        while True:
            query = db_handler.get_option_query()
            if query is not None:
                chat_id, chosen_format, order_number = query[0], query[1], query[2]

                sound_path = f'users_sounds/{chat_id}/sound.{chosen_format}'
                output_folder = f'users_sounds/{chat_id}/fragments'
                output_folder_final = f'users_sounds/{chat_id}/output_fragments'
                makedirs(output_folder, exist_ok=True)
                makedirs(output_folder_final, exist_ok=True)

                if chosen_format.lower() == 'mp3':
                    temp_audio = AudioSegment.from_file(sound_path)
                    sound_path = sound_path.replace('.mp3', '.wav')
                    temp_audio.export(sound_path, format="wav")
                    remove(f'{sound_path.split(".")[0]}.mp3')

                audio = AudioSegment.from_file(sound_path)

                fragment_length = 30000  # В миллисекундах

                num_fragments = len(audio) // fragment_length
                last_fragment_duration = len(audio) % fragment_length

                for i in range(num_fragments):
                    start_time = i * fragment_length
                    end_time = (i + 1) * fragment_length
                    fragment = audio[start_time:end_time]

                    fragment_filename = path.join(output_folder, f"{i + 1}.wav")
                    fragment.export(fragment_filename, format="wav")

                    # Имитация запуска команды из консоли
                    cmd = f'spleeter separate {fragment_filename} -p spleeter:2stems -o {output_folder_final} --filename_format "{i + 1}_{{instrument}}.{{codec}}"'
                    run(cmd, shell=True)

                if last_fragment_duration >= 10000:
                    last_fragment = audio[-last_fragment_duration:]
                    last_fragment_filename = path.join(output_folder, f"{num_fragments + 1}.wav")
                    last_fragment.export(last_fragment_filename, format="wav")

                    cmd = f'spleeter separate {last_fragment_filename} -p spleeter:2stems -o {output_folder_final} --filename_format "{num_fragments + 1}_{{instrument}}.{{codec}}"'
                    run(cmd, shell=True)
                else:
                    # Если последний фрагмент меньше 10 секунд, объединяем его с предпоследним
                    if num_fragments > 0:
                        last_fragment = audio[-last_fragment_duration:]
                        prev_fragment_filename = path.join(output_folder, f"{num_fragments}.wav")
                        prev_fragment = AudioSegment.from_file(prev_fragment_filename)

                        combined_last = prev_fragment + last_fragment
                        combined_last_filename = path.join(output_folder, f"{num_fragments}.wav")
                        combined_last.export(combined_last_filename, format="wav")

                        cmd = f'spleeter separate {combined_last_filename} -p spleeter:2stems -o {output_folder_final} --filename_format "{num_fragments}_{{instrument}}.{{codec}}"'
                        run(cmd, shell=True)

                # Склеивание файлов _vocals и _accompaniment
                all_vocals = glob(path.join(output_folder_final, '*_vocals.*'))
                all_accompaniment = glob(path.join(output_folder_final, '*_accompaniment.*'))

                # Создаем словарь, где ключ - индекс фрагмента, значение - путь к файлу
                vocals_dict = {}
                accompaniment_dict = {}

                for vocals_file in all_vocals:
                    index = int(path.basename(vocals_file).split('_')[0])
                    vocals_dict[index] = vocals_file

                for accompaniment_file in all_accompaniment:
                    index = int(path.basename(accompaniment_file).split('_')[0])
                    accompaniment_dict[index] = accompaniment_file

                # Получаем индексы в правильной последовательности
                sorted_indices = sorted(set(vocals_dict.keys()) | set(accompaniment_dict.keys()))

                combined_vocals = AudioSegment.empty()
                combined_accompaniment = AudioSegment.empty()

                for index in sorted_indices:
                    if index in vocals_dict:
                        combined_vocals = combined_vocals.append(AudioSegment.from_file(vocals_dict[index]), crossfade=0)
                    if index in accompaniment_dict:
                        combined_accompaniment = combined_accompaniment.append(AudioSegment.from_file(accompaniment_dict[index]), crossfade=0)

                final_vocals_path = f'users_sounds/{chat_id}/final_vocals.{chosen_format}'
                final_accompaniment_path = f'users_sounds/{chat_id}/final_accompaniment.{chosen_format}'

                combined_vocals.export(final_vocals_path, format=chosen_format)
                combined_accompaniment.export(final_accompaniment_path, format=chosen_format)

                # Удаление временных файлов
                for file in all_vocals + all_accompaniment:
                    remove(file)

                db_handler.set_removes_ready(chat_id)
                db_handler.del_options_query()

            time.sleep(3)

Handler.checking()
