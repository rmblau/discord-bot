from os import environ
import discord
from discord.ext import commands
from discord.ext.commands.core import command
#from discord.ext.commands import bot
from discord.ext.commands.bot import Bot as bot
from utils import db

intents = discord.Intents.default()
intents.members = True
client = discord.Client()

class general(commands.Cog, name="general"):
    def __init__(self, bot) -> None:
        self.bot = bot

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

    @commands.command(name="server")
    async def servers(self,ctx):
        await ctx.send(bot.guilds)

def setup(bot):
    bot.add_cog(general(bot))
