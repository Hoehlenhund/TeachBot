import discord
from discord import message, ActivityType
from discord.ext import commands
from discord.ext.commands import Cog
from discord.utils import get
from discord import utils

# extension, wo bot die rollen im willkommenschannel vergibt

# damit bot nicht nur auf text reagiert, sondern auch auf reation
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix = '$', intents=intents)

#intents = discord.Intents.all()
#client = discord.Client(intents=intents)

class reaction_cog(commands.Cog):
    # Allows to access the client within the cog
    def __init__(self, client):
        self.client = client 

    #@client.event  
    # Wenn User auf vorgegebene Rolle klickt, kriegt er die Rolle zugewiesen -> Funktioniert!
    # Dies geschieht nur auf der Nachricht im welcome-channel mit der in Z. 26 angegebenen Message ID  
    @commands.Cog.listener() # cog listener hört zu, was in verschiedenen kanälen passiert
    async def on_raw_reaction_add(self,payload): # nimmt wahr, dass man reaktion hinzufügt
        message_id = payload.message_id
        if message_id == 0123456789: # nur willkommenskanal auf nachricht, wo man anklicken kann
            guild = self.client.get_guild(payload.guild_id)
            print(guild)
            role = discord.utils.get(guild.roles, name=str(payload.emoji.name))
            print(role)   
            if role != None:
                member = payload.member 
                print(member) 
                if member != None:
                    await member.add_roles(role)  

    # wenn raktion auf die message passiert ist, prüft er, welche rolle er vergeben soll, indem er schaut, welcher emoji gedrückt wurde
    # emojis im discord müssen genau so benannt sein, wie die rolle

    #@client.event
    #Wenn User die Reaktion zurücknimmt, wird die Rolle wieder abgenommen -> Funktioniert nicht... 
    # user ist nicht integriert - 
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
    #async def on_reaction_remove(self, payload):            
        message_id = payload.message_id

        if message_id == 0123456789:
            guild = self.client.get_guild(payload.guild_id)
            
            #funktionieren nicht
            #user = payload.member
            #user = utils.get(payload.guild.members, id=payload.user_id)
            #user = get(guild.members, id=payload.user_id)
            #user = guild.get_member(payload.user_id)
            #user = await guild.fetch_member(payload.member_id)
            #user = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)

            #Freddies funktioniert mit none
            user = guild.get_member(payload.user_id)
            role = discord.utils.get(guild.roles, name=str(payload.emoji.name))
            print(role)
            print(user)
            if user != None:
                user = payload.member 
                print(user) 
                if user != None:
                    await user.remove_roles(role)

def setup(client):
    client.add_cog(reaction_cog(client))
    print('reaction cog is loaded')
    #print(discord.__version__) 

#client.run("")
