import os
import discord
from os import environ
from discord.ext import commands
import sqlite3
from db import Database

TOKEN = environ['DISCORD_TOKEN']
client = discord.Client()
bot = commands.Bot(command_prefix='!')

if __name__ == "__main__":
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
    Database.create_connection('roran.db')
    Database.create_table('roran.db')
    print(f'{bot.user.name} has connected to Discord!')


bot.run(TOKEN)
