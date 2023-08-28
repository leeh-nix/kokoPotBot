import discord
from discord.ext import commands
from discord.ext.commands import TextChannelConverter
from functions.checks import is_owner


class Send(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.check(is_owner)
    async def send(self, ctx, channel: discord.TextChannel, *, message):
        """Sends a message to the specified channel.

        Args:
            channel (discord.TextChannel): The channel to send the message to.
            message (str): The message content.
        """
        try:
            await channel.send(message)
            await ctx.send("Message sent successfully.", delete_after=5)
        except discord.HTTPException as e:
            await ctx.send(f"An error occurred: {e}")

    @send.error
    async def send_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You are not the bot owner.", delete_after=5)
        else:
            await ctx.send(f"An error occurred: {error}")