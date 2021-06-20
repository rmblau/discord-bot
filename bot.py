import os
import discord
import logging
from os import environ
from discord import client

from discord.ext.commands.bot import Bot
from utils import db
from discord.ext import commands
import sqlite3


class MyBot(commands.Bot):

    async def on_ready(self):
        db.Database.create_connection('roran.db')
        db.Database.create_table('roran.db')
        print(f'{self.user.name} has connected to Discord!')


client = MyBot(command_prefix='~')
TOKEN = environ['DISCORD_TOKEN']

if __name__ == "__main__":
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(
        filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    for file in os.listdir("./commands"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                client.load_extension(f"commands.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")

client.run(TOKEN)
