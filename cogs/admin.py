import discord, random, time, asyncio
from discord.ext import commands
from discord import Embed

total_check = 0

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client
    

  

    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = Embed(color = 16711680)
            embed.add_field(name="404", value="Please pass in all required arguments.", inline=True)
            embed.set_image(url = "https://media1.tenor.com/images/fdb0976290a4bf9defe1dba271e6a98b/tenor.gif?itemid=4117250")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandNotFound):
            if ctx.channel.type is discord.ChannelType.private:
                err0r_448nd_d = 0

    
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def kick(self, ctx, member:discord.Member, *, reason = None):
        await member.kick(reason = reason)
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def ban(self, ctx, member:discord.Member, *, reason = None):
        await member.ban(reason = reason)
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def get_id(self, ctx, *, user: discord.User):
        await ctx.author.send(str(user.id))

    
def setup(client):
    client.add_cog(Admin(client))
    
