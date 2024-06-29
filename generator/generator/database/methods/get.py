from sqlalchemy.exc import NoResultFound
from sqlalchemy import asc

from generator.database.main import Database
from generator.database.models import OptionsQueue, BeatsQueue


def get_oldest_options_queue_item(handler_number: int = None) -> OptionsQueue | None:
    session = Database().session
    try:
        query = session.query(OptionsQueue).order_by(asc(OptionsQueue.creation_date))
        if handler_number is not None:
            query = query.filter(OptionsQueue.handler_number == handler_number)
        return query.first()
    except NoResultFound:
        return None


def get_all_options_queue_items() -> list[OptionsQueue]:
    session = Database().session
    try:
        return session.query(OptionsQueue).all()
    except NoResultFound:
        return []


def get_all_options_queue_items_handling_status(handler_number: int = None) -> list[bool]:
    session = Database().session
    try:
        query = session.query(OptionsQueue.is_handling)
        if handler_number is not None:
            query = query.filter(OptionsQueue.handler_number == handler_number)
        return [item[0] for item in query.all()]
    except NoResultFound:
        return []


def get_oldest_beats_queue_item(handler_number: int = None) -> BeatsQueue | None:
    session = Database().session
    try:
        query = session.query(BeatsQueue).order_by(asc(BeatsQueue.creation_date))
        if handler_number is not None:
            query = query.filter(BeatsQueue.handler_number == handler_number)
        return query.first()
    except NoResultFound:
        return None


def get_all_beats_queue_items() -> list[BeatsQueue]:
    session = Database().session
    try:
        return session.query(BeatsQueue).all()
    except NoResultFound:
        return []


def get_all_beats_queue_items_handling_status(handler_number: int = None) -> list[bool]:
    session = Database().session
    try:
        query = session.query(BeatsQueue.is_handling)
        if handler_number is not None:
            query = query.filter(BeatsQueue.handler_number == handler_number)
        return [item[0] for item in query.all()]
    except NoResultFound:
        return []
