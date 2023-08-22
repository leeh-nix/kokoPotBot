from discord.ext import commands
from functions.konachanImgExtractor import konachanImgExtractor

# kokos pot server, nsfw bot spam GYAN's server
# konachan_list = [1124585323196862604, 1138102688098304081]
konachan_channels = {
    "kokos pot server" : 1124585323196862604,
    "gyan's nsfw bot spam thread": 1138102688098304081
}

class Konachan(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    @commands.hybrid_command(hidden=True)
    # @commands.check(is_owner)
    # @is_in_guild(607520631944118292)
    async def konachan(self, ctx, tags):
        """Sends some images from konachan based on tag provided is it exists"""
        
        if ctx.channel.id in konachan_channels.values():
            data = konachanImgExtractor(tags)
            try:
                await ctx.send(" ".join(data))
            except Exception as e:
                print(e)
        else:
            await ctx.send("Error: You are not in the right channel.")