import discord
from discord.ext import commands
import datetime
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions
import sqlite3
from discord import guild
from Cogs import on_message
import launcher


class OnServerJoin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):

    # Add to database
        print(f"This is the member id {member.id}")
        # datebank wird eröffnet
        conn = sqlite3.connect('BotDBNew.sqlite')
        cur = conn.cursor()

        # wenn member id vom user noch nicht existiert, in db speichern
        cur.execute("INSERT INTO Userdata(userId, userName) VALUES (?, ?)", (f'{member.id}', f'{member.name}',))
        
        print(launcher.member_number)
        launcher.member_number = member.id
        # einträge commiten, damit sie in db gespeichert werden
        conn.commit()
        conn.close()

    # BEGRÜSSUNGSNACHRICHT KÄSTCHEN

    # Layout of the join message by https://leovoel.github.io/embed-visualizer/
        embed = discord.Embed(colour=0x95efcc, description=f"Herzlich willkommen! Du bist das {len(list(member.guild.members))} Mitglied! Um Fragen zu stellen schreibe mir .chat. Um in den Test Dialog zu kommen .test.")

        embed.set_thumbnail(url=f"{member.avatar_url}")

    # members profil picture
        embed.set_author(name=f"{member.name}", url=f"{member.avatar_url}", icon_url=f"{member.avatar_url}")

    # Server picture
        embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")

    # Time of joining and puts into footer
        embed.timestamp = datetime.datetime.utcnow()

        channel = self.client.get_channel(id=0123456789)

        await member.send(embed=embed)

# standard (macht cog als cog verfügbar für launcher)
def setup(client):
    client.add_cog(OnServerJoin(client))
    print('on_member_join is loaded')
