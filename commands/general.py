import discord
from discord.ext import commands
from discord.ext.commands import bot

class general(commands.Cog, name="general"):
    def __init__(self,bot) -> None:
        self.bot = bot
        
    @commands.command(name='ping', help='Responds with pong')
    async def ping(self, context):
        
        embed = discord.Embed(
        )
        
        embed.add_field(
            name = "Pong!",
            value = ":ping_pong",
            inline = True
        )
        
        embed.set_footer(
            text=f'Pong request by {context.message.author}, latency is {round(1000 * bot.latency)}ms")'
        )
        await context.send(embed=embed)

def setup(bot):
    bot.add_cog(general(bot))        
