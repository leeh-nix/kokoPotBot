from cogs.popCatAPI import popCatAPIImageCommands
from cogs.sync import Sync
from cogs.funText import TextCommands
from cogs.konachan import Konachan
from cogs.send import Send
from cogs.delete import Delete
from cogs.github import Github
from cogs.gemini import Gemini

# from cogs.kokoshot import Kokoshot
from commissions.commissions_event_handler import *

COGS = [
    Sync,
    TextCommands,
    popCatAPIImageCommands,
    Konachan,
    Send,
    MoshiMoshi,
    Delete,
    Github,
    Gemini,
    # Kokoshot,
]


async def add_cogs(bot):
    for cog in COGS:
        await bot.add_cog(cog(bot))
