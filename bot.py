import os
from os import environ
from discord import client
import discord
import disnake
from utils import utils
#from discord.ext.commands.bot import Bot
from disnake.ext.commands.bot import Bot
from utils import db


class MyBot(Bot):

    async def on_ready(self):
        print(f'{self.user.name} has connected to Discord!')


Bot = MyBot(command_prefix='+')

TOKEN = environ['DISCORD_TOKEN']


if __name__ == "__main__":
    # db.Database.create_table(db.Database)
    logger = utils.get_logger()
    for file in os.listdir("./commands"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                Bot.load_extension(f"commands.{extension}")
                print(f"Loaded extension '{extension}'")
                logger.info(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                logger.info(
                    f"Failed to load extension {extension}\n{exception}")
Bot.run(TOKEN)
