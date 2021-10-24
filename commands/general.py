import disnake
from dislash import InteractionClient
from disnake.ext import commands
from disnake.interactions.application_command import \
    ApplicationCommandInteraction

intents = disnake.Intents.all()
intents.members = True
client = disnake.Client()
inter_client = InteractionClient(
    commands.Bot, test_guilds=[831327284479918121, 663770377906028545, 632665484692684821])


class general(commands.Cog, name="general"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='onboard', help='Onboarding script')
    async def onboard(self, context):

        user = context.author
        await user.send('Hello!')

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

    @commands.slash_command(name="server")
    async def servers(self, interaction: ApplicationCommandInteraction):
        activeservers = client.guilds
        for guild in activeservers:
            await interaction.response.send_message(guild.name)


def setup(bot):
    bot.add_cog(general(bot))
