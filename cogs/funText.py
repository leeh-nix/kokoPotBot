import discord
from discord.ext import commands
from functions.checks import is_in_guild, is_owner

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
    @commands.check(is_owner)
    async def pingalinga(self, ctx, amount: int, member: discord.Member, *, message):
        if amount <= 15:
            for i in range(amount):
                await ctx.send(f"{message} {member.mention}")
        else:
            await ctx.send(f"{message} <@{ctx.author.id}> ||try amount <15 times||")

    @pingalinga.error
    async def pingalinga_error(self, ctx, error):
        await ctx.send(
            f"Either you don't have the privilage to use this command or you're using it wrongly\n`k!pingalinga <amount(15)> <member> <message>`"
        )

    # can not check if the user's invisible or not atm so it always returns the else part
    # @commands.hybrid_command()
    # async def expose(self, ctx: commands.Context, member: discord.Member):
    #     if member.desktop_status == "invisible":
    #         print("EXPOSED")
    #         await ctx.send(
    #             f"EXPOSED!! 😱😈 {member.mention} is online. `{member.activity}`"
    #         )
    #     else:
    #         await ctx.send("welp no exposing today")

    @commands.command(aliases=["tq", "thankq", "ty"])
    async def thanks(self, message):
        await message.channel.send("Always there for you <3")
