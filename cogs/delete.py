from discord import Member
from discord.ext import commands
from functions.checks import is_owner
class Delete(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def purge(self, ctx, amount: int):
        """Deletes the message of the channel or the member if specified and the amount specified amount

        Args:
            amount (int): specify the number of message you want to delete
        """
        try:
            deleted = await ctx.channel.purge(limit=amount)
        except Exception as e:
            await ctx.send(e)
        finally:
            await ctx.channel.send(f"Deleted {len(deleted)} message(s)", delete_after=3)


    @commands.command(hidden=True, aliases=["del"])
    @commands.check(is_owner)
    async def delete(self, ctx, amount: int, member: Member):
        """Deletes the provided number of messages of the specified member only.

        Args:
            amount (int): specify the number of message you want to delete
            member (discord.Member):  specify the member.
        """

        def is_member_message(message):
            return message.author == member

        deleted = 0
        try:
            async for message in ctx.channel.history(limit=None):
                if is_member_message(message):
                    await message.delete()
                    deleted += 1
                    if deleted >= amount:
                        break
        except Exception as e:
            # print(e)
            await ctx.send(e, delete_after=3)
        finally:
            await ctx.channel.send(f"Deleted {deleted} message(s)", delete_after=3)
