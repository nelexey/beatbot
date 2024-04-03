"""Связующий класс между файлами семплов и файлом разметки"""

from .samples import *
from .utils import tonality_notes, change_octave, notes_numbers, divide_length

sample_generators = {'lead': lead,
                     'eguitar': eguitar,
                     'piano': piano,
                     'bass': bass,
                     'aguitar': aguitar,

                     'kick': kick,
                     'hihat': hihat,
                     'clap': clap,
                     'voicetag': None
                     }

class Sample:

    def __init__(self, markup) -> None:
        self.s_length = markup.s_length
        self.q_length = markup.q_length

        # Ноты должны быть представлены цифрами и быть на 5-ой октаве.
        self.notes = [notes_numbers[change_octave(note, 5)] for note in tonality_notes.get_notes(markup.tonality, markup.lad)]


    def generate_markup(self, instrument):
        if sample_generators[instrument]:
            return sample_generators[instrument].generate(self.notes, self.s_length, self.q_length, divide_length)
        else:
            return None