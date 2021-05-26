from os.path import isfile
from sqlite3 import connect
import sqlite3
import logging
from sqlite3.dbapi2 import Error

from discord import user


class Database():

    logging.basicConfig(filename='database.log', level=logging.INFO)

    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)

        except Error as e:
            logging.info(e)

        finally:
            if conn:
                conn.close()
        return conn

    def create_table(db_file):
        db = sqlite3.connect(db_file)
        cursor = db.cursor()
        cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS main(
                user_id TEXT,
                weather_loc TEXT
                )
                ''')

    def insert(user_id, user_location):
        db = sqlite3.connect('roran.db')
        cursor = db.cursor()
        sql = f"INSERT INTO main(user_id, weather_loc) VALUES(?,?)"
        values = (user_id, user_location)
        cursor.execute(sql, values)
        db.commit()

    def update(user_id, user_location):
        db = sqlite3.connect('roran.db')
        cursor = db.cursor()
        sql = (
            'UPDATE main SET weather_loc = ? where user_id = ? ')
        values = (user_id, user_location)
        cursor.execute(sql, values)
        db.commit()
