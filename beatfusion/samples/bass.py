from random import shuffle, choice

class Generator:
    @staticmethod
    def generate(notes, s_length, sq_length, notes_length) -> list:
        # print(f'got notes: {notes}, got length {s_length}, got square length {sq_length}')
        
        ### Инициализация разметки
        # Время начала: [[нота, время начала, длина]]
        notes_markup = []
        # Длина трека
        track_length = 0
        # Список длин нот
        # [2,4,6] сколько squares длится нота
        length_list = (20, 12)*4

        # Предыдущая нота
        previous_note = 0

        shuffle(notes)

        for i in range(len(length_list)):
            # "i" это номер ноты
            note_length = sq_length * length_list[i]

            # Каждая последующая нота должна отличаться от предыдущей
            while True:
                note = choice(notes)
                if note != previous_note:
                    previous_note = note
                    break
            
            notes_markup.append([note, track_length, note_length])
            # Добавление длины ноты к длине трека
            track_length += note_length

        return(notes_markup)
        

            

            
        

