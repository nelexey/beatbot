import os
import shutil

from .markup import Markup
from .audiolize import Audiolize
from .utils import generate_unique_folder_name

class Track:

    def __init__(self, 
                 filename, 
                 ext, 
                 working_dir,
                 output_path,
                 style, 
                 tonality, 
                 lad, 
                 bpm=150) -> None:
        """
        Объект класса Track, это представление структуры для генерации аудиофайла.
        Алгоритм заключается в создании нотной разметки notes_markup для каждого инструмента, 
        последующей конвертации в аудио и наложения эффектов с последующим объединением.
        """

        self.style = style
        self.tonality = tonality
        self.lad = lad

        self.filename = filename
        self.ext = ext
        self.bpm = bpm

        self.dir = f'{working_dir}/{generate_unique_folder_name(working_dir)}'
        os.mkdir(self.dir)
        self.input_dir = f'wav/'
        self.output_dir = output_path

        # Параметры длины бита
        self.s_length = 12800 * (150 / bpm) # ms
        self.q_length = self.s_length / 128 # ms

        """
        Подклассы

        Markup – класс для создания нотной разметки всех семплов в данном стиле.
            Sample – класс, обобщающий параметры для каждого генератора (класса) семпла.

        Audiolize – объединяющий класс для работы со звуковой частью
            Convert – класс для конвертации разметки в .wav
            Vst – класс для наложения эффектов на .wav
            Merge – класс для соединения .wav в цельный трек.
        """

        self.Markup = Markup(self)
        self.Audiolize = Audiolize(self)
    
    def clear(self):
        shutil.rmtree(self.dir)
