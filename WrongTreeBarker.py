import overpy
from telegram import Bot
import geojson
import schedule
import time

# setup for overpass turbo query:
api = overpy.Overpass()
querystring = "[out:json];way[\"natural\"=\"tree\"];(._;>;);out center;"
oldfeatures = []

# setup for telegram bot:
api_token = "INSERT TELEGRAM API TOKEN HERE"
chat_id = "YOUR CHAT ID"
bot=Bot(token=api_token)
def send_notification(message):
    bot.send_message(chat_id=chat_id, text=message)

#helper function to parse overpass query response
def way_to_feature(way):
    coordinates = [(float(node.lon), float(node.lat)) for node in way.nodes]
    return geojson.Feature(
        id=way.id,
        geometry=geojson.LineString(coordinates),
        properties=way.tags
    )

def runbot(): #this function gets called periodically to run the query and send the resulting telegram message
    global oldfeatures
    queryresponse = api.query(querystring)
    features=[]
    for way in queryresponse.ways:
        features.append(way_to_feature(way))
    if not features:
        print(str(time.ctime(time.time()))+": Everything is fine, there are no wrong trees.")
        oldfeatures=features
    elif features != oldfeatures:
        print(str(time.ctime(time.time()))+": There were wrong trees: "+str(features))
        notificationmessage="🚨🚨🚨!!!ALARM!!! 🚨🚨🚨 \nSomeone mapped a tree 🌳🌲🌴 incorrectly!!!"
        send_notification(notificationmessage)
        for feature in features:
            bot.send_location(chat_id=chat_id, longitude=feature["geometry"]["coordinates"][0][0], latitude=feature["geometry"]["coordinates"][0][1])
        oldfeatures=features
    else:
        print(str(time.ctime(time.time()))+": Nothing has changed about the features.")


print("Starting...")
schedule.every(15).minutes.do(runbot) #starts a query every 15min


while True:
    schedule.run_pending()
    time.sleep(1)