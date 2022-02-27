from multiprocessing import synchronize
from disnake.interactions.base import Interaction
from user.user import User
from quotes.quote import Quote
from user.base import Session, engine, Base
import asyncio
from sqlalchemy import select, update, insert

import weather


class Database():

    def create_session():
        session = Session()
        return session

    def create_table(self):
        Base.metadata.create_all(engine)

    async def create_user(user_id, user_location, country_code='US', units='imperial'):
        async with Session() as session:
            user = User(id=user_id, weather_location=user_location,
                        country_code=country_code, units=units)
            session.add(user)
            await session.commit()
        return user

    async def update_user(self, user_id, user_location, country_code='US', units='imperial'):

        async with Session() as session:
            user = await session.execute(update(User).
                                         where(User.id == user_id).
                                         values(

                weather_location=user_location,
                country_code=country_code,
                units=units

            ).execution_options(synchronize_session="fetch"))

            await session.commit()
            return user
