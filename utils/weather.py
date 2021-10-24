from utils.user import User
from utils.db import Database as db
from .base import Session


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
