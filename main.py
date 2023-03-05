import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import check
import dotenv
import os

from emojifier import emojify
from keep_alive import keep_alive

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")


intents = discord.Intents.default()
intents.message_content = True
command_prefix = "k!"
guild_id = 607520631944118292

activity = discord.Activity(
    name="with your emotions 😘", type=discord.ActivityType.playing
)

bot = commands.Bot(command_prefix=command_prefix, activity=activity, intents=intents)

# Confirmation on bot login
@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    # try:
    #     # synced = await bot.tree.sync()
    #     synced = await bot.tree.sync(guild=discord.Object(...))
    #     # synced = await Bot.copy_global_to(*, 607520631944118292)
    #     print(f"Synced {len(synced)} command(s)")
    # except Exception as e:
    #     print(e)


# @bot.commands.command()
# async def sync() -> None:
# try:
# synced = await bot.tree.sync()
# print(f"Sync succesful: {len(synced)} commands were synced")
# await success_msg.delete(delay=5)
# except Exception as e:
#     print(e)

# Commands start from here

# Checking guild permissions
def is_in_guild(guild_id):
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.id == guild_id

    return check(predicate)

# Slash command to check info of a user
@bot.hybrid_group(fallback="enter")
# @bot.hybrid_command()
async def tag(message, member: discord.Member):
    """
        Displays the info of the user: the joining date and their current avatar
        
        Usage: /tag enter <@user>
    """
    await message.send(f"{member.mention} joined on {member.joined_at} {member.display_avatar}")

# @tag.command()
# async def emojifi(message, *lst):
#     lst = list(lst)
#     await message.send(emojify(lst))

@tag.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("I could not find that member...")


@bot.command()
# @commands.is_owner()
@is_in_guild(607520631944118292)
async def send(ctx):
    # Prompt the user for the channel ID and message content
    await ctx.send("Enter the channel ID:")
    channel_id_msg = await bot.wait_for(
        "message", check=lambda m: m.author == ctx.author
    )
    channel_id = int(channel_id_msg.content)

    await ctx.send("Enter the message content:")
    message_content_msg = await bot.wait_for(
        "message", check=lambda m: m.author == ctx.author
    )
    message_content = message_content_msg.content

    # Retrieve the TextChannel object for the specified ID
    channel = bot.get_channel(channel_id)

    if channel is None:
        await ctx.send("Invalid channel ID")
        return

    await channel.send(message_content)


# @bot.command()
# async def emoji(message, *lst):
#     lst = list(lst)
#     await message.channel.send(emojify(lst))


@bot.command()
async def hello(message):
    await message.channel.send("Hello!")


@bot.hybrid_command()
async def ping(message):
    await message.send("Let's go Baby!")


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

# keep_alive()
try:
    bot.run(TOKEN)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
    else:
        raise e
