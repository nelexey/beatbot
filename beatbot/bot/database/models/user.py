from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime
from sqlalchemy.sql import func
from bot.database.main import Database


class User(Database.BASE):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(255), nullable=True, default=None)
    first_name = Column(String(255), nullable=True, default=None)
    last_name = Column(String(255), nullable=True, default=None)
    balance = Column(BigInteger, default=0)
    has_sub = Column(Boolean, default=False)
    sub_expiration_date = Column(DateTime)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, default=func.now())
