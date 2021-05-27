import logging
import os
import discord
from os import environ
from discord.ext import commands
import sqlite3
from utils import db

TOKEN = environ['DISCORD_TOKEN']
client = discord.Client()
bot = commands.Bot(command_prefix='!')


def setup_logging():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(
        filename='./logs/discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)


if __name__ == "__main__":
    setup_logging()
    for file in os.listdir("./commands"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"commands.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


@bot.event
async def on_ready():
    db.Database.create_connection(environ['DB_NAME'])
    db.Database.create_table(environ['DB_NAME'])
    print(f'{bot.user.name} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author.bot:
        return
bot.run(TOKEN)
