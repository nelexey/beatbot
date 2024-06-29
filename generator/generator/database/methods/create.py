from sqlalchemy.exc import NoResultFound

from generator.database.main import Database
from generator.database.models import OptionsQueue, BeatsQueue


def create_options_queue_item(query_data: dict, handler_number: int) -> None:
    session = Database().session
    try:
        new_queue_item = OptionsQueue(
            query_data=query_data,
            handler_number=handler_number
        )
        session.add(new_queue_item)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


def create_beats_queue_item(query_data: dict, handler_number: int) -> None:
    session = Database().session
    try:
        new_queue_item = BeatsQueue(
            query_data=query_data,
            handler_number=handler_number
        )
        session.add(new_queue_item)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
