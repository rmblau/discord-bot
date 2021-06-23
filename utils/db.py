from discord import user
from sqlite3.dbapi2 import Error
import logging
import sqlite3
from sqlite3 import connect
from os.path import isfile
from os import environ


class Database():

    logging.basicConfig(filename='database.log', level=logging.INFO)

    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)

        except Error as e:
            logging.info(e)

        return conn

    def create_table(db_file):
        db = sqlite3.connect(db_file)
        cursor = db.cursor()
        cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS main(
                user_id TEXT,
                weather_loc TEXT,
                units TEXT,
                country_code TEXT
                )
                ''')


class Weather():

    def insert(user_id, user_location, country_code, units):

        db = sqlite3.connect(environ['DB_NAME'])
        cursor = db.cursor()
        sql = f"INSERT INTO main(user_id, weather_loc, units,country_code) VALUES(?,?,?,?)"
        values = (user_id, user_location, units, country_code)
        cursor.execute(sql, values)
        db.commit()
        db.close()

    def update(user_id, user_location, country_code='US', units='imperial'):
        db = sqlite3.connect(environ['DB_NAME'])
        cursor = db.cursor()
        sql = (
            f'UPDATE main SET weather_loc = ?, country_code = ?, units = ? where user_id = ? ')
        values = (user_location, country_code, units, user_id)
        cursor.execute(sql, values)
        db.commit()
        db.close()

    def get_location(user_id):

        db = sqlite3.connect(environ['DB_NAME'])
        cursor = db.cursor()
        sql = (
            f'SELECT weather_loc FROM main where user_id = ?'
        )
        values = (user_id,)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        db.commit()
        print(result)
        return result

    def get_country_code(user_id):

        db = sqlite3.connect(environ['DB_NAME'])
        cursor = db.cursor()
        sql = (
            f'SELECT country_code FROM main where user_id = ?'
        )
        values = (user_id,)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        db.commit()
        print(result)
        return result

    def get_units(user_id):

        db = sqlite3.connect(environ['DB_NAME'])
        cursor = db.cursor()
        sql = (
            f'SELECT units FROM main where user_id = ?'
        )
        values = (user_id,)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        db.commit()
        print(result)
        return result
