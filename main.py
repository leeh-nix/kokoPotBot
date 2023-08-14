import datetime
import io
import discord
from discord.ext import commands
from discord.ext.commands import check
import dotenv
import os
from typing import Literal, Optional

# import typing
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from extractReminderDetails import extractReminderDetails
from image import imagetransform
from konachanImgExtractor import konachanImgExtractor
from utils import *

# import logging
# from checkReminders import checkReminders
import asyncio
import tracemalloc


tracemalloc.start()
dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
URI = os.getenv("URI")
URL_ENDPOINT = os.getenv("URL_ENDPOINT")


intents = discord.Intents.all()
intents.message_content = True
command_prefix = "k!"
guild_id = 607520631944118292
owners = [
    418364415856082954,
    757478713402064996,
    413155474800902154,
    840584597472936006,
    1132574358909493248,
]

channel_list = [
    457217966505852928,
    1048553311768420363,
    864370415076769813,
    1124341821154267196,
]

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
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.get_database("kokospotbot_db")
reminderCollection = db.reminder  # collection: reminder

# list
watchlist = []


# Confirmation on bot login
@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    await startReminderLoop()


async def is_owner(ctx):
    if ctx.author.id in owners:
        return True


@bot.command()
@commands.check(is_owner)
async def addOwner(ctx, member: discord.Member):
    """Add a member to the owners list"""
    owners.append(member.id)
    await ctx.send(f"Added {member} to the owners list")


@bot.command(hidden=True)
@commands.check(is_owner)
async def sync(
    ctx: commands.Context,
    guilds: commands.Greedy[discord.Object],
    spec: Optional[Literal["~", "*", "^"]] = None,
) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


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
@commands.check(is_owner)
async def startRemindLoop(ctx):
    await startReminderLoop()
    await ctx.send("Reminder loop started")
    print("startReminderLoop")


@startRemindLoop.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Error starting reminder loop")


@bot.command(hidden=True)
@commands.check(is_owner)
async def test(ctx, *, message):
    print(ctx)
    print(message)
    await ctx.send(message)


# Checking guild permissions
def is_in_guild(guild_id):
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.id == guild_id

    return check(predicate)


# Commands start from here


@bot.command(hidden=True)
@is_in_guild(607520631944118292)
async def delReminders(ctx):
    """Deletes all remidner with remindTime less than current time."""
    currentTime = datetime.datetime.now().timestamp() // 1
    try:
        reminderCollection.delete_many({"remindTime": {"$lt": currentTime}})
        await ctx.send("Deleted all completed reminders")
        await ctx.send("Reminders Count: ", reminderCollection.count_documents({}))
    except Exception as e:
        # logging.error(e)
        print(e)


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


@bot.hybrid_command()
@commands.check(is_owner)
async def send(ctx, channel: discord.TextChannel, message):
    """Sends a message to specified channel
    Args:
        channelId (int): specify the channel ID
        message (str): Message you want to send
    """
    channel = channel
    if channel:
        await channel.send(message)
        await ctx.send("Message sent successfully.")
    else:
        await ctx.send("Invalid channel ID.")


# @bot.command()
# async def emoji(message, *lst):
#     lst = list(lst)
#     await message.channel.send(emojify(lst))


@bot.command(hidden=True)
@commands.check(is_owner)
async def add(ctx, *, message):
    message = "".join(message)
    watchlist.append(message)
    await ctx.send(f"added: `{message}` to the watchlist")


@bot.command()
@commands.check(is_owner)
async def display(ctx):
    await ctx.send(watchlist)


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


@bot.command(aliases=["remind"])
async def timer(ctx, *, message: str):
    """Sets a reminder for the specified time.
    Usage: k! timer <Remind Time> <Reminder Text>
    eg. k!timer 1d 2h 3m 4s to touch grass
    """
    print("=================================================")
    print(message, type(message))
    givenMessage = "".join(message)

    reminderDetails = extractReminderDetails(givenMessage)
    # logging.info(
    print(
        f"givenTime: {reminderDetails['givenTime']} remindTime: {reminderDetails['remindTime']} string: {reminderDetails['text']}"
    )
    givenTime = reminderDetails["givenTime"]
    # print(reminderDetails["givenTime"])
    # print(reminderDetails["remindTime"])
    # print(reminderDetails["text"])
    remindTime = int(reminderDetails["remindTime"])
    text = reminderDetails["text"]
    user = ctx.author.id
    channelId = ctx.channel.id
    try:
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
    except Exception as e:
        # logging.error(f"An error occurred: {e}")
        await ctx.send(
            "An error occurred while setting the reminder. Please try again later."
        )
    print(f"{reminderCollection.count_documents({})} done!")


konachan_list = [1124585323196862604, 1138102688098304081]


@bot.command(hidden=True)
# @commands.check(is_owner)
# @is_in_guild(607520631944118292)
async def konachan(ctx, tags):
    """fetches 5 images from konachan (if nothing is returned then your tag doesn't has any post associated with it in the website)

    Args:
        tags (string): Enter the tag you want to search for.
    """
    if ctx.channel.id in konachan_list:
        data = konachanImgExtractor(tags)
        for imgdata in data:
            try:
                print(imgdata)
                await ctx.send(imgdata)
            except Exception as e:
                print(e)
    else:
        await ctx.send("Error: You are not in the right channel.")


@bot.command()
async def encode(ctx, *, message):
    """Encode your message in binary"""
    message = "".join(message)
    result = encoding(message)
    await ctx.send(f"The encoded message: {result}")


@bot.command()
async def decode(ctx, *, message):
    """Decode your binary message"""
    message = "".join(message)
    result = decoding(message)
    await ctx.send(f"The decoded message: {result}")


@bot.command()
async def doublestruck(ctx, *, message):
    message = "".join(message)
    result = doublestruckAPI(message)
    await ctx.send(f"{result}")


@bot.command()
async def clown(ctx, message, *args):
    # url = f"{API_BASE_URL}/clown?image={message}"
    """You're a clown

    Args:
        message (image link): Provide image link ending with (.jpg, .jpeg, .png)

    Raises:
        ValueError: _description_
    """
    if not message.startswith("http") or not message.endswith(
        (".jpg", ".jpeg", ".png", ".gif")
    ):
        await ctx.send("Please enter valid url.")
        raise ValueError("Invalid image URL")
    else:
        result = await clownApiRequest(message)
    with open("clown_image.png", "wb") as file:
        file.write(result)

    with open("clown_image.png", "rb") as file:
        await ctx.send(file=discord.File(file, "clown_image.png"))


@bot.command()
async def advertise(ctx, message):
    # url = f"{API_BASE_URL}/ad?image={message}"
    """Advertise your image

    Args:
        message (image link): Provide image link ending with (.jpg, .jpeg, .png)

    Raises:
        ValueError: Provided message doesn't contain the image link
    """
    if not message.startswith("http") or not message.endswith(
        (".jpg", ".jpeg", ".png", ".gif")
    ):
        await ctx.send("Please enter valid url.")
        raise ValueError("Invalid image URL")
    else:
        result = await adApiRequest(message)
    with open("advertise_image.png", "wb") as file:
        file.write(result)

    with open("advertise_image.png", "rb") as file:
        await ctx.send(file=discord.File(file, "advertise_image.png"))


@bot.command()
async def uncover(ctx, message):
    """Uncover the poster 

    Args:
        message (image link): Provide image link ending with (.jpg, .jpeg, .png)

    Raises:
        ValueError: _description_
    """
    # url = f"{API_BASE_URL}/uncover?image={message}"
    if not message.startswith("http") or not message.endswith(
        (".jpg", ".jpeg", ".png", ".gif")
    ):
        await ctx.send("Please enter valid url.")
        raise ValueError("Invalid image URL")
    else:
        result = await uncoverApiRequest(message)
    with open("uncover_image.png", "wb") as file:
        file.write(result)

    with open("uncover_image.png", "rb") as file:
        await ctx.send(file=discord.File(file, "uncover_image.png"))


@bot.command()
async def jail(ctx, message):
    """Sends the image with adding a layer of jail bars

    Args:
        message (image link): provide image link with ending image extension (.png, .jpg, jpeg etc)

    Raises:
        ValueError: provided message doesn't contain the image link
    """
    # url = f"{API_BASE_URL}/jail?image={message}"
    # TODO: use regex to trim the link provided and add the image extension
    if not message.startswith("http") or not message.endswith(
        (".jpg", ".jpeg", ".png", ".gif")
    ):
        await ctx.send("Please enter valid url.")
        raise ValueError("Invalid image URL")
    else:
        result = await jailApiRequest(message)
    with open("jail_image.png", "wb") as file:
        file.write(result)

    with open("jail_image.png", "rb") as file:
        await ctx.send(file=discord.File(file, "jail_image.png"))


@bot.hybrid_command()
async def imageresize(
    ctx,
    message,
    format: Literal["gif", "png, jpeg, jpg etc"],
    height: Optional[int] = None,
    width: Optional[int] = None,
    aspect_ratio: Optional[Literal["1-1", "4-3", "3-4"]] = None,
):
    """Resizes the image provided in the message box, the link must be ending with png, jpeg, jpg , gif etc

    Args:
        ctx (_type_): _description_
        message (_type_): Enter the link of your image
        format (Literal[&quot;gif&quot;, &quot;png, jpeg, jpg etc&quot;]): png, jpeg, jpg, gif etc
        height (Optional[int], optional): provide height
        width (Optional[int], optional): provide width
        aspect_ratio (Optional[str], optional): Enter the aspect ratio (eg. 4-3 for 4:3)
    """
    if (height is None and width is None and aspect_ratio is None) or (
        (height is None or width is None) and aspect_ratio is not None
    ):
        return await ctx.send("Please enter at least two values to resize your image.")
    else:
        result = imagetransform(message, height, width, aspect_ratio)
    with io.BytesIO(result) as image_file:
        image_file.seek(0)
        if format == "gif":
            await ctx.send(file=discord.File(image_file, "image.gif"))
        else:
            await ctx.send(file=discord.File(image_file, "image.png"))


@bot.command(hidden=True)
@commands.check(is_owner)
async def purge(ctx, amount: int):
    """Deletes the message of the channel or the member if specified and the amount specified amount

    Args:
        amount (int): specify the number of message you want to delete
    """
    try: 
        deleted = await ctx.channel.purge(limit=amount)
    except Exception as e:
        await ctx.send(e)
    finally: await ctx.channel.send(f"Deleted {len(deleted)} message(s)", delete_after=3)

@bot.command(hidden=True, aliases=["del"])
@commands.check(is_owner)
async def delete(ctx, amount: int, member: Optional[discord.Member] = None):
    """Deletes the message of the channel or the member if specified and the amount specified amount

    Args:
        amount (int): specify the number of message you want to delete
        member (Optional[discord.Member], optional):  specify the member (Optional).
    """

    def is_member_message(message):
        return message.author == member

    deleted = 0
    try:
        async for message in ctx.channel.history(limit=None):
            if is_member_message(message):
                await message.delete()
                deleted += 1
                if deleted >= amount:
                    break
    except Exception as e:
        # print(e)
        await ctx.send(e, delete_after=3)
    finally:
        await ctx.channel.send(f"Deleted {deleted} message(s)", delete_after=3)

@bot.hybrid_command()
async def embed(
    ctx,
    content,
    title,
    description,
    color: discord.Colour,
    footer: Optional[str] = None,
    embed_url: Optional[str] = None,
):
    embed = discord.Embed(
        title=title, description=description, color=color, url=embed_url
    )
    embed.set_footer(text=footer)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(content, embed=embed, tts=False)

@bot.command()
async def hello(message):
    await message.channel.send("Hello!")


@bot.hybrid_command()
async def ping(message):
    await message.send(f"Let's go Baby! ```{(bot.latency * 1000)//1} ms```")


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

burrman = 758978243842801669
isallowed = False


@bot.command(hidden=True)
@commands.check(is_owner)
async def toggleburrman(ctx):
    global isallowed
    isallowed = not isallowed
    await ctx.send(isallowed)


@bot.command(hidden=True)
@commands.check(is_owner)
async def currentstatus(ctx):
    global isallowed
    await ctx.send(isallowed)


def check_status(member: discord.Member):
    if member.status == discord.Status.invisible:
        return True


@bot.event
async def on_voice_state_update(member, before, after):
    if (
        not isallowed
        and member.id == burrman
        and (check_status() or member.is_on_mobile())
    ):
        # if member.status == discord.Status.invisible:
        await member.move_to(None)
        print(f"{member} was disconnected from the voice channel on mobile.")


@bot.event
async def on_error(event, *args, **kwargs):
    print("on_error called")
    channel = bot.get_channel(1139802368024784946)
    print(channel)
    await bot.get_channel(1139802368024784946).send(
        f"Error: EVENT: {event}\nARGS: {args}\nKWARGS: {kwargs}"
    )


@bot.event
async def on_command_error(ctx, error):
    print("oncommanderror called", error)
    channel = ctx.channel.id
    await bot.get_channel(1139802368024784946).send(
        f"ctx: <#{channel}>\n```\nError: {error}```"
    )


@bot.event
async def on_command_completion(ctx):
    print("on command completion called")
    channel = ctx.channel.id
    await bot.get_channel(1139802190685405244).send(
        f"ctx: <#{channel}>\n{ctx.message.jump_url}>\n ============================="
    )



# ============================================================================================================================
try:
    bot.run(TOKEN)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
    else:
        raise e
