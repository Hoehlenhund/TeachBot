#discord
import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions
from discord.ext.commands.core import check
from discord import channel

#deep learning
import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

#the rest
import sqlite3
from discord.user import ClientUser
import launcher
import asyncio

client = discord.Client(case_insensitive=True)
prefix = commands.Bot(command_prefix='.')



class OnMessage(commands.Cog): 
   

    # Allows to access the client within the cog
    def __init__(self, client):
        self.client = client
    

    @commands.command
    async def on_message(self, message):
        pass

    client.quiz=False
    @commands.Cog.listener()
    async def on_message(self, message):
       
    
        print(message.content)
        input = message.content
        author = message.author

        # datenbank öffnen
        conn = sqlite3.connect('BotDBNew.sqlite')
        cur = conn.cursor()

        # wenn nachricht vom bot selbst ist, ignorieren
        if message.author == client.user:
            return

        #-------------- Hard Coded ------------------

        # wie werden sachen in die db gespeichert und ausgelesen
        elif message.content.startswith('!teachbot'):
            courses = cur.execute("SELECT studyCourse FROM Userdata")
            await message.author.send('Hallo, freut mich sehr! Ich hätte noch ein paar Fragen, um dich genauer einschätzen zu können. Welcher Vorlesung besuchst du? '
                                'Du hast folgende zur Auswahl, bitte Antworte mit !Beispiel: ' + str(courses.fetchall()))


        # sqlite befehle um in datenbank zu speichern
        # anfangs alle daten abfragen
        elif message.content.startswith('Webgrundlagen'):
            print(launcher.member_number)
            cur.execute("UPDATE Userdata SET studyCourse = 'Webgrundlagen' WHERE userId = ?", [f'{launcher.member_number}'])
            conn.commit()
            await message.author.send('Du bist erfolgreich den Fragen zum Fach Webgrundlagen beigetreten! Noch eine kurze Frage: In welchem Semester bist du?')
 
        # Was ist, wenn mehrere Kurse besucht werden? ToDo: Allgemein halten statt hard coded
        elif message.content.startswith('Was anderes'):
            cur.execute("UPDATE Userdata SET studyCourse = 'Was anderes' WHERE userId = ?", [f'{launcher.member_number}'])
            conn.commit()
            await message.author.send('Du bist erfolgreich den Fragen zum Fach Was anderes beigetreten! Noch eine kurze Frage: In welchem Semester bist du? (1-99)')


        conn.commit()
        conn.close()


def setup(client):
    client.add_cog(OnMessage(client))
    print('on_message is loaded')
