import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions
import sqlite3
import asyncio
from discord.user import ClientUser
import launcher

client = discord.Client(case_insensitive=True)

class OnMessage(commands.Cog):

    # Allows to access the client within the cog
    def __init__(self, client):
        self.client = client

   

def setup(client):
    client.add_cog(OnMessage(client))
    print('topics is loaded')
