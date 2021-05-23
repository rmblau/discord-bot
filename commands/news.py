import pprint as pp
import discord
from discord.ext import commands
from discord.ext.commands import bot
import requests
from newsapi import NewsApiClient
from os import environ


class news(commands.Cog, name="news"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.news_token = environ['NEWS_API_KEY']

    @commands.command(name='news', help='responds with news about a topic')
    async def news(self, context, topic,):
        
        url = "https://free-news.p.rapidapi.com/v1/search"

        querystring = {"q": f"{topic}", "lang": "en",
                       "page_size": 1}

        headers = {
            'x-rapidapi-key': self.news_token,
            'x-rapidapi-host': "free-news.p.rapidapi.com"
        }

        the_news = requests.get(
        url, headers=headers, params=querystring).json()
        for article in the_news['articles']:
            
            embed = discord.Embed(
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
            embed.set_image(url=article['media'])
            await context.send(embed=embed)


def setup(bot):
    bot.add_cog(news(bot))


