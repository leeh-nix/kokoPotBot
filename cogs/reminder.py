from discord.ext import commands, tasks
import datetime
import asyncio
import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import dotenv
from functions.extractReminderDetails import extractReminderDetails
from functions.checks import is_in_guild

dotenv.load_dotenv()
URI = os.getenv("URI")
# Create a new client and connect to the server
client = MongoClient(URI, server_api=ServerApi("1"))
# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.get_database("kokospotbot_db")
reminderCollection = db.reminder  # collection: reminder


async def createReminder(userId, channelId, messageId, remindTime, text, messageLink):
    """
    Create a reminder and insert it into the reminder collection.

    Parameters:
        userId (str): The ID of the user.
        channelId (str): The ID of the channel.
        messageId (str): The ID of the message.
        remindTime (datetime): The time to set the reminder.
        text (str): The reminder text.

    Returns:
        None
    """
    newReminder = {
        "userId": userId,
        "channelId": channelId,
        "messageId": messageId,
        "remindTime": remindTime,
        "text": text,
        "messageLink": messageLink,
    }
    reminderCollection.insert_one(newReminder)
