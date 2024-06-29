import copy
from glob import glob
import random
import os

from generator.misc import keys
from generator.helpers import analyze_key, generate_random_filename, trimmed_audio_mp3
from .styles_generators.GeneratorsHandler import GeneratorsHandler


def platinum_beats_handler(data: dict):
    params = data['params']

    user_dir = data['user_dir']
    style_dir = data['style_dir']
    style = params['style']
    lad = params['lad']
    bpm = int(params['bpm'])
    ext = params['ext']
    beats_count = data['beats_count']

    print(params, style_dir)

    # Если у стиля есть разделение на лады.
    if params['harmonic']:

        non_empty_keys = []

        # Создать список папок, в которых есть звуки.
        for key in keys:
            if (
                    not glob(f'{style_dir}/lead/{lad}/{key}/*') or
                    not glob(f'{style_dir}/bass/{lad}/{key}/*')):
                continue
            else:
                non_empty_keys.append(key)

        print(non_empty_keys)

        # Собрать пары звуков по тональностям и перемешать.

        # Парные списки лидов и басов. Пары находятся под одним индексом.
        leads_presets = []
        bass_presets = []

        for key in non_empty_keys:
            leads = glob(f'{style_dir}/lead/{lad}/{key}/*')
            basses = glob(f'{style_dir}/bass/{lad}/{key}/*')

            while leads and basses:
                lead = random.choice(leads)
                bass = random.choice(basses)
                if lead not in leads_presets and bass not in bass_presets:
                    leads_presets.append(f'{lead}')
                    bass_presets.append(f'{bass}')
                else:
                    continue
                leads.remove(lead)
                basses.remove(bass)

        combined = list(zip(leads_presets, bass_presets))
        random.shuffle(combined)
        leads_presets, bass_presets = zip(*combined)


    else:
        get_all_leads = glob(f"{style_dir}/lead/*.wav")

        print(get_all_leads, beats_count)

        lad_correct_leads = []

        # Проанализировать все лиды на выбранный лад и собрать список.
        for lead in get_all_leads:
            key, lead_lad = analyze_key(lead)

            print(key, lead_lad)

            if lead_lad == lad:
                lad_correct_leads.append(lead)

        # Если недостаточно подходящих лидов, то добрать любыми.
        if len(lad_correct_leads) < beats_count:
            print(f'Not enough relevant leads: {len(lad_correct_leads)}')
            for lead in get_all_leads:
                if lead not in lad_correct_leads:
                    lad_correct_leads.append(lead)

        # Перемешать лиды и собрать пути.
        leads_presets = []
        for file in random.sample(lad_correct_leads, beats_count):
            leads_presets.append(file)

        # Перемешать басы и собрать пути.
        bass_presets = []

        # Если у стиля есть басы.
        # if style not in non_bass_styles:
        if params['support_bass']:
            get_all_basses = glob(f"{style_dir}/bass/*.wav")

            lad_correct_bass = []

            for bass in get_all_basses:
                key, bass_lad = analyze_key(bass)

                if bass_lad == lad:
                    lad_correct_bass.append(bass)

            if len(lad_correct_bass) < beats_count:
                print(f'Not enough relevant basses: {len(lad_correct_bass)}')
                while len(lad_correct_bass) < beats_count:
                    for bass in get_all_basses:
                        if bass not in lad_correct_bass:
                            lad_correct_bass.append(bass)

            bass_presets = []
            for file in random.sample(lad_correct_bass, beats_count):
                bass_presets.append(file)

    for i in range(len(leads_presets)):
        if len(bass_presets) != 0:
            print(f'{leads_presets[i]} | {bass_presets[i]}')
        else:
            print(f'{leads_presets[i]} | -')

    generator = GeneratorsHandler()

    beats = {}

    # Сгенерировать определенное кол-во битов
    for i in range(beats_count):
        filename = generate_random_filename()

        lead_path = leads_presets[i]
        if len(bass_presets) != 0:
            bass_path = bass_presets[i]
        else:
            bass_path = None

        audio_path = generator.make_beat(style,
                                         filename,
                                         lead_path,
                                         bass_path,
                                         style_dir,
                                         user_dir,
                                         bpm,
                                         ext)

        beats[i + 1] = audio_path

    print(beats)

    response_data = dict()
    response_data['beat'] = beats
    response_data['short'] = {}

    # Обрезать биты
    for i, file in beats.items():
        print(i, file)
        output_path = os.path.dirname(file) + '/'
        response_data['short'][i] = trimmed_audio_mp3(generate_random_filename(), file, output_path)

    return response_data
