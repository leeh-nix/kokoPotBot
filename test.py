import datetime
import discord
from discord.ext import commands
from discord.ext.commands import check
import asyncio
import dotenv
import os
from emojifier import emojify
import tracemalloc


tracemalloc.start()
dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
command_prefix = "k!"
guild_id = 607520631944118292
guild = 607520631944118292

activity = discord.Activity(
    name="with your emotions 😘", type=discord.ActivityType.playing
)

bot = commands.Bot(command_prefix=command_prefix, activity=activity, intents=intents)


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
async def remind(ctx, duration: int, time_unit: str, *, reminder: str):
    # eastern = pytz.timezone('US/Eastern')
    # current_time = datetime.datetime.now(eastern).timestamp()
    valid_units = [
        "second",
        "seconds",
        "minute",
        "minutes",
        "hour",
        "hours",
        "day",
        "days",
    ]

    if time_unit not in valid_units:
        await ctx.send(
            "Invalid time unit. Please use 'minute(s)', 'hour(s)', or 'day(s)'."
        )
        return
    if duration < 1:
        return "Invalid time. Please provide a positive number"

    current_time = datetime.datetime.now().timestamp()

    if timestamp < current_time:
        await ctx.send("Invalid timestamp. Please provide a future timestamp.")
        return

    delta = timestamp - current_time
    reminder_time = datetime.datetime.fromtimestamp(timestamp).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    await ctx.send(
        f"Reminder set for {reminder_time}. I will notify you in {delta//1} seconds."
    )

    await asyncio.sleep(delta)
    await ctx.send(f"{ctx.author.mention}, here's your reminder: {reminder}")


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

# keep_alive()


# ============================================================================================================================


def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


@bot.command()
@is_in_guild(607520631944118292)
async def eval_fn(ctx, *, cmd):
    """Evaluates input.

    Input is interpreted as newline seperated statements.
    If the last statement is an expression, that is the return value.

    Usable globals:
        - `bot`: the bot instance
        - `discord`: the discord module
        - `commands`: the discord.ext.commands module
        - `ctx`: the invokation context
        - `__import__`: the builtin `__import__` function

    Such that `>eval 1 + 1` gives `2` as the result.

    The following invokation will cause the bot to send the text '9'
    to the channel of invokation and return '3' as the result of evaluating

    >eval ```
    a = 1 + 2
    b = a * 2
    await ctx.send(a + b)
    a
    ```
    """
    fn_name = "_eval_expr"

    cmd = cmd.strip("` ")

    # add a layer of indentation
    cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

    # wrap in async def body
    body = f"async def {fn_name}():\n{cmd}"

    parsed = ast.parse(body)
    body = parsed.body[0].body

    insert_returns(body)

    env = {
        "bot": ctx.bot,
        "discord": discord,
        "commands": commands,
        "ctx": ctx,
        "__import__": __import__,
    }
    exec(compile(parsed, filename="<ast>", mode="exec"), env)

    result = await eval(f"{fn_name}()", env)
    await ctx.send(result)


# TODO @command.


try:
    bot.run(TOKEN)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
    else:
        raise e
