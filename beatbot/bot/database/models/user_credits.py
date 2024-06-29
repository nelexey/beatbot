from sqlalchemy import Column, Integer, BigInteger, Date, ForeignKey
from sqlalchemy.sql import func
from bot.database.main import Database


class UserCredits(Database.BASE):
    __tablename__ = 'user_credits'

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, ForeignKey('users.chat_id'))
    beats = Column(Integer, default=0)
    options = Column(Integer, default=0)
    updated_at = Column(Date, default=func.current_date())
