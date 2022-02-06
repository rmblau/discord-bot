from quotes.quote import Quote
from weather.db import Database as db
from datetime import datetime
from sqlalchemy import select


async def add_quote(quote):
    async with db.create_session() as session:
        quotes = Quote(
            time_stamp=datetime.today(), quote=quote)
        await session.add(quotes)
        await session.commit()
        return quotes


async def get_quote(quote_id):
    async with db.create_session() as session:
        result = await session.execute(select(Quote.quote).where(
            Quote.id == quote_id)).first()
        await session.commit()
        return result.scalar().first()


async def get_quotes():
    async with db.create_session() as session:
        rows = await session.execute(select(Quote.quote))
        row = rows.scalars().all()
        yield row


async def get_quote_time_stamp(quote_id):
    async with db.create_session() as session:
        result = await session.execute(select((Quote.time_stamp).where(
            Quote.id == quote_id)))
        await session.commit()
    return result.strftime("%Y-%m-%d")
