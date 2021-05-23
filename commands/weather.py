from pyzipcode import ZipCodeDatabase
import pprint as pp
import discord
from discord.ext import commands
from discord.ext.commands import bot
import requests
from os import environ

class weather(commands.Cog, name="weather"):
    def __init__(self,bot) -> None:
        self.bot = bot
        self.weather_token = environ['WEATHER_API_KEY']

    @commands.command(name='weather', help='responds with weather at user location')
    async def weather(self, context, user_location):
        zcdb = ZipCodeDatabase()
        zip = zcdb[user_location]
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'zip': f'{user_location},us',
            'units': 'imperial',
            'appid': self.weather_token
        }
        headers = {}

        response = requests.get(url, headers=headers, params=params)
        weather = response.json()
        current_conditions = weather['weather'][0]['description']
        current_temp = weather['main']['temp']
        feels_like = weather['main']['feels_like']
        huminity = weather['main']['humidity']
        weather_icon = weather['weather'][0]['icon']
        icon_url = f'http://openweathermap.org/img/wn/{weather_icon}@2x.png'
        embed = discord.Embed(
            title = f'Weather in {zip.city}, {zip.state}'
        )
        
        embed.add_field(
            name = 'Current conditions', value=f'**{current_conditions}**', inline=False
        )
        embed.add_field(
            name = 'Temp', value=f'**{current_temp}**', inline=False
        )
        embed.add_field(
            name='Feels Like', value=f'**{feels_like}**', inline=False
        )
        embed.add_field(
            name='Humidity', value=f'**{huminity} %**', inline=False
        )
        embed.set_thumbnail(url=icon_url)
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(weather(bot))
