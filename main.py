import datetime
import io
import random
import re
import discord
from discord.ext import commands
import dotenv
import os
from typing import Literal, Optional

from cogs.reminder import *
from commissions.commissions_event_handler import chatko

from functions.extractReminderDetails import extractReminderDetails
from functions.imageTransform import imageTransform
from functions.geminiVision import geminiVision
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
    "marteeen_new": 1152840208635670528,
    "shazam bolt": 829417226040901653,
}
burrman = [758978243842801669]

channelList = {
    "koko bot pot testing": 1048553311768420363,
    "bot-errors": 1139802368024784946,
    "invoked-commands": 1139802190685405244,
}

activity = discord.Activity(
    name="with your emotions 😘", type=discord.ActivityType.playing
)

bot = commands.Bot(
    command_prefix=command_prefix,
    activity=activity,
    intents=intents,
)

# MoshiMoshi server
MoshiMoshi: discord.Guild.id = 852092404604469278 # type: ignore


# Confirmation on bot login
@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    await startReminderLoop()


async def checkReminders():
    """Asynchronous function that checks reminders in the database collection and sends reminder messages to users."""
    print("Checked reminders.")
    while True:
        currentTime = datetime.datetime.now().timestamp() // 1

        # Get reminders from the database collection that match the current time
        # TODO - try doing "$lte" logic for the "remindTime"
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
async def info_error(ctx: commands.Context, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Error starting reminder loop")


@bot.command(hidden=True)
@commands.check(is_owner)
async def test(ctx: commands.Context, *, message):
    print(message)
    print(ctx.channel.id, ctx.channel.name, ctx.guild.name, ctx.guild.id)
    await ctx.send_help(test)
    await ctx.send(f"{ctx.message.reference}")
    await ctx.send(f"{message}")


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
async def tag_error(ctx: commands.Context, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("I could not find that member...")


# current time
@bot.command()
async def time(ctx):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await ctx.send(f"The current time is: {current_time}")


@bot.hybrid_command()
async def imageresize(
    ctx: commands.Context,
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


@bot.hybrid_command(name="embed")
async def embedSender(
    ctx: commands.Context,
    content,
    title,
    description,
    color: discord.Colour,
    footer: Optional[str] = None,
    embed_url: Optional[str] = None,
):
    """Create and send an embed.

    Args:
        ctx (discord.Context): _description_
        content (str): Content to send with the embed
        title (str): Title for the embed
        description (str): Description for the embed
        color (discord.Colour): Color for the embed
        footer (Optional[str], optional): Any footer for the embed. Defaults to None.
        embed_url (Optional[str], optional): Embed url. Defaults to None.
    """
    embed = discord.Embed(
        title=title, description=description, color=color, url=embed_url
    )
    embed.set_footer(text=footer)
    embed.timestamp = datetime.datetime.now()
    await ctx.send(content, embed=embed, tts=False)


# REVIEW - https://stackoverflow.com/questions/75348702/how-to-edit-images-in-embeds-discord-py

# EVENTS


async def on_command_error(ctx: commands.Context, error):
    print("On command error: ", error)
    user = ctx.author
    embed = discord.Embed(
        title=ctx.command.name,
        description=f"```{error}```\n{ctx.message.jump_url or 'No link found'}",
        color=discord.Color.red(),
        timestamp=datetime.datetime.now(),
    )
    embed.set_footer(
        text=("Requested by " + user.name) or None,
        icon_url=user.display_avatar or None,
    )
    await ctx.send(embed=embed, ephemeral=True)
    await bot.get_channel(channelList["bot-errors"]).send(embed=embed)


async def on_command_completion(ctx):
    commandName = ctx.command.name
    user = ctx.author
    print(f"Command successfully executed: {commandName} by {user.name}")
    embed = discord.Embed(
        title=commandName,
        description=ctx.message.jump_url,
        color=discord.Color.blue(),
        timestamp=datetime.datetime.now(),
    )
    embed.set_footer(
        text="Requested by " + user.name,
        icon_url=user.display_avatar,
    )
    await bot.get_channel(channelList["invoked-commands"]).send(embed=embed)


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

    # Gemini Vision model
    if content.startswith("hey gemini"):
        print("gemini vision")
        img: discord.Attachment = msg.attachments[0]
        img = await img.read()
        try:
            res = geminiVision(content, img)
        except Exception as e:
            res = "Error: " + str(e)
        await msg.channel.send(res)

    # COMMISSION PART: (start)
    if (
        member.id in burrman
        and member.is_on_mobile()
        and not member.desktop_status == "invisible"
    ):
        print("started with mobile")
        await msg.channel.send(f"{member.mention} **PC SE AO** 🤢 🤮 ")
    if member.id in owners.values():
        if msg.content.lower() == "chatko":
            from functions.geminiText import genai

            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash-latest",
                safety_settings=None,
                system_instruction="""your response is being sent when the members are kicked from vc. 
        So you're task is to reply with a small creative insult and it need not to be related to games. it can be anything;
        from tech to education to job/unemployment and race, sex, relationship status with random dank emojis at the end... 
        But you must only respond with one insult in output. NO salutations, NO here's this that nothing nada.""",
            )

            generation_config = genai.types.GenerationConfig(
                temperature=1.5,
            )

            response = model.generate_content(
                contents="one liner insult for example: `# Get out and uninstall valorant... 👈🤓`",
                generation_config=generation_config,
            )
            print("invoking chatko")
            try:
                await chatko(msg, modified_ctx)
            except Exception as e:
                print(e, member.name)
            finally:
                await msg.channel.send(f"# {response.text}")

    # passing the message command for other bot commands if not chatko not found
    # await bot.process_commands(msg)
    # COMMISSION PART: (end)


# ============================================================================================================================ #


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
