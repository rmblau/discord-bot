from os import environ
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.schema import MetaData
engine = create_engine(
    f'postgresql://postgres:postgres@db: 5433/postgres', echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()
metadata = MetaData()
