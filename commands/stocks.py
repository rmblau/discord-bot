import pprint as pp
import discord
from discord.ext import commands
from discord.ext.commands import bot
import requests
import logging
import aiohttp
import asyncio
from os import environ


class stocks(commands.Cog, name="stocks"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.token = environ['STOCK_API_KEY']

    @commands.command(name='stocks', help='responds with stock data')
    async def news(self, context, symbol):
        # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
        url = 'https://www.alphavantage.co/query'
        params = {
            f"function": "TIME_SERIES_INTRADAY",
            f"symbol": {symbol},  # remove later
            f'interval': '5min',
            f'apikey': self.token
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    print(response)
                    stonks = await response.json()
                    print(pp.pformat(stonks))
                    for stonk in stonks['Meta Data'].items():
                        embed = discord.Embed(
                            title=f'Information'
                        )
                        embed.add_field(
                            name='Symbol', value=f'**{stonk[:][1]}**', inline=False
                        )
                        for data in stonks['Time Series (5min)'].items():
                            embed.add_field(
                                name='Description', value=f'**{data[:][1]}**', inline=False
                            )

                            await context.send(embed=embed)
                else:
                    await context.send(f'No articles found!')


def setup(bot):
    bot.add_cog(stocks(bot))
