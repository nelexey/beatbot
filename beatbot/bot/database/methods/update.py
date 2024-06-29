from sqlalchemy.exc import NoResultFound
from typing import Any
from datetime import datetime, timedelta

from bot.database.main import Database
from bot.database.models import User, UserCredits, Service, UserStatistics
from bot.misc.parameters import OPTION_CREDITS


def update_user(chat_id: int, **kwargs: Any) -> None:
    session = Database().session
    try:
        user = session.query(User).filter(User.chat_id == chat_id).one()
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        session.commit()
    except NoResultFound:
        pass


def reduce_user_balance(chat_id: int, amount: float) -> None:
    session = Database().session
    try:
        user = session.query(User).filter(User.chat_id == chat_id).one()
        user.balance -= amount
        user.updated_at = datetime.now()
        session.commit()
    except NoResultFound:
        pass


def fill_user_balance(chat_id: int, amount: float) -> None:
    session = Database().session
    try:
        user = session.query(User).filter(User.chat_id == chat_id).one()
        user.balance += amount
        user.updated_at = datetime.now()
        session.commit()
    except NoResultFound:
        pass


def fill_user_credits(chat_id: int, beats: int = 0, options: int = 0) -> None:
    session = Database().session
    try:
        user_credits = session.query(UserCredits).filter(UserCredits.chat_id == chat_id).one()
        user_credits.beats += beats
        user_credits.options += options
        user_credits.updated_at = datetime.now()
        session.commit()
    except NoResultFound:
        pass


def refill_user_options_credits(chat_id: int) -> None:
    session = Database().session
    try:
        user_credits = session.query(UserCredits).filter(UserCredits.chat_id == chat_id).one()
        user_credits.options = OPTION_CREDITS
        user_credits.updated_at = datetime.now()
        session.commit()
    except NoResultFound:
        pass


def refill_credits_if_needed(chat_id: int):
    today = datetime.now().date()  # Get current date
    session = Database().session
    user_credits = session.query(UserCredits).filter(UserCredits.chat_id == chat_id).one_or_none()

    # Check if user_credits found and updated_at is more than 24 hours ago
    if user_credits and (today - user_credits.updated_at) >= timedelta(days=1):
        # Call method to refill user credits
        refill_user_options_credits(chat_id)


def remove_user_options_credit(chat_id: int) -> None:
    session = Database().session
    try:
        user_credits = session.query(UserCredits).filter(UserCredits.chat_id == chat_id).one()
        user_credits.options -= 1
        session.commit()
    except NoResultFound:
        pass


def remove_user_beats_credit(chat_id: int) -> None:
    session = Database().session
    try:
        user_credits = session.query(UserCredits).filter(UserCredits.chat_id == chat_id).one()
        user_credits.beats -= 1
        session.commit()
    except NoResultFound:
        pass


def set_user_sub(chat_id: int) -> None:
    session = Database().session
    try:
        user = session.query(User).filter(User.chat_id == chat_id).one()
        user.has_sub = True
        user.sub_expiration_date = datetime.now() + timedelta(days=30)
        session.commit()
    except NoResultFound:
        pass


def delete_sub_if_expired(chat_id: int) -> bool:
    session = Database().session
    try:
        user = session.query(User).filter(User.chat_id == chat_id).one()
        now = datetime.now()

        # If subscription is expired
        if user.has_sub and user.sub_expiration_date <= now:
            user.has_sub = False
            user.sub_expiration_date = None
            session.commit()
            return True
    except NoResultFound:
        pass

    return False


def remove_user_sub(chat_id: int) -> None:
    session = Database().session
    try:
        user = session.query(User).filter(User.chat_id == chat_id).one()
        user.has_sub = False
        user.sub_expiration_date = None
        session.commit()
    except NoResultFound:
        pass


def update_user_statistic(chat_id: int, service_name: str, amount: int = 1) -> None:
    session = Database().session
    try:
        service = session.query(Service).filter(Service.service_name == service_name).one_or_none()
        if service is None:
            service = Service(service_name=service_name)
            session.add(service)
            session.commit()

        user_stat = session.query(UserStatistics).filter(
            UserStatistics.chat_id == chat_id,
            UserStatistics.service_id == service.id
        ).one_or_none()

        if user_stat is None:
            user_stat = UserStatistics(chat_id=chat_id, service_id=service.id, uses=amount)
            session.add(user_stat)
        else:
            user_stat.uses += amount
            user_stat.updated_at = datetime.now()

        session.commit()
    except NoResultFound:
        pass
