from sqlalchemy import Column, Integer, DateTime, func, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from generator.database.main import Database


class OptionsQueue(Database.BASE):
    __tablename__ = 'options_queue'

    id = Column(Integer, primary_key=True)
    query_data = Column(JSONB)
    creation_date = Column(DateTime, server_default=func.now())
    handler_number = Column(Integer)
    is_handling = Column(Boolean, default=False)
