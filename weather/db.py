from disnake.interactions.base import Interaction
from user.user import User
from quotes.quote import Quote
from user.base import Session, engine, Base
import asyncio
from sqlalchemy import select, update

import weather


class Database():

    def create_session():
        session = Session()
        return session

    def create_table(self):
        Base.metadata.create_all(engine)

    async def create_user(user_id, user_location, country_code='US', units='imperial'):
        async with Session() as session:
            user = User(user_id, user_location, country_code, units)
            session.add(user)
            await session.commit()
        return user

    async def update_user(self, user_id, user_location, country_code='US', units='imperial'):

        async with Session() as session:
            user = session.query(User).filter(User.id).where(User.id == user_id).update({
                User.weather_location: user_location,
                User.country_code: country_code,
                User.units: units})
            await session.commit()
            return user
