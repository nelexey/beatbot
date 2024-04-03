import os
from glob import glob
from random import choice

from .convert import Convert
from .effects import Effects
from .merge import Merge
from .utility_data import style_instruments
from .exceptions import MarkupException

class Audiolize:
    """
    Связующий класс по работе с аудио
    """

    def __init__(self, track) -> None:
        # data_dir, style, markup, s_length, filename, ext
        self.input_dir = track.input_dir
        self.convert_dir = f'{track.dir}/converted'
        self.effect_dir = f'{track.dir}/effected'
        self.merge_dir = f'{track.dir}/merged'
        self.output_dir = track.output_dir
        self.fragments_dir= f'{track.dir}/fragments'

        for directory in [self.convert_dir,self.effect_dir,self.merge_dir,self.output_dir,self.fragments_dir]:
            os.mkdir(directory)

        self.markup = track.Markup.samples_markups
        self.style = track.style

        self.Convert = Convert(self, track)
        self.Effects = Effects()
        self.Merge = Merge(self, track)

        self.output_files = []


    def convert(self, instruments=None):
        for instrument in instruments:
            if instrument not in self.markup.keys():
                raise MarkupException(f'instrument ({instrument}) not in {self.style}')
            
        for instrument in instruments:
            sounds = glob(f'{self.input_dir}/Generator/{instrument}/*.wav')

            if len(sounds)==0: continue

            self.Convert.convert_to_wav(instrument,
                                        self.markup[instrument],
                                        sounds)
            
    def merge(self, bpm, instruments=None):            
        for instrument in instruments:
            if instrument in list(self.markup.keys()):
                path_to_sample = self.Convert.paths[instrument]
                change_speed = False
            else:
                path_to_sample = choice(glob(f'{self.input_dir}/{self.style}/{instrument}/*.wav'))
                change_speed = True
            self.Merge.merge_samples(instrument, 
                                     path_to_sample, bpm, change_speed)
    
    def reverb(self, instruments: list):
        for instrument in instruments:
            if instrument not in list(style_instruments[self.style].keys()):
                raise MarkupException(f'instrument ({instrument}) not in {self.style}')

        for instrument in instruments:
            if 'reverb' not in list(style_instruments[self.style][instrument].keys()):
                return f'{instrument} does not have reverb params! Skipping...'
            
            self.Effects.reverb(self.Merge.paths[instrument], **style_instruments[self.style][instrument]['reverb'])
    
    def volume(self, instruments: list):
        for instrument in instruments:
            if instrument not in list(style_instruments[self.style].keys()):
                raise MarkupException(f'instrument ({instrument}) not in {self.style}')

        for instrument in instruments:
            if 'volume' not in list(style_instruments[self.style][instrument].keys()):
                return f'{instrument} does not have volume params! Skipping...'
            
            self.Effects.volume(self.Merge.paths[instrument], **style_instruments[self.style][instrument])
    
    def bake_track(self) -> str:
        '''
        Накладывает все аудиодорожки и сохраняет в файл.
        Возвращает путь к объединённому треку.
        '''
        return self.Merge.merge_lines(glob(f'{self.merge_dir}/*.wav'), self.output_dir)