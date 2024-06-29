from sqlalchemy.exc import NoResultFound

from generator.database.models import OptionsQueue, BeatsQueue
from generator.database.main import Database


def delete_options_queue_item(id: int) -> None:
    session: Database.session = Database().session
    try:
        queue_item: OptionsQueue = session.query(OptionsQueue).filter(
            OptionsQueue.id == id).one()
        session.delete(queue_item)
        session.commit()
    except NoResultFound:
        pass


def delete_beats_queue_item(id: int) -> None:
    session: Database.session = Database().session
    try:
        queue_item: BeatsQueue = session.query(BeatsQueue).filter(
            BeatsQueue.id == id).one()
        session.delete(queue_item)
        session.commit()
    except NoResultFound:
        pass
