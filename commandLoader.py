from cogs.popCatAPI import popCatAPITextCommands
from cogs.sync import Sync
from cogs.funText import TextCommands
from cogs.konachan import Konachan
from cogs.send import Send

COGS = [Sync, TextCommands, popCatAPITextCommands, Konachan, Send]

async def add_cogs(bot):
    for cog in COGS:
        await bot.add_cog(cog(bot))

