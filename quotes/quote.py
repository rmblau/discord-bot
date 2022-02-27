from datetime import time
from sqlalchemy import Column, String
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.sqltypes import BigInteger, DateTime, Integer

from user.base import Base


class Quote(Base):
    __tablename__ = 'quotes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    time_stamp = Column(DateTime)
    quote = Column(String)

    def __init__(self, time_stamp, quote) -> None:
        self.time_stamp = time_stamp
        self.quote = quote
