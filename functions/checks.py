from discord.ext.commands import check

# Add checks here along with the variables used in it

owners = {
    "kuroko": 418364415856082954,
    "bisskut": 757478713402064996,
    "sakura": 413155474800902154,
    "rileyyy": 911968173606195250,
    "Marteeen": 840584597472936006,
}

# Owner
async def is_owner(ctx):
    for values, keys in owners.items():
        if ctx.author.id == keys:
            return True

# Guild
def is_in_guild(guild_id):
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.id == guild_id
    return check(predicate)
