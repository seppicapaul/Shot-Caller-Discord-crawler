import discord
import requests
import json
import csv
import mysql.connector


mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="seppicapaul",
    password="",
    port="3306",
    database="discord_data",
    use_unicode=True
)

mycursor = mydb.cursor()

def getChannelMessages(server, channel, channelID):
    headers = {
        'authorization': 'ODY5MzIwODE4Njk2NTQwMjMw.YP8g9w.Wuj438s4NwPgvOHSPBokgv3nZ74'
    }
    r = requests.get(f'https://discord.com/api/v9/channels/{channelID}/messages', headers=headers)
    jsonObjs = json.loads(r.text)

    author = ""
    message = ""
    messageID = ""
    dateTime = ""

    for value in jsonObjs:
        try:
            author = value['author']['username']
            message = value['content']
            messageID = value['id']
            dateTime = value['timestamp']
            print(value, '\n')
            if len(message) != 0:
                print("Server: " + server)
                print("Channel: " + channel)
                # print("Channel id: " + channel_id)
                print("Author: " + author)
                print("Message: " + message)
                print("Message id: " + messageID)
                print("Date/time: " + dateTime, '\n')
                sql = "REPLACE INTO discord_import$stream (SERVER_NAME, CHANNEL_NAME, AUTHOR, MESSAGE, MESSAGE_ID, DATETIME) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (server, channel, author, message, messageID, dateTime)
                mycursor.execute(sql, val)
                mydb.commit()
        except:
            pass


filename = open('influencers of crypto - Discord.csv')
file = csv.DictReader(filename)

guild_name = ""
channel_name = ""
channel_id = ""

for col in file:
    guild_name = col['guild_name']
    channel_name = col['channel_name']
    channel_id = col['channel_id']
    # print("Server: " + guild_name)
    # print("Channel name: " + channel_name)
    # print("Channel id: " + channel_id, '\n')
    getChannelMessages(guild_name, channel_name, channel_id)
