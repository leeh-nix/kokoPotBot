import datetime
import io
import random
import re
import aiohttp
import discord
from discord.ext import commands
import dotenv
import os
from typing import Literal, Optional

# from discord.ext.commands import check

from cogs.reminder import *
from commissions.commissions_event_handler import chatko

from functions.extractReminderDetails import extractReminderDetails
from functions.imageTransform import imageTransform
from functions.checks import is_owner, is_in_guild

from commandLoader import add_cogs
from asyncio import run, sleep
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

gods = {
    "kuroko": 418364415856082954,
    "sakura": 413155474800902154,
}

owners = {
    "kuroko": 418364415856082954,
    "bisskut": 757478713402064996,
    "sakura": 413155474800902154,
    "riley": 911968173606195250,
    "marteeen": 840584597472936006,
    "marteeen_new": 1152840208635670528,
}
burrman = [758978243842801669]

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
    activity=activity,
    intents=intents,
)

# MoshiMoshi server
MoshiMoshi: discord.Guild.id = 852092404604469278


# Confirmation on bot login
@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    await startReminderLoop()


async def checkReminders():
    print("Checked reminders.")
    while True:
        currentTime = datetime.datetime.now().timestamp() // 1

        # Get reminders from the database collection that match the current time
        reminders = reminderCollection.find({"remindTime": {"$gte": currentTime}})

        for reminder in reminders:
            remindTime = reminder["remindTime"]
            userId = reminder["userId"]

            try:
                if remindTime == currentTime:
                    try:
                        print("Processing reminder:", reminder["text"])
                        user = bot.get_user(userId)
                        channel = await bot.fetch_channel(reminder["channelId"])
                        print("Fetched channel:", channel)
                        title = "I'm here to reminder you cutie!"
                        description = reminder["text"]
                        embed_url = reminder["messageLink"]
                        color = discord.Colour.random()
                        embed = discord.Embed(
                            title=title,
                            description=description,
                            url=embed_url,
                            color=color,
                            timestamp=datetime.datetime.fromtimestamp(remindTime),
                        )

                        embed.set_footer(
                            text=f"reminder id: {reminder['reminderId']}",
                            icon_url=user.display_avatar,
                        )
                        embed.set_author(name=user.name, icon_url=user.display_avatar)
                        # embed.set_thumbnail(url=user.display_avatar)

                        await channel.send(content=f"{user.mention}", embed=embed)

                        print("Message sent successfully.")

                    except Exception as e:
                        print("Error sending reminder:", e)
            except Exception as e:
                print("Error processing reminder:", e)
        await sleep(1)


async def startReminderLoop():
    while True:
        await checkReminders()


@bot.command(hidden=True)
@commands.check(is_owner)
async def startRemindLoop(ctx):
    await ctx.send("Reminder loop started")
    await startReminderLoop()
    print("startReminderLoop")


@startRemindLoop.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Error starting reminder loop")


@bot.hybrid_command()
async def reminder(
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
        color = discord.Color.red()
    else:
        reminderId = random.randint(1000, 9999)
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
        color = discord.Color.green()
    embed = discord.Embed(
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


@bot.command()
async def timer(ctx, *, message: str):
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
            color = discord.Color.red()
        else:
            reminderId = random.randint(1000, 9999)
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
            color = discord.Color.green()
            embed = discord.Embed(
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


@bot.hybrid_command()
async def getreminders(ctx):
    """Gets all reminders."""
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
            description = "...what are you looking for? theres nothing here for you."

        title = name
        footer = f"Found {counter} reminders"
        embed = discord.Embed(
            title=title, color=discord.Color.magenta(), description=description
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_thumbnail(url=ctx.author.display_avatar)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed, tts=False)

    except Exception as e:
        print(e)


@bot.hybrid_command(name="delreminder", description="Deletes a reminder by reminderId.")
async def delreminder(ctx, *, reminderid: int):
    """Deletes a reminder by reminderId."""
    try:
        reminderId = reminderid
        userId = ctx.author.id
        reminders = reminderCollection.find({"userId": userId})

        for reminder in reminders:
            reminderUserId = reminder["userId"]

            if userId == reminderUserId:
                reminderCollection.delete_one({"reminderId": reminderId})
                await ctx.send(f"Deleted reminder {reminderId}")
                return  # Stop iterating once a matching reminder is found

        # If no matching reminder is found
        await ctx.send(f"Reminder {reminderId} not found for user {userId}")

    except Exception as e:
        print(e)
        await ctx.send(
            f"An error occurred while deleting the reminder. ```py\nERROR: {e}```"
        )


@bot.command(hidden=True)
@is_in_guild(607520631944118292)
async def delReminders(ctx):
    """Deletes all remidner with remindTime less than current time."""
    currentTime = datetime.datetime.now().timestamp() // 1
    try:
        reminderCollection.delete_many({"remindTime": {"$lt": currentTime}})
        await bot.get_channel(955825787599216701).send(
            f"Deleted all completed reminders\nReminders Count: {reminderCollection.count_documents({})}"
        )
    except Exception as e:
        print(e)


@bot.command(hidden=True)
@commands.check(is_owner)
async def test(ctx, *, message):
    print(ctx)
    print(message)
    print(ctx.channel.id, ctx.channel.name, ctx.guild.name, ctx.guild.id)
    messageLink = ctx.message.jump_url
    print("message link: ", messageLink)
    await ctx.send(f"{message}, {messageLink}")


# Slash command to check info of a user
@bot.hybrid_group(fallback="enter")
async def tag(message, member: discord.Member):
    """
    Displays the info of the user: the joining date and their current avatar
    Usage: /tag enter <@user>
    """
    await message.send(
        f"{member.mention} joined on {member.joined_at} {member.display_avatar}"
    )


@tag.error
async def tag_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("I could not find that member...")


# current time
@bot.command()
async def time(ctx):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await ctx.send(f"The current time is: {current_time}")


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
    if height is None and width is None and aspect_ratio is None:
        return await ctx.send(
            "Please enter at least two values to resize your image. Either provide (h and w) OR (h/w with as)"
        )
    else:
        result = imageTransform(message, height, width, aspect_ratio)
    with io.BytesIO(result) as image_file:
        image_file.seek(0)
        if format == "gif":
            await ctx.send(file=discord.File(image_file, "image.gif"))
        else:
            await ctx.send(file=discord.File(image_file, "image.png"))


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
    embed.timestamp = datetime.datetime.now()
    await ctx.send(content, embed=embed, tts=False)


# EVENTS


async def on_command_error(ctx, error):
    print("oncommanderror called", error)
    channel = ctx.channel.id
    await bot.get_channel(1139802368024784946).send(
        f"ctx: <#{channel}>\n```\nError: {error}```"
    )


async def on_command_completion(ctx):
    print("on command completion called")
    channel = ctx.channel.id
    await bot.get_channel(1139802190685405244).send(
        f"ctx: <#{channel}>\n{ctx.message.jump_url}>\n =============================",
        suppress_embeds=True,
    )


async def on_message(msg):
    member = msg.author
    content: str = msg.content
    modified_ctx = await bot.get_context(msg)
    if content.startswith("reminder for ") or content.startswith("reminder"):
        try:
            print("ON_MESSAGE REMINDER INVOKED")

            timer_command = bot.get_command("timer")
            if timer_command:
                await timer_command.invoke(modified_ctx)
        except Exception as e:
            print(member.name)
            print(e)
    if (
        member.id in burrman
        and member.is_on_mobile()
        and not member.desktop_status == "invisible"
    ):
        print("started with mobile")
        await msg.channel.send("typing from mobile eww")
        await msg.channel.send(f"# {member.mention} **PC SE AO** 🤢 🤮 ")
    if member.id in owners.values():
        if msg.content.lower().startswith("chatko"):
            print("started with chatko")
            try:
                await chatko(msg, modified_ctx)
                print("chatko")
            except Exception as e:
                print(e, member.name)
            finally:
                await msg.reply("# get out and uninstall valo... 👈🤓")

    # passing the message command for other bot commands if not chatko not found
    # await bot.process_commands(msg)


# ============================================================================================================================


EVENTS = [on_command_error, on_command_completion, on_message]


def add_events():
    for event in EVENTS:
        bot.add_listener(event)


async def main():
    async with bot:
        add_events()
        await add_cogs(bot)
        await bot.start(TOKEN, reconnect=True)


try:
    run(main())
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
    else:
        raise e
