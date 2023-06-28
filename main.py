import datetime
import discord
from discord.ext import commands
from discord.ext.commands import check
import dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from extractReminderDetails import extractReminderDetails
import logging

# from checkReminders import checkReminders
import asyncio
import tracemalloc


tracemalloc.start()
dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
URI = os.getenv("URI")


intents = discord.Intents.default()
intents.message_content = True
command_prefix = "k!"
guild_id = 607520631944118292
guild = 607520631944118292

owners = [418364415856082954, 413155474800902154]

activity = discord.Activity(
    name="with your emotions 😘", type=discord.ActivityType.playing
)

bot = commands.Bot(
    command_prefix=command_prefix,
    owners_ids=set(owners),
    activity=activity,
    intents=intents,
)

# Create a new client and connect to the server
client = MongoClient(URI, server_api=ServerApi("1"))
# Send a ping to confirm a successful connection
# @bot.command()
# async def dbconnect(ctx):
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.get_database("kokospotbot_db")
reminderCollection = db.reminder  # collection: reminder


# Confirmation on bot login
@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    await startReminderLoop()

    try:
        # synced = await bot.tree.sync()
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        # synced = await bot.tree.sync(guild=discord.Object(...))
        # synced = await Bot.copy_global_to(*, 607520631944118292)
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@bot.command(hidden=True)
async def delReminders(ctx):
    """Deletes all remidner with remindTime less than current time."""
    currentTime = datetime.datetime.now().timestamp() // 1
    try:
        reminderCollection.delete_many({"remindTime": {"$lt": currentTime}})
        await ctx.send("Deleted all completed reminders")
        await ctx.send("Reminders Count: ", reminderCollection.count_documents({}))
    except Exception as e:
        logging.error(e)


async def checkReminders():
    print("Checked reminders.")
    while True:
        currentTime = datetime.datetime.now().timestamp() // 1

        # Get reminders from the database collection that match the current time
        reminders = reminderCollection.find({"remindTime": {"$lte": currentTime}})

        for reminder in reminders:
            remindTime = reminder["remindTime"]
            text = reminder["text"]
            userId = reminder["userId"]
            channel = reminder["channelId"]

            # Do something with the reminder, e.g., send a message to the member
            if remindTime == currentTime:
                await bot.get_channel(channel).send(
                    f"<@{userId}>, here's your reminder: {text}"
                )
                reminderCollection.delete_one({"userID": userId})

            # elif remindTime < currentTime:

        # Remove the reminder from the collection after processing

        # print("Checked reminders.")

        # Wait for a specific remindTime before checking again (e.g., 1 second)
        await asyncio.sleep(1)



# @bot.command()
# async def remindPing(ctx):
#     await ctx
async def startReminderLoop():
    while True:
        await checkReminders()


@bot.command()
@commands.is_owner()
async def startRemindLoop(ctx):
    # loop = asyncio.get_running_loop()
    # loop.create_task(startReminderLoop())
    # await bot.get_channel.send("Reminder loop started")
    await startReminderLoop()
    await ctx.send("Reminder loop started")
    print("startReminderLoop")


@startRemindLoop.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Error starting reminder loop")


@bot.command()
@commands.is_owner()
async def test(ctx, *, message):
    print(ctx)
    print(message)
    await ctx.send(message)


@bot.command()
async def disconnect(ctx, member: discord.Member, *, message):
    text = "".join(message)
    # Check if the command is invoked in a guild
    if ctx.guild is None:
        await ctx.send("This command can only be used in a guild.")
        return

    # Check if the member is connected to a voice channel
    if member.voice is None or member.voice.channel is None:
        await ctx.send("Member is not connected to any voice channel.")
        return

    # Disconnect the member from the voice channel
    await member.voice.channel.disconnect()
    await ctx.send("Niklo\nKal ana")


# @bot.command()
# async def join(ctx, channel: discord.VoiceChannel):
#     if ctx.voice_client is None:
#         await ctx.author.move_to(channel)


# @bot.commands.command()
# async def sync() -> None:
# try:
# synced = await bot.tree.sync()
# print(f"Sync succesful: {len(synced)} commands were synced")
# await success_msg.delete(delay=5)
# except Exception as e:
#     print(e)


# Checking guild permissions
def is_in_guild(guild_id):
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.id == guild_id

    return check(predicate)


# Commands start from here

# TODO: check bot.load_extension() and reload_extension()
# TODO: check .uptime or some method for calculating the uptime of the bot

# @bot.command()
# async def loadextension(ctx):
#     await ctx.send("Loading utils extension")
#     print("Loading utils extension")
#     await bot.load_extension('utils')


# @bot.hybrid_command()
# @commands.guild_only()
# @is_in_guild(607520631944118292)
# async def evalu(ctx, *args):
#     args = list(args)
#     expr = ' '.join(str(i)for i in args[1:-1])
#     try:
#         print("cmd: ", expr)
#         result = eval(expr)
#         if asyncio.iscoroutine(result):
#             result = await result
#         await ctx.send(f"result: {result}")
#     except Exception as e:
#         print(e)
#         await ctx.send(f"An error occurred: {e}")


# @bot.add_command(command=command)


# help
@bot.command()
async def helpme(ctx):
    await ctx.channel.send(
        """```
k!ping || Pings the bot
k!send <Channel/Channel ID> <Message you want to send> || Sends the message provided to the specified channel.
k!time || Returns the current time
k!remind <Duration in minutes> <Time unit> <Reminder text> || Sets a reminder for the specified time```"""
    )


# Slash command to check info of a user
@bot.hybrid_group(fallback="enter")
# @bot.hybrid_command()
async def tag(message, member: discord.Member):
    """
    Displays the info of the user: the joining date and their current avatar

    Usage: /tag enter <@user>
    """
    await message.send(
        f"{member.mention} joined on {member.joined_at} {member.display_avatar}"
    )


@tag.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("I could not find that member...")


# @commands.is_owner()
@bot.hybrid_group(name="send", description="Sends a message to a specified channel.")
# @is_in_guild(607520631944118292)
async def send(ctx, channelId: int, *, message):
    """Sends a message to specified channel

    Args:
        channelId (int): specify the channel ID
        message (str): Message you want to send
    """
    channel = bot.get_channel(channelId)
    if channel:
        await channel.send(message)
        await ctx.send("Message sent successfully.")
    else:
        await ctx.send("Invalid channel ID.")


@send.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Please enter the correct channel...")


# @bot.command()
# async def emoji(message, *lst):
#     lst = list(lst)
#     await message.channel.send(emojify(lst))


# current time
@bot.command()
async def time(ctx):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await ctx.send(f"The current time is: {current_time}")


# reminder command
async def createReminder(user, channelId, remindTime, text):
    newReminder = {
        "userId": user,
        "channelId": channelId,
        "remindTime": remindTime,
        "text": text,
    }
    reminderCollection.insert_one(newReminder)


@bot.command()
async def timer(ctx, *, message: str):
    """Sets a reminder for the specified time.

    Usage: m! remind <remindTime> <Reminder text>
    eg. m!remind 1d 2h 3m 4s to touch grass
    """
    print("=================================================")
    print(message, type(message))
    givenMessage = "".join(message)

    reminderDetails = extractReminderDetails(givenMessage)
    logging.info(
        f"givenTime: {reminderDetails['givenTime']} remindTime: {reminderDetails['remindTime']} string: {reminderDetails['text']}"
    )
    givenTime = reminderDetails["givenTime"]
    print(reminderDetails["givenTime"])
    print(reminderDetails["remindTime"])
    print(reminderDetails["text"])
    remindTime = int(reminderDetails["remindTime"])
    text = reminderDetails["text"]
    user = ctx.author.id
    channelId = ctx.channel.id
    if givenTime == 0:
        await ctx.send(
            "Please enter a valid time or use k!help remind for help on this command."
        )
    else:
        await createReminder(user, channelId, remindTime, text)
        await ctx.channel.send("Reminder added successfully")
        await ctx.send(
            f"Reminder set for <t:{remindTime}:f>. I will notify you in <t:{remindTime}:R>."
        )
    print(f"{reminderCollection.count_documents({})} done!")


@bot.command()
async def hello(message):
    await message.channel.send("Hello!")


@bot.hybrid_command()
async def ping(message):
    await message.send(f"Let's go Baby! ```{bot.latency * 1000} ms```")


@bot.command()
async def pat(message):
    await message.channel.send("Aww thank you cutie i really need that sometimes <3")


@bot.command(aliases=["tq", "thankq", "ty"])
async def thanks(message):
    await message.channel.send("Always there for you <3")


# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

#     if message.content.startswith('hello'):
#         await message.channel.send("Hellooo  how are you")

# ============================================================================================================================
try:
    bot.run(TOKEN)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
    else:
        raise e
