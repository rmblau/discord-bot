from os import environ
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
        
        db = sqlite3.connect(environ['DB_NAME'])
        cursor = db.cursor()
        sql = f"INSERT INTO main(user_id, weather_loc) VALUES(?,?)"
        values = (user_id, user_location)
        cursor.execute(sql, values)
        db.commit()
        db.close()

    def update(user_location, user_id):
        db = sqlite3.connect(environ['DB_NAME'])
        cursor = db.cursor()
        sql = (
            f'UPDATE main SET weather_loc = ? where user_id = ? ')
        values = (user_id, user_location)
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
