from utils import quote
from utils.quote import Quote
from utils.db import Database as db
from datetime import datetime
from sqlalchemy import select


def add_quote(quote):
    with db.create_session() as session:
        quotes = Quote(
            time_stamp=datetime.today(), quote=quote)
        session.add(quotes)
        session.commit()
    return quotes


def get_quote(quote_id):
    with db.create_session() as session:
        result = session.query(Quote.quote).where(
            Quote.id == quote_id).one()
        session.commit()
    return result[0]


def get_quotes():
    with db.create_session() as session:
        for row in session.query(Quote.quote).all():
            yield row


def get_quote_time_stamp(quote_id):
    with db.create_session() as session:
        result = session.query(Quote.time_stamp).where(
            Quote.id == quote_id).one()
        session.commit()
    return result[0].strftime("%Y-%m-%d")
