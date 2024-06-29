from sqlalchemy.exc import NoResultFound
from typing import Any

from generator.database.models import OptionsQueue, BeatsQueue
from generator.database.main import Database


def update_options_queue_item(id: int, **kwargs: Any) -> None:
    session = Database().session
    try:
        queue_item = session.query(OptionsQueue).filter(OptionsQueue.id == id).one()
        for key, value in kwargs.items():
            if hasattr(queue_item, key):
                setattr(queue_item, key, value)
        session.commit()
    except NoResultFound:
        pass


def update_options_handling_status(id: int, is_handling: bool):
    return update_options_queue_item(id=id, is_handling=is_handling)


def update_beats_queue_item(id: int, **kwargs: Any) -> None:
    session = Database().session
    try:
        queue_item = session.query(BeatsQueue).filter(BeatsQueue.id == id).one()
        for key, value in kwargs.items():
            if hasattr(queue_item, key):
                setattr(queue_item, key, value)
        session.commit()
    except NoResultFound:
        pass


def update_beats_handling_status(id: int, is_handling: bool):
    return update_beats_queue_item(id=id, is_handling=is_handling)
