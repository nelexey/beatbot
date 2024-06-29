import asyncio

from generator.beats.platinum import drill, trap, plug, jersey_club, old_school, opium, newjazz

styles_generators = {
    'drill': drill,
    'trap': trap,
    'plug': plug,
    'jc': jersey_club,
    'old_school': old_school,
    'opium': opium,
    'new_jazz': newjazz
}


class GeneratorsHandler:
    def __init__(self):
        self.styles = styles_generators

    def make_beat(self,
                  style: str,
                  filename: str,
                  lead_path: str,
                  bass_path: str,
                  style_dir: str,
                  user_dir: str,
                  bpm: int,
                  ext: str):

        if style not in self.styles:
            return {'error': 'Invalid style'}

        style_generator = self.styles[style]
        result = style_generator(filename,
                                 lead_path,
                                 bass_path,
                                 style_dir,
                                 user_dir,
                                 bpm,
                                 ext)

        return result
