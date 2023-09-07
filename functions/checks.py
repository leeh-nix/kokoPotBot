import discord
from discord.ext.commands import check

# Add checks here along with the variables used in it

owners = {
    "kuroko": 418364415856082954,
    "bisskut": 757478713402064996,
    "sakura": 413155474800902154,
    "rileyyy": 911968173606195250,
    "Marteeen": 840584597472936006,
}

guilds = {
    "MoshiMoshi": 852092404604469278
}

# Owner
async def is_owner(ctx):
    for values, keys in owners.items():
        if ctx.author.id == keys:
            return True

# Guild
def is_in_guild(guild_id: discord.Guild.id) -> check:
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.id == guild_id
    return check(predicate)
# def is_in_guild(guild_id) -> check:
#     def predicate(ctx):
#         for values, keys in guilds.items():
#             if ctx.guild.id == keys:
#                 return True
#         return ctx.guild is not None and ctx.guild.id == guild_id
#     return check(predicate)
