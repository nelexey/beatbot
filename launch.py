import db_handler
from os import remove
from glob import glob

beats = 3

chat_ids = db_handler.get_beats_generating_chat_ids()
chat_ids_by_messages_to_del_ids = db_handler.get_chat_ids_by_messages_to_del_ids()
db_handler.del_processing_for_all()
db_handler.del_all_queries()
db_handler.del_all_options_queries()
mailing_list = []

for chat_id in chat_ids:
    for file in glob(f'output_beats/{chat_id}_[1-{beats}]*.*'):
        remove(file)

    db_handler.del_beats_ready(chat_id)
    db_handler.del_beats_generating(chat_id)
    mailing_list.append(chat_id)

removes_mailing_list = []

for chat_id in db_handler.get_options_query_chat_ids():
    removes_mailing_list.append(chat_id)

for file in (glob(f'users_sounds/*/*.*')) + glob(f'users_sounds/*/fragments/*.*') + glob(f'users_sounds/*/output_fragments/*.*'):
    remove(file)
    