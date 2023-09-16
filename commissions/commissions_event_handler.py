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