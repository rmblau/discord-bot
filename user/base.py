from os import environ
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.schema import MetaData
engine = create_async_engine(
    f'postgresql+asyncpg://postgres:R2dkY9Lra=>8.Xz2@db:5433/postgres', echo=True,)

Session = sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()
metadata = MetaData()
