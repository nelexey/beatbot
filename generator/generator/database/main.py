from typing import Final
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from generator.misc import settings
from generator.misc import SingletonMeta


class Database(metaclass=SingletonMeta):
    BASE: Final = declarative_base()

    def __init__(self):
        self.__engine = create_engine(settings.database_url, pool_size=10, max_overflow=20)
        session_factory = sessionmaker(bind=self.__engine)
        self.__session = scoped_session(session_factory)

    @property
    def session(self):
        return self.__session

    @property
    def engine(self):
        return self.__engine
