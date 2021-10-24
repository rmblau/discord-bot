import pprint as pp
from os import environ

import aiohttp
import babel.numbers
import disnake
from disnake.ext import commands
from disnake.interactions.application_command import \
    ApplicationCommandInteraction


class stocks(commands.Cog, name="stocks"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.token = environ['STOCK_API_KEY']

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(name='stocks', aliases=['s'], description='current stock prices')
    async def stocks(self, interaction: ApplicationCommandInteraction, symbol):
        # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
        url = 'https://www.alphavantage.co/query'
        params = {
            f"function": "GLOBAL_QUOTE",
            f"symbol": str(symbol).upper(),
            f'apikey': self.token
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    stonks = await response.json()
                    symbol = stonks["Global Quote"]["01. symbol"]
                    open = babel.numbers.format_currency(
                        stonks["Global Quote"]["02. open"], "USD", locale="en_US")
                    high = babel.numbers.format_currency(
                        stonks["Global Quote"]["03. high"], "USD", locale="en_US")
                    low = babel.numbers.format_currency(
                        stonks["Global Quote"]["04. low"], "USD", locale="en_US")
                    price = babel.numbers.format_currency(
                        stonks["Global Quote"]["05. price"], "USD", locale="en_US")
                    volume = babel.numbers.format_decimal(
                        stonks['Global Quote']["06. volume"], locale="en_US")
                    last_day = stonks["Global Quote"]["07. latest trading day"]
                    previous_close = babel.numbers.format_currency(
                        stonks["Global Quote"]["08. previous close"], "USD", locale="en_US")
                    change = babel.numbers.format_currency(
                        stonks["Global Quote"]["09. change"], "USD", locale="en_US")
                    change_percent = stonks["Global Quote"]["10. change percent"]
                    embed = disnake.Embed(
                        color=disnake.Color.green()
                    )

                    embed.add_field(
                        name='symbol',  value=f"**{symbol}**", inline=False
                    )
                    embed.add_field(
                        name='price', value=f"**{price}**", inline=True
                    )

                    embed.add_field(
                        name='open', value=f"**{open}**", inline=True
                    )

                    embed.add_field(
                        name='high', value=f"**{high}**", inline=True
                    )

                    embed.add_field(
                        name='low', value=f"**{low}**", inline=True
                    )

                    embed.add_field(
                        name='volume', value=f"**{volume}**", inline=True
                    )

                    embed.add_field(
                        name='latest trading day', value=f"**{last_day}**", inline=True
                    )

                    embed.add_field(
                        name='previous close', value=f"**{previous_close}**", inline=True
                    )

                    embed.add_field(
                        name='change', value=f"**{change}**", inline=True
                    )

                    embed.add_field(
                        name='change percent', value=f"**{change_percent}**", inline=True
                    )

                    await interaction.response.send_message(embed=embed)
                else:
                    await interaction.response.send_message(f'No company found!')

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(name='convert', aliases=['cvrt'], description='currency conversion')
    async def convert(self, interaction: ApplicationCommandInteraction, from_unit, to_unit):
        url = 'https://www.alphavantage.co/query'
        params = {
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": from_unit,
            "to_currency": to_unit,
            "apikey": self.token
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    bucks = await response.json()
                    from_currency = bucks["Realtime Currency Exchange Rate"]["1. From_Currency Code"]
                    to_currency = bucks["Realtime Currency Exchange Rate"]["3. To_Currency Code"]
                    exchange_rate = bucks["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
                    embed = disnake.Embed(
                        color=disnake.Color.purple()
                    )
                    embed.add_field(
                        name="Conversion", value=f'**1 {from_currency} is {exchange_rate} {to_currency}**', inline=False)

                    await interaction.response.send_message(embed=embed)
                else:
                    await interaction.response.send_message(f'No company found!')


def setup(bot):
    bot.add_cog(stocks(bot))
