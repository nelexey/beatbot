import asyncio
import os

from .handlers.midi_to_wav_handler import midi_to_wav_handler
from generator.helpers import generate_random_filename, delete_file

from generator.database.methods.create import create_options_queue_item
from generator.database.methods.get import get_all_options_queue_items_handling_status, get_oldest_options_queue_item
from generator.database.methods.update import update_options_handling_status
from generator.database.methods.delete import delete_options_queue_item

from generator.web.requests.Service import option_done_req


def midi_to_wav(data):
    audio_path = data['file_path']
    midi_path = data['additional']['midi']

    audio_format = os.path.splitext(audio_path)[1].lower()[1:]

    query_data = {'option_name': data['option_name'],
                  'chat_id': data['chat_id'],
                  'audio_path': audio_path,
                  'audio_format': audio_format,
                  'midi_path': midi_path}

    handler_number = 1

    create_options_queue_item(query_data, handler_number)

    while True:
        query = get_oldest_options_queue_item(handler_number)

        if query is not None and not query.is_handling:

            update_options_handling_status(query.id, True)

            new_audio_path = midi_to_wav_handler(query.query_data['midi_path'], query.query_data['audio_path'],
                                                 query.query_data['audio_format'])

            delete_options_queue_item(query.id)

            result = {'file_path': new_audio_path}

            asyncio.run(option_done_req(query.query_data['option_name'],
                                        query.query_data['chat_id'],
                                        result)
                        )

            asyncio.run(delete_file(audio_path))
            asyncio.run(delete_file(midi_path))

        else:
            break

    return None
