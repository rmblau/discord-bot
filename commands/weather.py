from threading import Condition
from attr import validate
import babel
from babel.numbers import format_percent
from discord import client
import pprint as pp
import discord
from discord.ext import commands
import requests
from datetime import datetime
from utils.db import Database as db
from utils.db import Weather as w
from babel.units import format_unit
import pgeocode
import aiohttp
import logging
import pandas as pd
from os import environ


class weather(commands.Cog, name="weather"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.weather_token = environ['WEATHER_API_KEY']
        self.conn = db.create_connection(environ['DB_NAME'])

    @commands.command(name='set', help='''set variables for weather: user_location, country_code(US by default), and
    units for temp(imperial by default) invoke with .set
    ''')
    async def set(self, context, user_location, country_code='US', units='imperial'):

        user_id = context.author.id
        cursor = self.conn.cursor()
        sql = f"SELECT user_id FROM main WHERE user_id = ?"
        values = (user_id,)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        if result is None:
            w.insert(user_id, user_location, country_code, units)
            context.send(
                f"Prefered location set to {user_location} {country_code} with {units}")
        elif result is not None:
            w.update(user_id, user_location, country_code, units)
            await context.send(
                f"Location set to {user_location} {country_code} with {units}!")

    @commands.command(name='w', help='''responds with weather at user location
    after setting a location one can call the weather with +w or with +w <postal code> for a different location''')
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

                await context.send(f'Prefered location not set, please set with "+set"')

            elif result is not None:
                user_location = w.get_location(user_id)[0]
                units = w.get_units(user_id)[0]
                country_code = w.get_country_code(user_id)[0]
                await self.show_weather(context, user_location, units, country_code)

    async def show_weather(self, context, user_location, units='imperial', country_code='US'):
        if user_location.isnumeric():
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

        elif country_code != 'US':
            url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': user_location,
                'state code': country_code,
                'units': units,
                'appid': self.weather_token
            }
        # else:
        #    url = "http://api.openweathermap.org/data/2.5/weather"
        #    params = {
        #        'q': user_location,
        #        'state code': country_code,
        #        'units': units,
        #        'appid': self.weather_token
        #    }
        headers = {}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    weather = await response.json()
                    print(pp.pformat(weather))
                    logging.info(pp.pformat(weather))
                    current_conditions = weather['weather'][0]['description']
                    name = weather['name']
                    country = weather['sys']['country']
                    if units == 'metric':
                        current_temp = format_celcius(weather['main']['temp'])
                    else:
                        current_temp = format_fahrenheit(
                            weather['main']['temp'])
                    if units == 'metric':
                        feels_like = format_celcius(
                            weather['main']['feels_like'])
                    else:
                        feels_like = format_fahrenheit(
                            weather['main']['feels_like'])

                    huminity = weather['main']['humidity']
                    high = weather['main']['temp_max']
                    if units == 'metric':

                        low = format_celcius(weather['main']['temp_min'])
                    else:
                        low = format_fahrenheit(weather['main']['temp_min'])
                    weather_icon = weather['weather'][0]['icon']
                    icon_url = f'http://openweathermap.org/img/wn/{weather_icon}@2x.png'
                    if country_code == 'US':
                        embed = discord.Embed(
                            title=f"Weather in {zipcode['place_name']}, {zipcode['state_name']}",
                            color=discord.Color.blue()
                        )
                    else:
                        embed = discord.Embed(
                            title=f"Weather in {name}, {country}"
                        )
                    embed.add_field(
                        name='Current conditions', value=f'**{current_conditions}**', inline=False
                    )
                    embed.add_field(
                        name='Temp', value=f'**{current_temp}**', inline=False
                    )
                    embed.add_field(
                        name='High/Low', value=f'**{high}/{low}**', inline=False
                    )
                    embed.add_field(
                        name='Feels Like', value=f'**{feels_like}**', inline=False
                    )
                    embed.add_field(
                        name='Humidity', value=f'**{huminity}%**', inline=False
                    )
                    embed.set_thumbnail(url=icon_url)

                    await context.reply(embed=embed, mention_author=True)

 #####THIS IS WEATHER FORCAST###############################
    @commands.command(name='wf', help='''responds with weather at user location
    after setting a location one can call the weather with +w or with +w <postal code> for a different location''')
    async def forcast(self, context, user_location=None, units='imperial', country_code='US'):

        if user_location is not None:
            try:

                await self.show_forcast(context, user_location, units, country_code)

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

                await context.send(f'Prefered location not set, please set with "+set"')

            elif result is not None:
                user_location = w.get_location(user_id)[0]
                units = w.get_units(user_id)[0]
                country_code = w.get_country_code(user_id)[0]
                await self.show_forcast(context, user_location, units, country_code)

    async def show_forcast(self, context, user_location, units='imperial', country_code='US'):

        if user_location.isnumeric():
            nomi = pgeocode.Nominatim(country_code)
            zipcode = nomi.query_postal_code(user_location)
            lat = zipcode['latitude']
            lon = zipcode['longitude']
            url = "https://api.openweathermap.org/data/2.5/onecall"
            params = {
                'lon': lon,
                'lat': lat,
                'units': units,
                'appid': self.weather_token
            }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    weather = await response.json()
                    weather_icon = weather['current']['weather'][0]['icon']
                    icon_url = f'http://openweathermap.org/img/wn/{weather_icon}@2x.png'
                    weather_forcast = weather['daily']
                    weather_dict = {
                        'dt': [],
                        'temp': [],
                        'min': [],
                        'max': [],
                        'night': [],
                        'feels_like': [],
                        'conditions': []

                    }
                    for day in weather_forcast:
                        feels_like = weather['current']['feels_like']
                        conditions = day['weather'][0]['description']
                        weather_dict['dt'].append(
                            datetime.fromtimestamp(day['dt']).strftime('%A'))
                        weather_dict['temp'].append(day['temp']['day'])
                        weather_dict['min'].append(day['temp']['min'])
                        weather_dict['max'].append(day['temp']['max'])
                        weather_dict['night'].append(day['temp']['night'])
                        weather_dict['feels_like'].append(feels_like)
                        weather_dict['conditions'].append(conditions)
                        weather_df = pd.DataFrame.from_dict(weather_dict)
                        print(weather_df)
                    embed = discord.Embed(title=f"Forecast for {zipcode['place_name']}, {zipcode['state_name']}",
                                          color=discord.Color.blue())
                    embed.add_field(
                        name=f'{weather_dict["dt"][0]}', value=f'**{weather_dict["max"][0]} / {weather_dict["min"][0]}\n {weather_dict["conditions"][0]}**')

                    embed.add_field(
                        name=f'{weather_dict["dt"][1]}', value=f'**{weather_dict["max"][1]}  / {weather_dict["min"][1]}\n {weather_dict["conditions"][1]}**')
                    embed.add_field(
                        name=f'{weather_dict["dt"][2]}', value=f'**{weather_dict["max"][2]} / {weather_dict["min"][2]} \n{weather_dict["conditions"][2]}**')
                    embed.add_field(
                        name=f'{weather_dict["dt"][3]}', value=f'**{weather_dict["max"][3]} / {weather_dict["min"][3]} \n{weather_dict["conditions"][3]}**')
                    embed.add_field(
                        name=f'{weather_dict["dt"][4]}', value=f'** {weather_dict["max"][4]}/{weather_dict["min"][4]} \n{weather_dict["conditions"][4]}**')
                    embed.add_field(
                        name=f'{weather_dict["dt"][5]}', value=f'** {weather_dict["max"][5]}/{weather_dict["min"][5]} \n{weather_dict["conditions"][5]}**')
                    embed.add_field(
                        name=f'{weather_dict["dt"][6]}', value=f'** {weather_dict["max"][6]}/{weather_dict["min"][6]} \n{weather_dict["conditions"][6]}**')

                    embed.set_footer(
                        icon_url=icon_url,
                        text=f'Currently {weather["current"]["temp"]} Feels like {weather["current"]["feels_like"]}')
                await context.reply(embed=embed, mention_author=True)


def format_celcius(temp):
    celcius = format_unit(
        f'{temp} ', 'temperature-celsius', 'short', locale='en_US')

    return celcius


def format_fahrenheit(temp):
    f = format_unit(f'{temp} ', 'temperature-fahrenheit',
                    'short', locale='en_US')

    return f


def setup(bot):
    bot.add_cog(weather(bot))
