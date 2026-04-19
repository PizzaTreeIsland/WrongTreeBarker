from telegram import Bot
import requests
import json
import schedule
import time
import asyncio
from telegram.request import HTTPXRequest


# setup for overpass turbo query:
url = "http://overpass-api.de/api/interpreter" #Or any other overpass server
querystring = "[out:json][timeout:60000];way[\"natural\"=\"tree\"];out center;"
oldfeatures = []
api_token = "YourApiToken"
chat_id = "YourChatID"


# setup for telegram bot:
async def send_notification(message):
    trequest = HTTPXRequest(connection_pool_size=256, pool_timeout=10.0)
    bot=Bot(token=api_token, request=trequest)
    await bot.send_message(chat_id=chat_id, text=message)


async def runbot(): 
    try:
        global oldfeatures
        queryresponse = requests.get(url, params={"data": querystring})
        if queryresponse.status_code==200:
            features=queryresponse.json()["elements"]
        else: 
            raise ValueError(queryresponse.status_code) 
        if not features:
            print(str(time.ctime(time.time()))+": Everything is fine, there are no wrong trees.")
            oldfeatures=features
        elif features != oldfeatures:
            print(str(time.ctime(time.time()))+": There were wrong trees: "+str(features))
            notificationmessage="🚨🚨🚨!!!ALARM!!! 🚨🚨🚨 \nSomeone mapped a tree 🌳🌲🌴 incorrectly!!!"
            await send_notification(notificationmessage)
            for feature in features:
                if feature["type"]=="node": #not necessary in this case but I wanted to keep it in as an example for other types (looking for nodes with wrong tags)
                    trequest = HTTPXRequest(connection_pool_size=256, pool_timeout=10.0)
                    bot=Bot(token=api_token, request=trequest)
                    await bot.send_location(chat_id=chat_id, longitude=feature["lon"], latitude=feature["lat"])
                else:
                    trequest = HTTPXRequest(connection_pool_size=256, pool_timeout=10.0)
                    bot=Bot(token=api_token, request=trequest)
                    await bot.send_location(chat_id=chat_id, longitude=feature["center"]["lon"], latitude=feature["center"]["lat"])
            oldfeatures=features
        else:
            print(str(time.ctime(time.time()))+": Nothing has changed about the features.")
    except Exception as e:
        print(str(time.ctime(time.time())) + ": An error occurred. Trying again in 15 minutes." + str(e))


print("Starting...")
schedule.every(15).minutes.do(lambda: asyncio.run(runbot())) #starts a query every 15min


while True:
    schedule.run_pending()
    time.sleep(1)
