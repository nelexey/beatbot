from .utility_data import get_instruments_pack, style_instruments
from .sample import Sample
from .exceptions import MarkupException

class Markup:
    """
    Класс для сбора всех нотных разметок семплов (samples_markup).

    У каждого стиля есть определенные инструменты,
    для каждого из этих инструментов генерируется разметка семпла (отрезка аудиодорожки).
    Все разметки семплов раскзадываются по слоям.
    """

    def __init__(self, track) -> None:
        self.style = track.style
        self.tonality = track.tonality
        self.lad = track.lad
        self.s_length = track.s_length
        self.q_length = track.q_length

        #TODO Исключение если не нашелся стиль
        # inst[0] - instrument,  
        # inst[1] - duration
        self.style_instruments = list(inst[0] for inst in get_instruments_pack(self.style))
        self.sample = Sample(self)
        
        """
        Нотная разметка:
            samples_markups = {
                                'instrument': [[notes], [notes] ...],
                                ...
                                }
        """
        self.samples_markups = {}
    
    def collect_markup(self, instruments):
        """
        Создать разметки семплов всех инструментов
        instruments: None, list – список тех инструментов стиля для которых нужно создать разметку.
        """

        for instrument in instruments:
            if instrument not in list(style_instruments[self.style].keys()):
                raise MarkupException(f'instrument ({instrument}) not in {self.style}')

        for instrument in instruments:
            markup = [self.sample.generate_markup(instrument)]

            if None in markup:
                print(f'Нет разметки для инструмента {instrument}! Пропуск.')
            else:
                self.samples_markups[instrument] = markup
        
    def get_instruments_in_markup(self):
        return ((instrument, self.samples_markups[instrument]) for instrument in self.samples_markups)

        
