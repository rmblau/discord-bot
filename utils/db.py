from re import U
import sqlalchemy
from sqlalchemy.orm import session
from sqlalchemy.orm.session import sessionmaker
from discord import user
from sqlite3.dbapi2 import Error
import logging
import sqlite3
from sqlite3 import connect
from os.path import isfile
from os import environ
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine
from sqlalchemy import select, update
from utils.User import User
from utils.base import Session, engine, Base


class Database():

    def create_session(engine):
        session = Session()
        return session

    def create_table(self):

        Base.metadata.create_all(engine)


class Weather():

    def insert(user_id, user_location, country_code, units):
        session = Database.create_session(engine)
        with session as session:
            user = User(user_id, user_location, country_code, units)
            session.add(user)
            session.commit()
        return user

    def update(user_id, user_location, country_code='US', units='imperial'):
        session = Database.create_session(engine)
        with session as session:
            user = session.query(User).filter(User.id == user_id).update({
                User.weather_location: user_location,
                User.country_code: country_code,
                User.units: units})
            session.commit()

    def get_location(user_id):
        session = Database.create_session(engine)
        with session as session:
            user = session.query(User.weather_location).filter(
                User.id == user_id).first()
            session.commit()
        return user

    def get_country_code(user_id):

        session = Database.create_session(engine)
        with session as session:
            user = session.query(User.country_code).filter(
                User.id == user_id).first()
            session.commit()
        return user

    def get_units(user_id):
        session = Database.create_session(engine)
        with session as session:
            user = session.query(User.units).filter(
                User.id == user_id).first()
            session.commit()
        return user
