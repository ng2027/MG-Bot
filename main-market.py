import discord, asyncio
from discord.ext import commands
import requests
import os, time
from dhooks import Embed
intents = discord.Intents(messages=True, guilds=True)
intents.members = True
intents.reactions = True
intents.presences = True


client = commands.Bot(command_prefix="!", description = "I'm here to help.", intents=intents)

#when bot goes online...

@client.event
async def on_ready():
    print("Bot is ready.")
    
#current btc price
@client.command(
    pass_context = True,
    description = f'This command returns the current price of a coin. To use type: !coin btc'
    )
@commands.cooldown(5, 3600, commands.BucketType.user)
async def coin(ctx, coin):
    try:
        response = requests.get(f"https://api.coinbase.com/v2/prices/{coin.upper()}-USD/spot")
        data = response.json()
        currency = data["data"]["base"]
        price = data["data"]["amount"]
        embed = Embed(color = 16711680)
        embed.add_field(name="Price", value=f"{coin.upper()} price: {price}$")
        await ctx.send(embed=embed)
    except Exception as error101:
        print(error101)
        await ctx.send('There has been as error using the !coin command')

#loads a cog py file
@client.command()
@commands.has_permissions(administrator = True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.message.add_reaction('✅')

#unloads a cog py file
@client.command()
@commands.has_permissions(administrator = True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.message.add_reaction('✅')
    
#access all the cog files
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run("TOKEN") #add token


