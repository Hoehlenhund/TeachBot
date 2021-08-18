import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions
import sqlite3

# was ausgeführt wird, wenn der bot startet

client = discord.Client()

class OnReady(commands.Cog):
    # Allows to access the client within the cog
    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')


def setup(client):
    client.add_cog(OnReady(client))
    print('on_ready is loaded')
