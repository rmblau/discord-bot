from os import environ

import aiohttp
import babel.numbers
import disnake
from disnake.ext import commands
from disnake.interactions.application_command import ApplicationCommandInteraction


class crypto(commands.Cog, name="crypto"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.token = environ['CRYPTO_KEY']

    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.slash_command(name='c', aliases=['crypto'], description='current crpytocurrency prices')
    async def crypto(self, interaction: ApplicationCommandInteraction, symbol):
        icon = f'https://icons.bitbot.tools/api/{str(symbol).upper()}/128x128'
        # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
        url = "https://api.nomics.com/v1/currencies/ticker"
        params = {
            'key': self.token,
            'ids': symbol,
            'interval': '1d',
            'convert': 'USD',
            'per-page': 100,
            'page': 1,
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    crypto = await response.json()
                    data = crypto[0]
                    print(data['logo_url'])
                    symbol = data["id"]
                    price = babel.numbers.format_currency(
                        data["price"],  "USD", locale="en_US")
                    high = babel.numbers.format_currency(
                        data["high"], "USD", locale="en_US")
                    market_cap = babel.numbers.format_currency(
                        data["market_cap"], "USD", locale="en_US")
                    market_cap_change = babel.numbers.format_currency(
                        data["1d"]["market_cap_change"], "USD", locale="en_US")
                    market_cap_change_percent = babel.numbers.format_percent(
                        data["1d"]["market_cap_change_pct"], format="##.####", locale="en_US")

                    embed = disnake.Embed(
                        color=disnake.Color.gold()
                    )

                    embed.add_field(
                        name='symbol',  value=f"**{symbol}**", inline=False
                    )

                    embed.add_field(
                        name='price', value=f"**{price}**")

                    embed.add_field(
                        name='high', value=f"**{high}**")

                    embed.add_field(
                        name='market cap', value=f"**{market_cap}**")

                    embed.add_field(
                        name='market cap change', value=f"**{market_cap_change}**")

                    embed.add_field(
                        name='market cap change percent', value=f"**{market_cap_change_percent}**")

                    embed.set_thumbnail(url=icon)
                    await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(crypto(bot))
