from disnake.enums import TextInputStyle
import disnake
from weather.db import Database as db
from user.user import User
from disnake.ext import commands
from disnake.interactions.application_command import \
    ApplicationCommandInteraction
from sqlalchemy import select

import weather


class MyModal(disnake.ui.Modal):
    def __init__(self):
        self.session = db.create_session()
        # The details of the modal, and its components
        components = [
            disnake.ui.TextInput(
                label="City/Zipcode",
                placeholder="Orlando or 44060",
                custom_id="user_location",
                style=TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Country Code",
                placeholder="US",
                custom_id="country_code",
                style=TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Units",
                placeholder="imperial or metric",
                custom_id="units",
                style=TextInputStyle.short,
                max_length=50,
            )
        ]
        super().__init__(
            title="Set Location",
            custom_id="create_weather_info",
            components=components,
        )

    # The callback received when the user input is completed.
    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(title="Location")
        for key, value in inter.text_values.items():
            user_id = inter.author.id
            user_location = inter.text_values['user_location']
            country_code = inter.text_values['country_code']
            units = inter.text_values['units']
            async with self.session as session:
                result = await session.execute(select(User.weather_location).where(
                    User.id == user_id))
            await session.commit()
            await db.create_user(user_id, user_location,
                                 country_code, units)
            await inter.response.send_message(
                f"Prefered location set to {user_location} {country_code} with {units}")
        # if result is None:
        #    await db.create_user(user_id, user_location,
        #                         country_code, units)
        #    await inter.response.send_message(
        #        f"Prefered location set to {user_location} {country_code} with {units}")
        # elif result is not None:
        #    await db.update_user(self, user_id, user_location,
        #                         country_code, units)
        # await inter.response.send_message(f"Location set to {user_location} {country_code} with {units}!")


class general(commands.Cog, name="general"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command(name='onboard', help='Onboarding script')
    async def onboard(self, interaction: ApplicationCommandInteraction):

        user = interaction.author
        await interaction.response.send_modal(modal=MyModal())

    @commands.slash_command(name='ping', description='Responds with pong')
    async def ping(self, interaction: ApplicationCommandInteraction):

        embed = disnake.Embed(
        )

        embed.add_field(
            name="Pong!",
            value=":ping_pong:",
            inline=True
        )
        embed.add_field(
            name='latency', value=f'{round(interaction.bot.latency * 1000)}ms')
        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(general(bot))
