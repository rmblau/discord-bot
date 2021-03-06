from datetime import datetime

from sqlalchemy.sql.sqltypes import String
from sqlalchemy import select
from user.user import User
from weather.db import Database as db
from babel.units import format_unit
from dataclasses import dataclass


class Weather():

    async def get_location(user_id):
        async with db.create_session() as session:
            user = await session.execute(select(User.weather_location).where(
                User.id == user_id))
            await session.commit()
        return user.scalars().first()

    async def get_country_code(user_id):
        async with db.create_session() as session:
            user = await session.execute(select(User.country_code).where(
                User.id == user_id))
            await session.commit()
        return user.scalars().first()

    async def get_units(user_id):
        async with db.create_session() as session:
            user = await session.execute(select(User.units).where(
                User.id == user_id))
            await session.commit()
        return user.scalars().first()

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
