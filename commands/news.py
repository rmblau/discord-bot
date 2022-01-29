import asyncio
import logging
import pprint as pp
from os import environ

import aiohttp
import disnake
from dislash.interactions import interaction
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from utils import utils


class news(commands.Cog, name="news"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.news_token = environ['NEWS_API_KEY']
        self.logger = utils.get_logger()

    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.slash_command(name='news', description='news stories')
    async def news(self, interaction: ApplicationCommandInteraction, *, topic):

        url = "https://free-news.p.rapidapi.com/v1/search"

        params = {"q": f"{topic}", "lang": "en",
                       "page_size": 1}

        headers = {
            'x-rapidapi-key': self.news_token,
            'x-rapidapi-host': "free-news.p.rapidapi.com"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                print(response)
                #user = interaction.author
                self.logger.info(pp.pformat(response))
                if response.status == 200:
                    print(response)
                    self.logger.info(response)
                    the_news = await response.json()
                    print(the_news)
                    for article in the_news['articles']:
                        embed = disnake.Embed(
                            title=f'Top headlines'
                        )
                        embed.add_field(
                            name='Headline', value=f'**{article["title"]}**', inline=False
                        )
                        embed.add_field(
                            name='Description', value=f'**{article["summary"]}**', inline=False
                        )
                        embed.add_field(
                            name='See more:', value=f'**{article["link"]}**', inline=False
                        )
                        if article['media'] is not None:
                            embed.set_image(url=article['media'])

                            await interaction.author.send(embed=embed)
                        else:
                            print('no media found')
                            await interaction.response.send_message(embed=embed)
                else:
                    await interaction.response.send_message(f'No articles found!')


def setup(bot):
    bot.add_cog(news(bot))
