from sqlalchemy import Column, Integer, BigInteger, Date, ForeignKey
from sqlalchemy.sql import func
from bot.database.main import Database


class UserStatistics(Database.BASE):
    __tablename__ = 'user_statistics'

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, ForeignKey('users.chat_id'))
    service_id = Column(Integer, ForeignKey('services.id'))
    uses = Column(Integer, default=0)
    updated_at = Column(Date, default=func.current_date())
