# from main import bot
from functions.checks import *

# from commissions.functions import chatko
from discord.ext import commands

burrman = [758978243842801669]
isallowed = False


async def chatko(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        voice_channel = ctx.author.voice.channel
        for member in voice_channel.members:
            await member.move_to(None)


class MoshiMoshi(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def toggleburrman(self, ctx):
        global isallowed
        isallowed = not isallowed
        print(isallowed)
        await ctx.send(isallowed)

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def currentstatus(self, ctx):
        global isallowed
        await ctx.send(isallowed)

async def on_message(message):
    member = message.author
    if (
        member.id in burrman
        and member.is_on_mobile()
        and not member.desktop_status == "invisible"
    ):
        print("started with mobile")
        await message.channel.send("typing from mobile eww")
        await message.channel.send(f"# {member.mention} **PC SE AO** 🤢 🤮 ")
    if member.id in owners.values():
        if message.content.lower().startswith("chatko"):
            print("started with chatko")
            try:
                await chatko(message)
                print("chatko")
            except Exception as e:
                print(e)
            finally:
                await message.reply("kal ana kall")

    # passing the message command for other bot commands if not chatko not found
    # await bot.process_commands(message)