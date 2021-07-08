from collections import namedtuple
from os import environ
import discord
from discord import channel
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands.core import Command, command, hooked_wrapped_callback
from discord.ext.commands.help import HelpCommand
from utils import db
import sqlite3

intents = discord.Intents.default()
intents.members = True


class Help(commands.MinimalHelpCommand):

    @commands.cooldown(1, 5, commands.BucketType.user)
    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command))
        embed.add_field(name="Help", value=command.help)
        aliases = command.aliases
        if aliases:
            embed.add_field(name='Aliases', value=", ".join(
                aliases), inline=False)
        channel = self.get_destination()
        await channel.send(embed=embed)


class HelpCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        help_command = Help()
        help_command.cog = self
        bot.help_command = help_command


def setup(bot):
    bot.add_cog(HelpCog(bot))
