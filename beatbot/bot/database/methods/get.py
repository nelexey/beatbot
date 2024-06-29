from typing import Optional
from sqlalchemy import exc

from bot.database.main import Database
from bot.database.models import User, UserCredits


def get_user(chat_id: int) -> Optional[User]:
    try:
        return Database().session.query(User).filter(User.chat_id == chat_id).one()
    except exc.NoResultFound:
        return None


def get_user_credits(chat_id: int) -> Optional[UserCredits]:
    try:
        return Database().session.query(UserCredits).filter(UserCredits.chat_id == chat_id).one()
    except exc.NoResultFound:
        return None
