import disnake
from disnake.ext import commands


class Help(commands.MinimalHelpCommand):

    @commands.cooldown(2, 5, commands.BucketType.user)
    async def send_command_help(self, command):
        embed = disnake.Embed(title=self.get_command_signature(command))
        embed.add_field(name="Help", value=command.help)
        aliases = command.aliases
        if aliases:
            embed.add_field(name='Aliases', value=", ".join(
                aliases), inline=False)
        channel = self.get_destination()
        await channel.send(embed=embed)


class HelpCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        help_command = Help()
        help_command.cog = self
        bot.help_command = help_command


def setup(bot):
    bot.add_cog(HelpCog(bot))
