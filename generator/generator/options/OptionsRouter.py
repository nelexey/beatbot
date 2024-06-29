import asyncio

from generator.options import (speed_up,
                               slow_down,
                               bassboost,
                               find_key,
                               find_tempo,
                               normalize_sound,
                               midi_to_wav,
                               remove_vocal,
                               rhymes)

options = {
    'speed_up': speed_up,
    'slow_down': slow_down,
    'midi_to_wav': midi_to_wav,
    'remove_vocal': remove_vocal,
    'rhymes': rhymes,
    'find_key': find_key,
    'find_tempo': find_tempo,
    'normalize_sound': normalize_sound,
    'bassboost': bassboost
}


class OptionsRouter:
    def __init__(self):
        self.options = options

    async def handle_request(self, data):
        option_name = data.get('option_name')
        if option_name not in self.options:
            return {'error': 'Invalid option_name'}

        option_func = self.options[option_name]
        result = await asyncio.to_thread(option_func, data)

        return result
