from discord import client
import pprint as pp
import discord
from discord.ext import commands
from discord.ext.commands import bot
from utils import db
import requests
import pgeocode
import aiohttp
from os import environ
import sqlite3


class weather(commands.Cog, name="weather"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.client = discord.Client()
        self.weather_token = environ['WEATHER_API_KEY']
        self.conn = db.Database.create_connection(environ['DB_NAME'])

    @commands.command(name='w', help='responds with weather at user location')
    async def weather(self, context, user_location=None, units='imperial', country_code='US'):

        if user_location is not None:
            try:

                await self.show_weather(context, user_location, units, country_code)
            except KeyError:
                await context.send(f'Location not set')
        else:

            user_id = context.author.id
            cursor = self.conn.cursor()
            sql = f"SELECT weather_loc FROM main WHERE user_id = ?"
            values = (user_id,)
            cursor.execute(sql, values)
            result = cursor.fetchone()
            print(f'Result is:{result}')
            if result is None:
                print(result)
                await context.send(f'Prefered location not set, please set with "!set"')

            elif result is not None:
                print(result)
                user_location = db.Database.get_location(user_id)[0]
                units = db.Database.get_units(user_id)[0]
                country_code = db.Database.get_country_code(user_id)[0]
                await self.show_weather(context, user_location, units, country_code)

    async def show_weather(self, context, user_location, units='imperial', country_code='US'):
        nomi = pgeocode.Nominatim(country_code)
        zipcode = nomi.query_postal_code(user_location)
        lat = zipcode['latitude']
        lon = zipcode['longitude']
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'lon': lon,
            'lat': lat,
            'units': units,
            'appid': self.weather_token
        }
        headers = {}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    weather = await response.json()
                    print(weather)
                    current_conditions = weather['weather'][0]['description']
                    current_temp = weather['main']['temp']
                    feels_like = weather['main']['feels_like']
                    huminity = weather['main']['humidity']
                    weather_icon = weather['weather'][0]['icon']
                    icon_url = f'http://openweathermap.org/img/wn/{weather_icon}@2x.png'
                    if country_code == 'US':
                        embed = discord.Embed(
                            title=f"Weather in {zipcode['place_name']}, {zipcode['state_name']}"
                        )
                        embed.add_field(
                            name='Current conditions', value=f'**{current_conditions}**', inline=False
                        )
                        embed.add_field(
                            name='Temp', value=f'**{current_temp}**', inline=False
                        )
                        embed.add_field(
                            name='Feels Like', value=f'**{feels_like}**', inline=False
                        )
                        embed.add_field(
                            name='Humidity', value=f'**{huminity} %**', inline=False
                        )
                        embed.set_thumbnail(url=icon_url)
                    else:
                        embed = discord.Embed(
                            title=f"Weather in {zipcode['county_name']}, {zipcode['state_name']}"
                        )
                        embed.add_field(
                            name='Current conditions', value=f'**{current_conditions}**', inline=False
                        )
                        embed.add_field(
                            name='Temp', value=f'**{current_temp}**', inline=False
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
