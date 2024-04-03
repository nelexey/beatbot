from random import shuffle, choice


class Generator:
    @staticmethod
    def generate(notes, s_length, sq_length, notes_length) -> list:
   
        ### Инициализация разметки
        # Время начала: [[нота, время начала, длина]]
        notes_markup = []
        # Длина трека
        track_length = 0
        # Список длин нот
        # [2,4,6] сколько squares длится нота
        length_list = notes_length([2,4,8], 32) + notes_length([2,4,8], 32)

        # Предыдущая нота
        previous_note = 0

        shuffle(notes)

        length_notes_pairs = []

        for i in range(len(length_list)):
            # "i" это номер ноты
            note_length = sq_length * length_list[i]

            # Каждая последующая нота должна отличаться от предыдущей
            while True:
                note = choice(notes)
                if note != previous_note:
                    previous_note = note
                    break

            length_notes_pairs.append((note_length, note))
            
            notes_markup.append([note, track_length, note_length])
            # Добавление длины ноты к длине трека
            track_length += note_length
        
        for note_length, note in length_notes_pairs:
            notes_markup.append([note, track_length, note_length])
            # Добавление длины ноты к длине трека
            track_length += note_length

        return(notes_markup)
        

            

            
        

