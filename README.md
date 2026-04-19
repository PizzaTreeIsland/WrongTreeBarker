# Wrong Tree Barker
A Telegram Bot that alerts me whenever someone incorrectly maps trees as ways in openstreetmap. 

<img src="https://github.com/user-attachments/assets/a5887d08-94f2-49d5-8ec0-95aa9aa5aee4" alt="Graph showing the frequency of occurence of tree ways over time" width="600"/>




I pride myself in having completely eliminated trees that are wrongly mapped as ways (instead of nodes) on [openstreetmap](https://www.openstreetmap.org/). This, however, takes some maintanance from time to time as people expand the map continuously and therefore continue to make such mistakes. To make my life a bit easier, I made this simple script that checks for such tree ways every 15 minutes and alerts me via Telegram when a new one was found. 

<img src="https://github.com/user-attachments/assets/eff49bf6-7ff3-4410-80b0-24464899df18" alt="Screenshot of chat with WrongTreeBarker Bot" width="400"/>


I'm not suggesting anyone should do the very same thing as those tree accidents occur rarely and when they do, they take only so many people to fix. However, I publish this so you can be inspired to chose your own "pet issue" to fix and keep fixed. How about overlapping buildings in your home town or rogue orphan nodes in your region? 

# Usage
Create your own telegram bot by interacting with the [BotFather telegram account](https://t.me/BotFather). You will recieve an API Token. You can then find out your personal Telegram Chat ID, for example by sending a message to your bot and later running this python function: 

```python
from telegram import Bot

API_TOKEN = 'YOUR_BOT_API_TOKEN'

bot = Bot(token=API_TOKEN)
updates = bot.get_updates()

for update in updates:
    print(update.message.chat.id) 

```
Insert both the API Token and the Chat ID into the appropriate parts of the WrongTreeBarker.py code. 

Adjust the querytext string to query for whatever issues you want to monitor. For simple queries, the query wizard tool on [Overpass Turbo](https://overpass-turbo.eu/) is useful. For examples of more complex queries, see the [OSM Wiki page on overpass query examples](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_API_by_Example). ChatGPT is also a surprisingly good tool for writing queries of mid to high complexity. 

