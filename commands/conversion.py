from os import environ

import aiohttp
import discord
from discord.ext import commands


class conversion(commands.Cog, name="stocks"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.token = environ['STOCK_API_KEY']

    @commands.group(name='convert', aliases=['cvrt'], help='Use + convert followed by the currency you want to convert from and too, i.e, +stocks USD JPY.')
    # @commands.command(name = 'convert', aliases = ['cvrt'], help = 'Use +convert followed by the currency you want to convert from and too, i.e, +stocks USD JPY.')
    async def convert(self, context, from_unit, to):
        # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
        return from_unit, to

    @convert.command(name='currency')
    async def currency(self, context, from_unit, to_unit):
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
                    print(exchange_rate)
                    embed = discord.Embed(
                        color=discord.Color.purple()
                    )
                    embed.add_field(
                        name="Conversion", value=f'**1 {from_currency} is {exchange_rate} {to_currency}**', inline=False)

                    await context.reply(embed=embed)
                else:
                    await context.send(f'No company found!')


# def setup(bot):
#    bot.add_cog(conversion(bot))
