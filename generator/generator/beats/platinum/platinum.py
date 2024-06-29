import os
import asyncio

from generator.database.methods.create import create_beats_queue_item
from generator.database.methods.get import get_oldest_beats_queue_item
from generator.database.methods.update import update_beats_handling_status
from generator.database.methods.delete import delete_beats_queue_item
from generator.web.requests.Service import beat_done_req
from generator.helpers import generate_random_filename
from .handler import platinum_beats_handler


def platinum(data):
    model = data['model']
    chat_id = data['chat_id']
    params = data['params']
    beats_count = 3

    current_dir = os.path.dirname(os.path.abspath(__file__))

    session_dir = f'{generate_random_filename(4)}'
    user_dir = data['user_dir'] + f'/{session_dir}/'
    os.makedirs(user_dir, exist_ok=True)

    style_dir = os.path.join(current_dir, "sounds", str(data['params']['style']))

    query_data = {'model': model,
                  'chat_id': chat_id,
                  'params': params,
                  'user_dir': user_dir,
                  'style_dir': style_dir,
                  'beats_count': beats_count}

    handler_number = 1

    create_beats_queue_item(query_data, handler_number)

    while True:
        query = get_oldest_beats_queue_item(handler_number)

        if query is not None and not query.is_handling:
            try:
                update_beats_handling_status(query.id, True)

                try:
                    beats_and_shorts = platinum_beats_handler(query.query_data)
                    result = {'paths': beats_and_shorts}

                except Exception as e:
                    print(e)
                    import traceback
                    traceback.print_exc()
                    result = {'error': 'Error due handling'}

                asyncio.run(beat_done_req(query.query_data['model'],
                                          query.query_data['chat_id'],
                                          query.query_data['user_dir'],
                                          result)
                            )
            finally:
                delete_beats_queue_item(query.id)

        else:
            break
