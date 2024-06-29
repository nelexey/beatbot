from sqlalchemy import Column, Integer, String
from bot.database.main import Database


class Service(Database.BASE):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)
    service_name = Column(String(255), unique=True)
