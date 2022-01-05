import disnake
from disnake.ext import commands
from disnake.interactions.application_command import \
    ApplicationCommandInteraction


class general(commands.Cog, name="general"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command(name='onboard', help='Onboarding script')
    async def onboard(self, interaction: ApplicationCommandInteraction):

        user = interaction.author
        await interaction.send('Hello!')

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
