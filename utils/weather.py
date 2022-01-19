from datetime import datetime

from sqlalchemy.sql.sqltypes import String
from utils.user import User
from utils.db import Database as db
from babel.units import format_unit
from dataclasses import dataclass


class Weather():

    def get_location(user_id):
        with db.create_session() as session:
            user = session.query(User.weather_location).filter(
                User.id == user_id).first()
            session.commit()
        return user

    def get_country_code(user_id):
        with db.create_session() as session:
            user = session.query(User.country_code).filter(
                User.id == user_id).first()
            session.commit()
        return user

    def get_units(user_id):
        with db.create_session() as session:
            user = session.query(User.units).filter(
                User.id == user_id).first()
            session.commit()
        return user

    def format_celcius(temp):
        celcius = format_unit(
            f'{temp} ', 'temperature-celsius', 'short', locale='en_US')
        return celcius

    def format_fahrenheit(temp):
        f = format_unit(f'{round(temp)} ', 'temperature-fahrenheit',
                        'short', locale='en_US')
        return f


@dataclass
class WeatherConditions:
    dt: datetime
    temp: str
    min: str
    max: str
    night: str
    feels_like: str
    conditions: str
