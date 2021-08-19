from utils.user import User
from utils.db import Database


class Weather():

    def __init__(self) -> None:
        self.session = Database.create_session()

    def get_location(self, user_id):
        with self.session as session:
            user = session.query(User.weather_location).filter(
                User.id == user_id).first()
            session.commit()
        return user

    def get_country_code(self, user_id):
        with self.session as session:
            user = session.query(User.country_code).filter(
                User.id == user_id).first()
            session.commit()
        return user

    def get_units(self, user_id):
        with self.session as session:
            user = session.query(User.units).filter(
                User.id == user_id).first()
            session.commit()
        return user
