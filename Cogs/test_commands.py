# hard gecodeter test

# from asyncio.windows_events import NULL
import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions
import sqlite3

from discord.ext.commands.core import check

import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

client = discord.Client()


class TestCommands(commands.Cog):
    # Allows to access the client within the cog
    def __init__(self, client):
        self.client = client

    # Events

    

    @commands.command()
    async def test(self, ctx):
        message = ctx.message
        author = message.author
        if message.author == client.user: # bot ist client.user - dann wird kommando nicht ausgeführt, weil sie von bot selbst kommt
            return # bricht an dieser stelle ab

        conn = sqlite3.connect('BotDBNew.sqlite') 

        cur = conn.cursor()

        await author.send('Um einen Test zu starten musst du zunächste ein Thema wählen.')

        while True:
            suggestion = cur.execute(
                "SELECT topicName FROM Topics WHERE topicName = topicName")
            await author.send('Folgende Themen stehen zur Auswahl:' + str(suggestion.fetchall()))

            answer = await self.client.wait_for('message', check=lambda message: isinstance(message.content, str) and message.author != self.client.user and message.author == author)
            print(answer.content)
            try:
                print("Bin im try")
                topicId = cur.execute(
                    "SELECT topicId FROM Topics WHERE topicName=?", (f'{answer.content}',))
                result1 = str(topicId.fetchone()[0]) 
                print(result1)
                topicName = cur.execute(
                    "SELECT topicName FROM Topics WHERE topicId=?", (f'{result1}',))

                break 
            except: 
                await author.send('Dieses Kapitel steht nicht in der Liste, vielleicht hast du dich ja nur vertippt;)') 
        print(f'{topicId}') 
        print(f'{topicName}') 
        chapter=str(topicName.fetchone()[0]) 
        await author.send('Du hast dich für das Kapitel ' + chapter + ' entschieden. Ist ja deine Beerdigung lol.') 
        initialQuestion = cur.execute(
            "SELECT question, answerOption1,answerOption2, answerOption3, answerOption4, answerOption5, questionId FROM Questions WHERE topicId=(?) ORDER BY questionId", (f'{result1}',))
        questionNr = 1
        list = initialQuestion.fetchall()
        

        for row in list:
            question = row[0]
            option1 = row[1]
            option2 = row[2]
            option3 = row[3]
            option4 = row[4]
            option5 = row[5]
            Id=row[6]


            while True:
                await author.send('Frage Nummer '+str(questionNr)+': ' + str(question))
                print(option1, option2, option3, option4, option5)
                answer = await self.client.wait_for('message', check=lambda message: isinstance(message.content, str) and message.author != self.client.user and message.author == author)

                print(option5)
                answerstring = str(answer.content).lower()
                if answerstring == ".skip":
                    await author.send("Frage übersprungen.")
                    break
                else:
                    with open('data.json', 'r') as json_data:
                        intents = json.load(json_data)

                    FILE = "data.pth"
                    data = torch.load(FILE)

                    input_size = data["input_size"]
                    hidden_size = data["hidden_size"]
                    output_size = data["output_size"]
                    all_words = data['all_words']
                    tags = data['tags']
                    model_state = data["model_state"]

                    model = NeuralNet(input_size, hidden_size, output_size)
                    model.load_state_dict(model_state)
                    model.eval()

                    sentence = tokenize(answerstring)
                    X = bag_of_words(sentence, all_words)
                    X = X.reshape(1, X.shape[0])
                    X = torch.from_numpy(X)

                    output = model(X)
                    _, predicted = torch.max(output, dim=1)

                    tag = tags[predicted.item()]
                   

                    probs = torch.softmax(output, dim=1)
                    prob = probs[0][predicted.item()]
                    if prob.item() > 0.75 and tag==str(Id):
                        for intent in intents['intents']:
                            
                            if tag == intent["tag"]:
                                
                                await message.author.send(random.choice(intent['responses']))
                                
                        break             
                    else:
                        await message.author.send("Your answer is not correct. You should try again.")
                        
                    
            questionNr = questionNr+1
    
        await author.send("Herzlichen Glückwunsch! Du hast alle Fragen zum Kapitel "+chapter+" abgeschlossen!") 

    @commands.command()
    async def chat(self,ctx):
        message = ctx.message
        author = message.author
        if author == client.user: # bot ist client.user - dann wird kommando nicht ausgeführt, weil sie von bot selbst kommt
            return # bricht an dieser stelle ab
        await author.send('Hi, möchtest dich also unterhalten?')
        while True:
            answer = await self.client.wait_for('message', check=lambda message: isinstance(message.content, str) and message.author != self.client.user and message.author == author)
            answerstring = str(answer.content).lower()
            if answerstring == ".ciao":
                    await author.send("Wir reden später weiter.")
                    break
            else:
                with open('intents.json', 'r') as json_data:
                    intents = json.load(json_data)

                FILE = "dataintents.pth"
                data = torch.load(FILE)

                input_size = data["input_size"]
                hidden_size = data["hidden_size"]
                output_size = data["output_size"]
                all_words = data['all_words']
                tags = data['tags']
                model_state = data["model_state"]

                model = NeuralNet(input_size, hidden_size, output_size)
                model.load_state_dict(model_state)
                model.eval()

                sentence = tokenize(answerstring)
                X = bag_of_words(sentence, all_words)
                X = X.reshape(1, X.shape[0])
                X = torch.from_numpy(X)

                output = model(X)
                _, predicted = torch.max(output, dim=1)

                tag = tags[predicted.item()]
               

                probs = torch.softmax(output, dim=1)
                prob = probs[0][predicted.item()]
                if prob.item() > 0.75 :
                    for intent in intents['intents']:
                        
                        if tag == intent["tag"]:
                            print("I'm here 2")
                            await message.author.send(random.choice(intent['responses']))
                            
                                 
                else:
                    await message.author.send("Sorry, das habe ich leider nicht verstanden.")

    
def setup(client):
    client.add_cog(TestCommands(client))
    print('testCommands is loaded')
