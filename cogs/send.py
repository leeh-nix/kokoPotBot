from discord.ext import commands
from discord import TextChannel
from functions.checks import is_owner

class Send(commands.Cog):
    @commands.hybrid_command()
    @commands.check(is_owner)
    async def send(ctx, channel: TextChannel, message):
        """Sends a message to specified channel
        Args:
            channelId (int): specify the channel ID
            message (str): Message you want to send
        """
        channel = channel
        if channel:
            await channel.send(message)
            await ctx.send("Message sent successfully.")
        else:
            await ctx.send("Invalid channel ID.")
            
    @send.error
    async def send_error(self, ctx, error):
        await ctx.send(error)