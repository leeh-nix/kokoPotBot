from discord import Embed, Color
from discord.ext import commands
from functions.geminiText import sendResponse


class Gemini(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="gemini")
    async def geminiPro(self, ctx: commands.Context, *, text):
        await ctx.typing()
        try:
            res = sendResponse(text)
        except Exception as e:
            print("ERROR while calling gemini: ", e)
        title = text[:256] if len(text) > 256 else text
        embed = Embed(
            title=title,
            description=res,
            timestamp=ctx.message.created_at,
            color=Color.dark_teal(),
        )
        await ctx.send(embed=embed)
