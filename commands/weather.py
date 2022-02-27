import imp
from disnake.ext.commands import context
from builtins import Exception, help
from pprint import pprint
import logging
import pprint as pp
from datetime import datetime
from os import environ

import aiohttp
import disnake
from disnake.ext.commands.errors import CommandInvokeError
import pgeocode
from disnake.ext import commands
from disnake.interactions.application_command import \
    ApplicationCommandInteraction
from geopy.geocoders import Nominatim
from sqlalchemy import select
from weather.db import Database as db
from user.user import User
from utils.utils import get_logger
from weather.weather import Weather as w


class weather(commands.Cog, name="weather"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.weather_token = environ['WEATHER_API_KEY']
        self.session = db.create_session()
        self.logger = get_logger()

    @commands.cooldown(2, 3, commands.BucketType.user)
    @commands.slash_command(name='set', help='''set variables for weather: user_location, country_code(US by default), and
    units for temp(imperial by default) invoke with /set
    ''')
    async def set(self, interaction: ApplicationCommandInteraction, user_location, country_code='US', units='imperial'):
        user_id = interaction.author.id
        async with self.session as session:
            if await w.get_location(user_id=user_id):
                await db.update_user(self, user_id, user_location, country_code, units)
                await interaction.response.send_message(f"Location set to {user_location} {country_code} with {units}", ephemeral=True)
            else:
                await db.create_user(user_id, user_location, country_code, units)
                await interaction.response.send_message(f"Prefered location set to {user_location} {country_code} with {units}", ephemeral=True)
            await session.commit()

    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.slash_command(name='w', description='current weather')
    async def weather(self, interaction: ApplicationCommandInteraction, user_location=None, country_code='US', units='imperial',):

        if user_location is not None:

            try:
                await self.show_weather(interaction, user_location, country_code, units)

            except Exception as e:
                print(e)
                self.logger.info(e)
        else:
            user_id = interaction.author.id
            async with self.session as session:
                result = await session.execute(select(User.weather_location).where(
                    User.id == user_id))
                await session.commit()
            self.logger.info(f'Result is: {result}')

            if result is None:

                await interaction.response.send_message(f'Prefered location not set, please set with "/set"')

            elif result is not None:
                try:
                    user_location = await w.get_location(user_id=user_id)
                    self.logger.info(user_location)
                    units = await w.get_units(user_id=user_id)
                    country_code = await w.get_country_code(user_id=user_id)
                    await self.show_weather(interaction, user_location, country_code, units)
                except Exception as e:
                    print(e)

    async def show_weather(self, interaction: ApplicationCommandInteraction, user_location, country_code='US', units='imperial'):
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
            self.logger.info(location)
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
                    weather_forecast = weather['daily']
                    conditions = [conditions['weather'][0]['description']
                                  for conditions in weather_forecast]
                    day = [datetime.fromtimestamp(day['dt']).strftime(
                        '%A') for day in weather_forecast]

                    if units == 'metric':
                        temp = w.format_celcius(weather['current']['temp'])
                        feels_like = w.format_celcius(
                            weather['current']['feels_like'])
                        max = [w.format_celcius(max['temp']['max'])
                               for max in weather_forecast]
                        min = [w.format_celcius(min['temp']['min'])
                               for min in weather_forecast]
                    else:
                        temp = w.format_fahrenheit(weather['current']['temp'])
                        feels_like = w.format_fahrenheit(
                            weather['current']['feels_like'])
                        max = [w.format_fahrenheit(
                            max['temp']['max']) for max in weather_forecast]
                        min = [w.format_fahrenheit(
                            min['temp']['min']) for min in weather_forecast]

                        if user_location.isnumeric():
                            embed = disnake.Embed(title=f"Weather for {zipcode['place_name']}",
                                                  color=disnake.Color.blue())
                        elif ~user_location.isnumeric():
                            embed = disnake.Embed(title=f"Weather for {user_location}, {country_code}",
                                                  color=disnake.Color.blue())
                    embed.add_field(name='Current Conditions',
                                    value=f'**{conditions[0]}**', inline=False)
                    embed.add_field(
                        name="Temp", value=f"**{temp}**", inline=False)
                    embed.add_field(
                        name=f'High/Low', value=f'**{max[0]}/{min[0]}**')
                    embed.add_field(
                        name=f"Feels like", value=f"**{feels_like}**", inline=False)
                    embed.add_field(
                        name="Humidity", value=f"**{weather['current']['humidity']}%**", inline=False)

                embed.set_thumbnail(url=icon_url)
                await interaction.response.send_message(embed=embed, ephemeral=False)

    @ commands.cooldown(2, 5, commands.BucketType.user)
    @ commands.slash_command(name='wf', description='7 day forecast')
    async def forecast(self, interaction: ApplicationCommandInteraction, user_location=None, country_code='US', units='imperial',):

        if user_location is not None:
            try:

                await self.show_forecast(interaction, user_location, country_code, units)

            except Exception as e:
                self.logger.info(e)
        else:
            user_id = interaction.author.id
            async with self.session as session:
                result = await session.execute(select(User.weather_location).where(
                    User.id == user_id))
                await session.commit()

            if result is None:

                await interaction.response.send_message(f'Prefered location not set, please set with "+set"')

            elif result is not None:
                user_location = await w.get_location(user_id)
                units = await w.get_units(user_id)
                country_code = await w.get_country_code(user_id)
                await self.show_forecast(interaction, user_location, country_code, units)

    async def show_forecast(self, interaction: ApplicationCommandInteraction, user_location, country_code='US', units='imperial'):

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
            self.logger.info(location)
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
                    weather_forecast = weather['daily']
                    conditions = [conditions['weather'][0]['description']
                                  for conditions in weather_forecast]
                    day = [datetime.fromtimestamp(day['dt']).strftime(
                        '%A') for day in weather_forecast]

                    if units == 'metric':
                        max = [w.format_celcius(max['temp']['max'])
                               for max in weather_forecast]
                        min = [w.format_celcius(min['temp']['min'])
                               for min in weather_forecast]
                    else:
                        max = [w.format_fahrenheit(
                            max['temp']['max']) for max in weather_forecast]
                        min = [w.format_fahrenheit(
                            min['temp']['min']) for min in weather_forecast]

                        if user_location.isnumeric():
                            embed = disnake.Embed(title=f"Forecast for {zipcode['place_name']}",
                                                  color=disnake.Color.blue())
                        elif ~user_location.isnumeric():
                            embed = disnake.Embed(title=f"Forecast for {user_location}, {country_code}",
                                                  color=disnake.Color.blue())
                    embed.add_field(
                        name=f'Today', value=f'**{max[0]}/{min[0]}\n {conditions[0]}**')

                    embed.add_field(
                        name=f'Tomorrow', value=f'**{max[1]}/{min[1]}\n {conditions[1]}**')
                    embed.add_field(
                        name=f'{day[2]}', value=f'**{max[2]}/{min[2]} \n{conditions[2]}**')
                    embed.add_field(
                        name=f'{day[3]}', value=f'**{max[3]}/{min[3]} \n{conditions[3]}**')
                    embed.add_field(
                        name=f'{day[4]}', value=f'** {max[4]}/{min[4]} \n{conditions[4]}**')
                    embed.add_field(
                        name=f'{day[5]}', value=f'** {max[5]}/{min[5]} \n{conditions[5]}**')
                    embed.add_field(
                        name=f'{day[6]}', value=f'** {max[6]}/{min[6]} \n{conditions[6]}**')

                    embed.set_footer(
                        icon_url=icon_url,
                        text=f'Currently {round(weather["current"]["temp"])}° Feels like {round(weather["current"]["feels_like"])}°')
                await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(weather(bot))
