import disnake
from utils.quotes import add_quote, get_quote, get_quote_time_stamp, get_quotes
from disnake.ext import commands
from disnake.interactions.application_command import \
    ApplicationCommandInteraction
from disnake.ext.commands.errors import CommandInvokeError
from weather.db import Database as db
import pprint


class quotes(commands.Cog, name="quotes"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.session = db.create_session()

    @commands.cooldown(2, 3, commands.BucketType.user)
    @commands.slash_command(name='add_quote', description='add quotes')
    async def add_quote(self, interaction: ApplicationCommandInteraction, quote):
        add_quote(quote=quote)
        await interaction.response.send_message(
            f"quote {quote} added!")

    @commands.cooldown(2, 3, commands.BucketType.user)
    @commands.slash_command(name='get_quote', description='quotes')
    async def get_quote(self, interaction: ApplicationCommandInteraction, quote):
        try:
            embed = disnake.Embed(title="")
            embed.add_field(
                name="Quote", value=f"{get_quote(quote_id=quote)}", inline=False)
            embed.add_field(name=f"Date added",
                            value=f"{get_quote_time_stamp(quote_id=quote)}")
            await interaction.response.send_message(embed=embed)
        except CommandInvokeError as e:
            await interaction.response.send_message(e)

    @commands.cooldown(2, 3, commands.BucketType.user)
    @commands.slash_command(name='get_quotes', description='quotes')
    async def get_quotes(self, interaction: ApplicationCommandInteraction):
        try:
            embed = disnake.Embed(title="")
            embed.add_field(
                name="Quote", value=f"{pprint.pformat(list(get_quotes()))}", inline=False)
            await interaction.response.send_message(embed=embed)
        except CommandInvokeError as e:
            await interaction.response.send_message(e)


def setup(bot):
    bot.add_cog(quotes(bot))
