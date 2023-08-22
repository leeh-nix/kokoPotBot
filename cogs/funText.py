from discord.ext import commands

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
        await message.channel.send("Aww thank you cutie i really need that sometimes <3")


    @commands.command(aliases=["tq", "thankq", "ty"])
    async def thanks(self, message):
        await message.channel.send("Always there for you <3")
    