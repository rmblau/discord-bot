from utils import quote
from quotes.quotes import Quote
from weather.db import Database as db
from datetime import datetime
from sqlalchemy import select


async def add_quote(quote):
    async with db.create_session() as session:
        quotes = Quote(
            time_stamp=datetime.today(), quote=quote)
        session.add(quotes)
        await session.commit()
        return quotes


async def get_quote(quote_id):
    async with db.create_session() as session:
        result = session.execute(select(Quote.quote).where(
            Quote.id == quote_id))
        await session.commit()
        return result.scalars().first()


async def get_quotes():
    async with db.create_session() as session:
        for row in session.execute(select((Quote.quote))).all():
            yield row


def get_quote_time_stamp(quote_id):
    with db.create_session() as session:
        result = session.execute(select((Quote.time_stamp).where(
            Quote.id == quote_id))
        await session.commit()
    return result.strftime("%Y-%m-%d")
