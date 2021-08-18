import json
import sqlite3


import json


# function to add to JSON
def write_json(data, filename='data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


conn = sqlite3.connect('BotDBNew.sqlite')

cur = conn.cursor()

Question = cur.execute(
    "SELECT questionId, answerOption1,answerOption2, answerOption3, answerOption4, answerOption5 FROM Questions ORDER BY questionId ASC")

list = Question.fetchall()

with open('data.json') as json_file:
    data = json.load(json_file)
    data['intents']=[]
    
    

    for row in list:
        questionId = row[0]
        option1 = row[1]
        option2 = row[2]
        option3 = row[3]
        option4 = row[4]
        option5 = row[5]

        temp = data['intents']
        
        

        # python object to be appended
        y = {"tag": str(questionId),
             "patterns": [
            str(option1),
            str(option2),
            str(option3),
            str(option4),
            str(option5)
        ],
            "responses": [
            "Example"
        ]
        }

        # appending data to emp_details
        temp.append(y)

write_json(data)
