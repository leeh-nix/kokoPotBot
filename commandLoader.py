from cogs.popCatAPI import popCatAPITextCommands
from cogs.sync import Sync
from cogs.funText import TextCommands
from cogs.konachan import Konachan
from cogs.send import Send
from commissions.commissions_event_handler import *

COGS = [Sync, TextCommands, popCatAPITextCommands, Konachan, Send, MoshiMoshi]

async def add_cogs(bot):
    for cog in COGS:
        await bot.add_cog(cog(bot))

