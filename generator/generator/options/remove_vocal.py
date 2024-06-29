import os
import asyncio

from .handlers.vocal_remover_handler import remove_vocal_handler
from generator.helpers import generate_random_filename, delete_file

from generator.database.methods.create import create_options_queue_item
from generator.database.methods.get import get_all_options_queue_items_handling_status, get_oldest_options_queue_item
from generator.database.methods.update import update_options_handling_status
from generator.database.methods.delete import delete_options_queue_item

from generator.web.requests.Service import option_done_req


def remove_vocal(data):
    audio_path = data['file_path']

    audio_format = os.path.splitext(audio_path)[1].lower()[1:]

    query_data = {'option_name': data['option_name'],
                  'chat_id': data['chat_id'],
                  'audio_path': audio_path,
                  'audio_format': audio_format}

    handler_number = 2

    create_options_queue_item(query_data, handler_number)

    while True:
        query = get_oldest_options_queue_item(handler_number)

        if query is not None and not query.is_handling:

            update_options_handling_status(query.id, True)

            vocal_path, instrumental_path = remove_vocal_handler(query.query_data['audio_path'], )

            delete_options_queue_item(query.id)

            result = {'vocal_path': vocal_path,
                      'instrumental_path': instrumental_path}

            asyncio.run(option_done_req(query.query_data['option_name'],
                                        query.query_data['chat_id'],
                                        result)
                        )

            asyncio.run(delete_file(audio_path))

        else:
            break
