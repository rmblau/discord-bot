from disnake.interactions.base import Interaction
from utils.user import User
from utils.quote import Quote
from utils.base import Session, engine, Base


class Database():

    def create_session():
        session = Session()
        return session

    def create_table(self):

        Base.metadata.create_all(engine)

    def create_user(user_id, user_location, country_code='US', units='imperial'):
        with Session() as session:
            user = User(user_id, user_location, country_code, units)
            session.add(user)
            session.commit()
        return user

    def update_user(self, user_id, user_location, country_code='US', units='imperial'):

        with Session() as session:
            user = session.query(User).filter(User.id == user_id).update({
                User.weather_location: user_location,
                User.country_code: country_code,
                User.units: units})
            session.commit()
            return user
