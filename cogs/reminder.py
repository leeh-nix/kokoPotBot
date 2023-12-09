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


# async def createReminder(uId, channelId, remindTime, text):
#     newReminder = {
#         "userId": uId,
#         "channelId": channelId,
#         "remindTime": remindTime,
#         "text": text,
#     }
#     reminderCollection.insert_one(newReminder)

# class Reminder(commands.Cog):
#     def __init__(self, bot) -> None:
#         self.bot = bot
#         self.checkReminders.start()
#     @commands.command(aliases=["remind"])
#     async def timer(self, ctx, *, message: str):
#         """Sets a reminder for the specified time.
#         Usage: k! timer <Remind Time> <Reminder Text>
#         eg. k!timer 1d 2h 3m 4s to touch grass
#         """
#         print("=================================================")
#         print(message, type(message))
#         givenMessage = "".join(message)

#         reminderDetails = extractReminderDetails(givenMessage)
#         # logging.info(
#         print(
#             f"givenTime: {reminderDetails['givenTime']} remindTime: {reminderDetails['remindTime']} string: {reminderDetails['text']}"
#         )
#         givenTime = reminderDetails["givenTime"]
#         # print(reminderDetails["givenTime"])
#         # print(reminderDetails["remindTime"])
#         # print(reminderDetails["text"])
#         remindTime = int(reminderDetails["remindTime"])
#         text = reminderDetails["text"]
#         uId = ctx.author.id
#         channelId = ctx.channel.id
#         try:
#             if givenTime == 0:
#                 await ctx.send(
#                     "Please enter a valid time or use k!help remind for help on this command."
#                 )
#             else:
#                 await createReminder(uId, channelId, remindTime, text)
#                 # await ctx.channel.send("Reminder added successfully")
#                 await ctx.send(
#                     f"Reminder set for <t:{remindTime}:f>. I will notify you in <t:{remindTime}:R>."
#                 )
#         except Exception as e:
#             # logging.error(f"An error occurred: {e}")
#             await ctx.send(
#                 "An error occurred while setting the reminder. Please try again later."
#             )
#         print(f"{reminderCollection.count_documents({})} done!")


#     @commands.command(hidden=True)
#     @is_in_guild(607520631944118292)
#     async def delReminders(self, ctx):
#         """Deletes all reminder with remindTime less than current time."""
#         currentTime = datetime.datetime.now().timestamp() // 1
#         try:
#             reminderCollection.delete_many({"remindTime": {"$lt": currentTime}})
#             await ctx.send("Deleted all completed reminders")
#             await ctx.send("Reminders Count: ", reminderCollection.count_documents({}))
#         except Exception as e:
#             # logging.error(e)
#             print(e)
#     async def deleteCompletedReminder(remindTime):
#         """Deletes all reminder with remindTime less than current time."""
#         currentTime = datetime.datetime.now().timestamp() // 1
#         try:
#             reminderCollection.delete_one({"remindTime": {"$lt": currentTime}})
#             print("Reminders Count: ", reminderCollection.count_documents({}))
#         except Exception as e:
#             # logging.error(e)
#             print(e)

# #FIXME: change the time to 5 secs from 1 secs
#     @tasks.loop(seconds=5)
#     async def checkReminders(self):
#         await self.bot.wait_until_ready()
#         print("Checked reminders.")
#         currentTime = datetime.datetime.now().timestamp() // 1

#         # Get reminders from the database collection that match the current time
#         reminders = reminderCollection.find({"remindTime": {"$lte": currentTime}})

#         for reminder in reminders:
#             remindTime = reminder["remindTime"]
#             text = reminder["text"]
#             userId = reminder["userId"]
#             channel = reminder["channelId"]

#             if remindTime == currentTime:
#                 await self.bot.get_channel(channel).send(
#                     f"<@{userId}>, here's your reminder: {text}")
#                 reminderCollection.delete_one({"userID": userId})
# # add a finish property to the reminder collection to check if the reminder has been completed
# # if the reminder has been completed, delete it
# # if remindTime > currentTime:
#         #     reminderCollection.delete_one({"userID": userId})
#         # else:
#         #     reminderCollection.delete_one({"userID": userId})
#             # elif remindTime < currentTime:
#         # Remove the reminder from the collection after processing
#         # print("Checked reminders.")
