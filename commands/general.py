import discord
from discord.ext import commands
from discord.ext.commands import bot
from db import Database
import sqlite3

intents = discord.Intents.default()
intents.members = True


class general(commands.Cog, name="general"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.conn = Database.create_connection('roran.db')

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
        conn = sqlite3.connect('roran.db')
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT user_id FROM main WHERE user_id = {user_id}")
        result = cursor.fetchone()
        if result is None:

            Database.insert(user_id, user_location)

            await context.send(f"Info updated!")
        elif result is not None:

            Database.update(user_location)


def setup(bot):
    bot.add_cog(general(bot))
