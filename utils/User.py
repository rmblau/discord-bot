from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.sql.sqltypes import BigInteger

from .base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    weather_location = Column(String)
    units = Column(String)
    country_code = Column(String)

    def __init__(self, id, weather_location, units, country_code) -> None:
        self.id = id
        self.weather_location = weather_location
        self.units = units
        self.country_code = country_code