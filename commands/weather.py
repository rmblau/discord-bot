import pprint as pp
import babel
import discord
from discord.ext import commands
from datetime import datetime

from sqlalchemy.sql.elements import Null
from utils.db import Database as db
from utils.db import Weather as w
from babel.units import format_unit
import pgeocode
from geopy.geocoders import Nominatim
import aiohttp
import logging
import pandas as pd
from utils.User import User
from utils.base import Session, engine, Base
import sqlalchemy.orm.session as session
from sqlalchemy import select
from os import environ


class weather(commands.Cog, name="weather"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.weather_token = environ['WEATHER_API_KEY']

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name='set', help='''set variables for weather: user_location, country_code(US by default), and
    units for temp(imperial by default) invoke with +set
    ''')
    async def set(self, context, user_location, country_code='US', units='imperial'):
        session = Session()
        user_id = context.author.id
        with session as session:
            result = session.query(User.weather_location).where(
                User.id == user_id).first()
        if result is None:
            w.insert(user_id, user_location, country_code, units)
            await context.send(
                f"Prefered location set to {user_location} {country_code} with {units}")
        elif result is not None:
            w.update(user_id, user_location, country_code, units)
            await context.send(
                f"Location set to {user_location} {country_code} with {units}!")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='w', help='''responds with weather at user location
    after setting a location one can call the weather with +w or with +w <postal code> for a different location''')
    async def weather(self, context, user_location=None, country_code='US', units='imperial',):

        if user_location is not None:

            try:
                await self.show_weather(context, user_location, country_code, units)

            except KeyError:

                await context.send(f'Location not set')
        else:
            user_id = context.author.id
            session = db.create_session(engine)
            with session as session:
                result = session.query(User.weather_location).where(
                    User.id == user_id).one()
                session.commit()
            print(f'Result is:{result}')

            if result is None:

                await context.send(f'Prefered location not set, please set with "+set"')

            elif result is not None:
                user_location = w.get_location(user_id)[0]
                units = w.get_units(user_id)[0]
                country_code = w.get_country_code(user_id)[0]
                await self.show_weather(context, user_location, country_code, units)

    async def show_weather(self, context, user_location, country_code='US', units='imperial'):
        url = "http://api.openweathermap.org/data/2.5/weather"
        if user_location.isnumeric():
            nomi = pgeocode.Nominatim(country_code)
            zipcode = nomi.query_postal_code(user_location)
            lat = zipcode['latitude']
            lon = zipcode['longitude']

            params = {
                'lon': lon,
                'lat': lat,
                'units': units,
                'appid': self.weather_token
            }

        elif country_code != 'US':

            params = {
                'q': user_location,
                'state code': country_code,
                'units': units,
                'appid': self.weather_token
            }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    weather = await response.json()
                    color = discord.Color.blue()
                    logging.info(pp.pformat(weather))
                    huminity = weather['main']['humidity']
                    high = weather['main']['temp_max']
                    low = weather['main']['temp_min']
                    current_temp = weather['main']['temp']
                    feels_like = weather['main']['feels_like']
                    current_conditions = weather['weather'][0]['description']
                    name = weather['name']
                    country = weather['sys']['country']
                    if units == 'metric':
                        current_temp = format_celcius(current_temp)
                        feels_like = format_celcius(
                            feels_like)
                        high = format_celcius(high)
                        low = format_celcius(low)
                    else:
                        current_temp = format_fahrenheit(
                            current_temp)
                        feels_like = format_fahrenheit(
                            feels_like)
                        high = format_fahrenheit(high)
                        low = format_fahrenheit(low)
                    weather_icon = weather['weather'][0]['icon']
                    icon_url = f'http://openweathermap.org/img/wn/{weather_icon}@2x.png'
                    if country_code == 'US':
                        embed = discord.Embed(
                            title=f"Weather in {zipcode['place_name']}, {zipcode['state_name']}",
                            color=color
                        )
                    else:
                        embed = discord.Embed(
                            title=f"Weather in {name}, {country}",
                            color=color
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
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='wf', help='''responds with a 7 day forecast at user location
    after setting a location. can be called with +wf or +wf <user_location> for a different location''')
    async def forecast(self, context, user_location=None, country_code='US', units='imperial',):

        if user_location is not None:
            try:

                await self.show_forecast(context, user_location, country_code, units)

            except KeyError:

                await context.send(f'Location not set')
        else:
            user_id = context.author.id
            session = db.create_session(engine)
            with session as session:
                result = session.query(User.weather_location).where(
                    User.id == user_id).one()
                session.commit()

            if result is None:

                await context.send(f'Prefered location not set, please set with "+set"')

            elif result is not None:
                user_location = w.get_location(user_id)[0]
                units = w.get_units(user_id)[0]
                country_code = w.get_country_code(user_id)[0]
                await self.show_forecast(context, user_location, country_code, units)

    async def show_forecast(self, context, user_location, country_code='US', units='imperial'):

        if user_location.isnumeric():
            nomi = pgeocode.Nominatim(country_code)
            zipcode = nomi.query_postal_code(user_location)
            lat = zipcode['latitude']
            lon = zipcode['longitude']
        else:
            geo = Nominatim(user_agent='Roran')
            location = geo.geocode(f'{user_location},{country_code}')
            lat = location.latitude
            lon = location.longitude
            print(location)
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

                        conditions = day['weather'][0]['description']
                        if units == 'metric':
                            temp = format_celcius(day['temp']['day'])
                            low = format_celcius(day['temp']['min'])
                            high = format_celcius(day['temp']['max'])
                            night = format_celcius(day['temp']['night'])
                            feels_like = format_celcius(
                                weather['current']['feels_like'])
                        else:
                            temp = format_fahrenheit(day['temp']['day'])
                            low = format_fahrenheit(day['temp']['min'])
                            high = format_fahrenheit(day['temp']['max'])
                            night = format_fahrenheit(day['temp']['night'])
                            feels_like = format_fahrenheit(
                                weather['current']['feels_like'])
                        weather_dict['temp'].append(temp)
                        weather_dict['min'].append(low)
                        weather_dict['max'].append(high)
                        weather_dict['night'].append(night)
                        weather_dict['feels_like'].append(feels_like)

                        weather_dict['dt'].append(
                            datetime.fromtimestamp(day['dt']).strftime('%A'))

                        weather_dict['conditions'].append(conditions)
                        if user_location.isnumeric():
                            embed = discord.Embed(title=f"Forecast for {zipcode['place_name']}, {zipcode['state_name']}",
                                                  color=discord.Color.blue())
                        elif ~user_location.isnumeric():
                            embed = discord.Embed(title=f"Forecast for {user_location}, {country_code}",
                                                  color=discord.Color.blue())
                    embed.add_field(
                        name=f'Today', value=f'**{weather_dict["max"][0]}/{weather_dict["min"][0]}\n {weather_dict["conditions"][0]}**')

                    embed.add_field(
                        name=f'Tomorrow', value=f'**{weather_dict["max"][1]}/{weather_dict["min"][1]}\n {weather_dict["conditions"][1]}**')
                    embed.add_field(
                        name=f'{weather_dict["dt"][2]}', value=f'**{weather_dict["max"][2]}/{weather_dict["min"][2]} \n{weather_dict["conditions"][2]}**')
                    embed.add_field(
                        name=f'{weather_dict["dt"][3]}', value=f'**{weather_dict["max"][3]}/{weather_dict["min"][3]} \n{weather_dict["conditions"][3]}**')
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
