import db_handler
from config import beats

from os import remove
from glob import glob

chat_ids = db_handler.get_beats_generating_chat_ids()
chat_ids_by_messages_to_del_ids = db_handler.get_chat_ids_by_messages_to_del_ids()
db_handler.del_processing_for_all()
db_handler.del_all_queries()
mailing_list = []

for chat_id in chat_ids:
    for file in glob(f'output_beats/{chat_id}_[1-{beats}]*.*'):
        remove(file)

    db_handler.del_beats_ready(chat_id)
    db_handler.del_beats_generating(chat_id)
    mailing_list.append(chat_id)

removes_mailing_list = []

chat_ids = db_handler.get_options_query_chat_ids()
print(chat_ids)

db_handler.del_all_options_queries()

for chat_id in chat_ids:
    db_handler.del_removes_ready(chat_id)
    removes_mailing_list.append(chat_id)

for file in (glob(f'users_sounds/*/*.*')) + glob(f'users_sounds/*/fragments/*.*') + glob(f'users_sounds/*/output_fragments/*.*'):
    remove(file)
    