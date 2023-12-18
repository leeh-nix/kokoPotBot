from discord import Embed
from discord.ext import commands
from functions.geminiText import sendResponse


class Gemini(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gemini")
    async def geminiPro(self, ctx, *, text):
        res = sendResponse(text)
        embed = Embed(
            title=text,
            description=res,
        )
        await ctx.send(embed=embed)
