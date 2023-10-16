import datetime
import io
import re
import discord
from discord.ext import commands
import dotenv
import os
from typing import Literal, Optional
# from discord.ext.commands import check

from cogs.reminder import reminderCollection, createReminder
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
        reminders = reminderCollection.find({"remindTime": {"$lte": currentTime}})

        for reminder in reminders:
            remindTime = reminder["remindTime"]
            text = reminder["text"]
            userId = reminder["userId"]
            channel = reminder["channelId"]

            if remindTime == currentTime:
                await bot.get_channel(channel).send(
                    f"<@{userId}>, here's your reminder: {text}"
                )
                reminderCollection.delete_one({"userID": userId})
            # elif remindTime < currentTime:
        # Remove the reminder from the collection after processing
        # print("Checked reminders.")
        # Wait for a specific remindTime before checking again (e.g., 1 second)
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


@bot.command()
async def timer(ctx, *, message: str):
    """Sets a reminder for the specified time.
    Usage: reminder for <Reminder Time> <Reminder Text>
    eg. k!timer 1d 2h 3m 4s to touch grass
    """
    print("=================================================")
    print(message, type(message))
    remove_prefix_pattern = r"(?:reminder(?: for)?)\s+(.+)"
    matched = re.search(remove_prefix_pattern, message, re.IGNORECASE)
    message = matched.group(1)
    givenMessage = message
    print("givenMessage", givenMessage)

    reminderDetails = extractReminderDetails(givenMessage)

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
            # await ctx.channel.send("Reminder added successfully")
            await ctx.send(
                f"Reminder set for <t:{remindTime}:f>. I will notify you in <t:{remindTime}:R>."
            )
    except Exception as e:
        await ctx.send(
            "An error occurred while setting the reminder. Please try again later."
        )
    print(f"{reminderCollection.count_documents({})} done!")


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
        print(e)


@bot.command(hidden=True)
@commands.check(is_owner)
async def test(ctx, *, message):
    print(ctx)
    print(message)
    print(ctx.channel.id, ctx.channel.name, ctx.guild.name, ctx.guild.id)
    await ctx.send(message)


# Commands start from here

# Slash command to check info of a user
@bot.hybrid_group(fallback="enter")
async def tag(message, member: discord.Member):
    """
    Displays the info of the user: the joining date and their current avatar
    Usage: /tag enter <@user>
    """
    await message.send(
        f"{member.mention} joined on {member.joined_at} {member.display_avatar}")


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
    embed.timestamp = datetime.datetime.utcnow()
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
