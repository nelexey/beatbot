import asyncio

from .platinum import platinum

gen_models = {
    'platinum': platinum,
    'beatfusion': ''
}


class BeatsRouter:
    def __init__(self):
        self.gen_models = gen_models

    async def handle_request(self, data):
        model = data.get('model')
        if model not in self.gen_models:
            return {'error': 'Invalid model'}

        generation_model = self.gen_models[model]
        result = await asyncio.to_thread(generation_model, data)

        return result
