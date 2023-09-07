import discord
from discord.ext import commands
from functions.checks import is_in_guild
# from functions.translator import translator

class TextCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, message):
        await message.channel.send("Hello!")

    @commands.hybrid_command()
    async def ping(self, message):
        await message.send(f"Let's go Baby! ```{(self.bot.latency * 1000)//1} ms```")

    @commands.command()
    async def pat(self, message):
        await message.channel.send(
            "Aww thank you cutie i really need that sometimes <3"
        )

    @commands.hybrid_command()
    @is_in_guild(852092404604469278) #MoshiMoshi
    async def pingalinga(self, ctx, amount: int, member: discord.Member, *, message):
        if amount < 15:
            for i in range(amount):
                await ctx.send(f"{message} {member.mention}")
        else: 
            await ctx.send(f"{message} <@{ctx.author.id}> ||try amount <15 times||")
    
    @pingalinga.error
    async def pingalinga_error(self, ctx, error):
        await ctx.send(f"eihter its not available for your server or you're using it wrongly\nUse Syntax: k!pingalinga <amount(15)> <member> <message>")

    @commands.command(aliases=["tq", "thankq", "ty"])
    async def thanks(self, message):
        await message.channel.send("Always there for you <3")
