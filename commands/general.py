from os import environ
import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands.core import command
from utils import db
import sqlite3

intents = discord.Intents.default()
intents.members = True


class general(commands.Cog, name="general"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.conn = db.Database.create_connection(environ['DB_NAME'])

    @commands.command(name='ping', help='Responds with pong')
    async def ping(self, context):

        embed = discord.Embed(
        )

        embed.add_field(
            name="Pong!",
            value=":ping_pong",
            inline=True
        )

        await context.send(embed=embed)

    @commands.command(name='set', help='set various variables', intents=intents)
    async def set(self, context, user_location):
        user_id = context.author.id
        cursor = self.conn.cursor()
        cursor.execute(
            f"SELECT user_id FROM main WHERE user_id = {user_id}")
        result = cursor.fetchone()
        if result is None:

            db.Database.insert(user_id, user_location)
            await context.send(f"Prefered location set to {user_location}")

        elif result is not None:

            db.Database.update(user_id, user_location)
            await context.send(f"Location set to {user_location}!")

    @commands.command(name='test', help='used for testing')
    async def test(self, context):
        user_id = context.author.id
        print(user_id)
        cursor = self.conn.cursor()
        cursor.execute(
            f"SELECT weather_loc FROM main WHERE user_id = {user_id}")
        result = cursor.fetchone()
        print(f'Result is:{result}')
        if result is None:
            await context.send(f'Prefered location not set, please set with "!set"')

        elif result is not None:
            db.Database.get_location(user_id)


def setup(bot):
    bot.add_cog(general(bot))
