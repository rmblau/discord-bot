import pprint as pp
import discord
from discord.ext import commands
from discord.ext.commands import bot
import requests
import logging
from datetime import datetime
import aiohttp
import asyncio
import babel.numbers
from os import environ, name


class stocks(commands.Cog, name="stocks"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.token = environ['STOCK_API_KEY']

    @commands.command(name='stocks', help='Use +stocks and the name of the company, i.e, +stocks GME.')
    async def stocks(self, context, symbol):
        # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
        url = 'https://www.alphavantage.co/query'
        params = {
            f"function": "GLOBAL_QUOTE",
            f"symbol": symbol,
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
                    volume = babel.numbers.format_currency(
                        stonks['Global Quote']["06. volume"], "USD", locale="en_US")
                    last_day = stonks["Global Quote"]["07. latest trading day"]
                    previous_close = babel.numbers.format_currency(
                        stonks["Global Quote"]["08. previous close"], "USD", locale="en_US")
                    change = babel.numbers.format_currency(
                        stonks["Global Quote"]["09. change"], "USD", locale="en_US")
                    change_percent = stonks["Global Quote"]["10. change percent"]
                    embed = discord.Embed(
                        color=discord.Color.green()
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

                    await context.reply(embed=embed)
                else:
                    await context.send(f'No company found!')


def setup(bot):
    bot.add_cog(stocks(bot))
