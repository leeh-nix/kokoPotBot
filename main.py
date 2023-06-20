import datetime
import discord
from discord.ext import commands
from discord.ext.commands import check
import asyncio
import dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pytz
from emojifier import emojify
import tracemalloc


tracemalloc.start()
dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
# URI = os.getenv("URI")


intents = discord.Intents.default()
intents.message_content = True
command_prefix = "k!"
guild_id = 607520631944118292
guild = 607520631944118292

activity = discord.Activity(
    name="with your emotions 😘", type=discord.ActivityType.playing
)

bot = commands.Bot(command_prefix=command_prefix, activity=activity, intents=intents)

URI = "mongodb+srv://kokose:gfelUa0fyUUVKO0M@kokosbotpot.rokrapr.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(URI, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
# @bot.command()
# async def dbconnect(ctx):
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
db = client.get_database('kokospotbot_db')
reminder = db.reminder #collection: reminder

# Confirmation on bot login
@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    try:
        # synced = await bot.tree.sync()
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        # synced = await bot.tree.sync(guild=discord.Object(...))
        # synced = await Bot.copy_global_to(*, 607520631944118292)
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


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
async def send(ctx, channel_id: int, *, message):
    channel = bot.get_channel(channel_id)
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
@bot.command()
async def remind(ctx, duration: int, time_unit: str, *, txt: str):
    time_unit = time_unit.lower()
    valid_units = ["minute", "minutes", "hour", "hours", "day", "days"]

    if time_unit not in valid_units:
        await ctx.send(
            "Invalid time unit. Please use 'minute(s)', 'hour(s)', or 'day(s)'."
        )
        return

    if duration < 1:
        await ctx.send("Invalid duration. Please provide a positive number.")
        return
    
    new_reminder = {
        'duration': duration,
        'time_unit' : time_unit,
        'txt': txt
    }
    print(new_reminder)
    reminder.insert_one(new_reminder)
    # ctx.send(reminder.count_documents({}), "done!")


    # await ctx.send(
    #     f"Reminder set for {reminder_time} EDT. I will notify you in {duration} {time_unit}."
    # )

    # delta = (reminder_time - current_time).total_seconds()
    # await asyncio.sleep(delta)
    # await ctx.send(f"{ctx.author.mention}, here's your reminder: {reminder}")


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
