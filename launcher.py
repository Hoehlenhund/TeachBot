import discord
from discord.ext import commands
import os
import datetime
import sys

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix='.', intents=intents, case_insensitive=True)

global member_number
member_number = 1

print("Launcher Started")


# durchsucht alle dateinamen in dem verzeichnis cogs - wenn filename mit .py endet, wird er als extension geladen
for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'Cogs.{filename[:-3]}')

# erste discord commands, kann man mit präfix . eintragen
# @client.command ist identifier für kommando
# muss dann das ausführen, was definiert ist

@client.command()
async def load(ctx, extension):
    client.load_extension(f'./Cogs.{extension}')

# unload extension

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'./Cogs.{extension}')

# reload extensions (cogs)

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'./Cogs.{extension}')
    client.load_extension(f'./Cogs.{extension}')

#restarts the entire bot

@client.command()
async def restart(self, ctx):
    try:
        await ctx.bot.close()
    except:
        pass
    finally:
        os.system("py -3 launcher.py")

# bot token aus entwicklerdatenbank
client.run('')
