#!/usr/local/bin/python3
import os
from os import environ
from utils import utils
from disnake.ext.commands.bot import Bot
from utils import db


class MyBot(Bot):

    async def on_ready(self):
        print(f'{self.user.name} has connected to Discord!')


def main():

    bot = MyBot(command_prefix='+')
    token = environ['DISCORD_TOKEN']
    # db.Database.create_table(db.Database)
    logger = utils.get_logger()
    for file in os.listdir("./commands"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"commands.{extension}")
                print(f"Loaded extension '{extension}'")
                logger.info(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                logger.info(
                    f"Failed to load extension {extension}\n{exception}")
                print(f"Failed to load extension {extension}\n{exception}")
    bot.run(token)


if __name__ == "__main__":
    main()
