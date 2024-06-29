import mido


def create_midi_markup(midi_file_path):
    # Открываем MIDI файл для чтения
    midi_file = mido.MidiFile(midi_file_path)

    # Инициализируем переменную для хранения начального темпа в BPM
    initial_bpm = None

    # Время начала: [[нота, время начала, длина]]
    midi_markup = []

    # Проходимся по всем трекам в MIDI файле
    for i, track in enumerate(midi_file.tracks):
        # print(f"Track {i}:")

        start_time = 0
        # Перебираем сообщения
        for msg in track:
            if msg.type == 'set_tempo' and initial_bpm is None:
                # Раскодируем значение темпа из байтов сообщения
                microseconds_per_beat = msg.tempo
                # Вычисляем начальный BPM на основе микросекунд на четверть ноты
                initial_bpm = 60000000 / microseconds_per_beat
                continue  # Выход из цикла после нахождения начального темпа

            if initial_bpm is not None:
                start_time += (msg.time / midi_file.ticks_per_beat) * (60000 / int(initial_bpm))

            if msg.type == 'note_on':
                note_on = start_time
                note_data = [msg.note, note_on, None]

                midi_markup.append(note_data)

                # print(f'{msg.type} -> {start_time} ms | note: {msg.note} | velocity: {msg.velocity}')

            if msg.type == 'note_off':
                duration = start_time - note_on
                for running_note in midi_markup:

                    if running_note[0] == msg.note and running_note[2] is None:
                        running_note[2] = duration

                # print(f'{msg.type} -> {msg.time} ms | note: {msg.note} | velocity: {msg.velocity}')

    # print(midi_markup)
    return midi_markup, start_time

