from sqlalchemy.exc import NoResultFound

from bot.database.main import Database
from bot.database.models import User, UserCredits
from bot.misc.parameters import OPTION_CREDITS


def create_user(username: str, first_name: str, last_name: str, chat_id: int) -> None:
    session = Database().session
    try:
        session.query(User.chat_id).filter(User.chat_id == chat_id).one()
    except NoResultFound:
        new_user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            chat_id=chat_id,
        )
        session.add(new_user)

        new_user_credits = UserCredits(
            chat_id=chat_id,
            options=OPTION_CREDITS,
        )
        session.add(new_user_credits)

        session.commit()
