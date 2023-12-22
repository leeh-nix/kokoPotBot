from functions.kokoshotRequest import kokoshotRequest
from discord.ext import commands
from typing import Optional, Literal
import dotenv
import os

dotenv.load_dotenv()
CUSTOMER_KEY = os.getenv("CUSTOMER_KEY")


class Kokoshot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(aliases=["ss"])
    async def kokoshot(
        self,
        ctx,
        url,
        cachelimit: Optional[int] = 3,
        delay: Optional[int] = 200,
        zoom: Optional[int] = 100,
        dimension: Optional[
            Literal["1366x768", "1920x1080", "2560x1440", "1024xfull"]
        ] = "1366x768",
        device: Optional[Literal["desktop", "phone", "tablet"]] = "desktop",
    ):
        """
        Takes a URL and generates a screenshot of the webpage using the Screenshot Machine API.

        Parameters:
            ctx: The context object representing the current state of the bot.
            url: The URL of the webpage to take a screenshot of.
            cachelimit: (Optional) The number of times the screenshot will be cached. Defaults to 3.
            delay: (Optional) The delay in milliseconds before taking the screenshot. Defaults to 200.
            zoom: (Optional) The zoom level of the screenshot. Defaults to 100.
            dimension: (Optional) The dimensions of the screenshot. Can be one of "1366x768", "1920x1080", "2560x1440", or "1024xfull". Defaults to "1366x768".
            device: (Optional) The device type for the screenshot. Can be one of "desktop", "phone", or "tablet". Defaults to "desktop".

        Returns:
            None
        """
        await ctx.send(
            f"https://api.screenshotmachine.com/?key={CUSTOMER_KEY}&url={url}&cacheLimit={cachelimit}&delay={delay}&zoom={zoom}&device={device}&dimension={dimension}",
        )
