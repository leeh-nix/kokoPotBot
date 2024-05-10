from discord.ext import commands
from discord import Color, Embed
from random import randint
import datetime
import re
from typing import Optional
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


async def createReminder(
    reminderId, userId, channelId, messageId, remindTime, text, messageLink
):
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
        "reminderId": reminderId,
        "userId": userId,
        "channelId": channelId,
        "messageId": messageId,
        "remindTime": remindTime,
        "text": text,
        "messageLink": messageLink,
    }
    reminderCollection.insert_one(newReminder)


class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def reminder(
        self,
        ctx,
        days: Optional[int] = 0,
        hours: Optional[int] = 0,
        minutes: Optional[int] = 0,
        seconds: int = 0,
        message: str = "you didn't provide any message",
    ):
        """Sets a reminder for the specified time."""
        print("Reminder called")
        print(message, type(message))
        # Time
        days = int(days)
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)

        currentTime = datetime.datetime.now().timestamp() // 1  # float
        givenTime = (days * 86400) + (hours * 3600) + (minutes * 60) + seconds  # int
        remindTime = int(currentTime) + int(givenTime)  # int
        user = ctx.author
        print(f"givenTime: {givenTime}, remindTime: {remindTime} string: {message}")
        text = message
        userId = user.id
        messageId = ctx.message.id
        channelId = ctx.channel.id
        messageLink = ctx.message.jump_url
        if givenTime == 0:
            description = "Please enter a valid timestamp."
            color = Color.red()
        else:
            reminderId = randint(1000, 9999)
            await createReminder(
                reminderId=reminderId,
                userId=userId,
                channelId=channelId,
                messageId=messageId,
                remindTime=remindTime,
                text=text,
                messageLink=messageLink,
            )
            description = f"Reminder set for <t:{remindTime}:f>. I will notify you in <t:{remindTime}:R>, reminder id: `#{reminderId}`."
            color = Color.green()
        embed = Embed(
            title="Reminder Added",
            description=description,
            color=color,
            timestamp=datetime.datetime.now(),
        )
        embed.set_footer(
            text="Requested by " + user.name,
            icon_url=user.display_avatar,
        )
        await ctx.send(embed=embed)

        print(f"{reminderCollection.count_documents({})} done!")

    @commands.command(hidden=True)
    async def timer(self, ctx, *, message: str):
        """Sets a reminder for the specified time.
        Usage: reminder for <Reminder Time> <Reminder Text>
        """
        print("=================================================")
        print(message, type(message))
        remove_prefix_pattern = r"(?:reminder(?: for)?)\s+(.+)"
        matched = re.search(remove_prefix_pattern, message, re.IGNORECASE)
        message = matched.group(1)
        givenMessage = message
        user = ctx.author

        reminderDetails = extractReminderDetails(givenMessage)

        print(
            f"givenTime: {reminderDetails['givenTime']} remindTime: {reminderDetails['remindTime']} string: {reminderDetails['text']}"
        )

        givenTime = reminderDetails["givenTime"]
        remindTime = int(reminderDetails["remindTime"])
        text = reminderDetails["text"]
        userId = user.id
        channelId = ctx.channel.id
        messageId = ctx.message.id
        messageLink = ctx.message.jump_url
        try:
            if givenTime == 0:
                description = "Please enter a valid time or use k!help remind for help on this command."
                color = Color.red()
            else:
                reminderId = randint(10000, 99999)
                await createReminder(
                    reminderId=reminderId,
                    userId=userId,
                    channelId=channelId,
                    messageId=messageId,
                    remindTime=remindTime,
                    text=text,
                    messageLink=messageLink,
                )
                # await ctx.channel.send("Reminder added successfully")
                description = f"Reminder set for <t:{remindTime}:f>. I will notify you in <t:{remindTime}:R>, reminder id: `#{reminderId}`."
                color = Color.green()
                embed = Embed(
                    title="Reminder Added",
                    description=description,
                    color=color,
                    timestamp=datetime.datetime.now(),
                )
                embed.set_footer(
                    text="Requested by " + user.name,
                    icon_url=user.display_avatar,
                )
                await ctx.send(embed=embed)

                print(f"{reminderCollection.count_documents({})} done!")
        except Exception as e:
            await ctx.send(
                f"An error occurred while setting the reminder. Please try again later. ||ERROR : {e}||"
            )

    @commands.hybrid_command()
    async def getreminders(self, ctx: commands.Context):
        """Gets all of the reminders for the user."""
        id = ctx.author.id
        name = ctx.author.name
        print("get reminders for: ", name)
        description = ""
        currentTime = datetime.datetime.now().timestamp() // 1
        counter = 0
        try:
            reminders = reminderCollection.find({"userId": id})
            for reminder in reminders:
                if currentTime < reminder["remindTime"]:
                    description += f'\n`#{reminder["reminderId"]}`. "<t:{reminder["remindTime"]}:f>" (<t:{reminder["remindTime"]}:R>) : {reminder["text"]}\n'
                    counter += 1

            if description == "":
                description = (
                    "...what are you looking for? theres nothing here for you."
                )

            title = name
            footer = f"Found {counter} reminders"
            embed = Embed(title=title, color=Color.magenta(), description=description)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_thumbnail(url=ctx.author.display_avatar)
            embed.set_footer(text=footer)
            await ctx.send(embed=embed, tts=False, ephemeral=True)

        except Exception as e:
            print(e)

    @commands.hybrid_command(
        name="delreminder", description="Deletes a reminder by reminderId."
    )
    async def delreminder(self, ctx: commands.Context, *, reminderid: int):
        """Deletes a reminder by reminderId."""
        try:
            found = False
            reminderId = reminderid
            userId = ctx.author.id
            reminders = reminderCollection.find({"userId": userId})

            for reminder in reminders:
                reminderUserId = reminder["userId"]

                if userId == reminderUserId:
                    if reminderId == reminder["reminderId"]:
                        reminderCollection.delete_one({"reminderId": reminderId})
                        await ctx.send(f"Deleted reminder {reminderId}")
                        found = True
                        break
                    else:
                        continue
                break
            if found == False:
                await ctx.reply(f"Deleted all of the reminders.")

        except Exception as e:
            print(e)

    # @bot.command(name="delallrem", hidden=True)
    # @is_in_guild(607520631944118292)
    # async def delReminders(self, ctx: commands.Context):
    #     """Deletes all remidner with remindTime less than current time."""
    #     currentTime = datetime.datetime.now().timestamp() // 1
    #     try:
    #         reminderCollection.delete_many({"remindTime": {"$lt": currentTime}})
    #         await bot.get_channel(955825787599216701).send(
    #             f"Deleted all completed reminders\nReminders Count: {reminderCollection.count_documents({})}"
    #         )
    #     except Exception as e:
    #         print(e)

    @commands.command(name="delallrem", hidden=True)
    @is_in_guild(607520631944118292)
    async def delReminders(self, ctx: commands.Context):
        """Deletes all remidner with remindTime less than current time."""
        currentTime = datetime.datetime.now().timestamp() // 1
        try:
            beforeDeletion = reminderCollection.count_documents({})
            reminderCollection.delete_many({"remindTime": {"$lt": currentTime}})
            afterDeletion = reminderCollection.count_documents({})
            await ctx.send(
                f"Deleted {beforeDeletion - afterDeletion} completed reminders\nReminders left: {afterDeletion}",
                ephemeral=True,
            )
        except Exception as e:
            print(e)
