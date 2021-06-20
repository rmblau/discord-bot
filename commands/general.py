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

    @commands.command(name='onboard', help='Onboarding script')
    async def onboard(self, context):

        user = context.author
        await user.send('Hello!')

    @commands.command(name='ping', help='Responds with pong')
    async def ping(self, context):

        embed = discord.Embed(
        )

        embed.add_field(
            name="Pong!",
            value=":ping_pong:",
            inline=True
        )

        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(general(bot))
