from functions.popCatRequests import *
from discord.ext import commands
import discord

class popCatAPIImageCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def encode(ctx, *, message):
        """Encode your message in binary"""
        message = "".join(message)
        result = encoding(message)
        await ctx.send(f"The encoded message: {result}")


    @commands.command()
    async def decode(ctx, *, message):
        """Decode your binary message"""
        message = "".join(message)
        result = decoding(message)
        await ctx.send(f"The decoded message: {result}")


    @commands.command()
    async def doublestruck(ctx, *, message):
        message = "".join(message)
        result = doublestruckAPI(message)
        await ctx.send(f"{result}")


    @commands.command()
    async def clown(ctx, message, *args):
        # url = f"{API_BASE_URL}/clown?image={message}"
        """You're a clown

        Args:
            message (image link): Provide image link ending with (.jpg, .jpeg, .png)

        Raises:
            ValueError: _description_
        """
        if not message.startswith("http") or not message.endswith(
            (".jpg", ".jpeg", ".png", ".gif")
        ):
            await ctx.send("Please enter valid url.")
            raise ValueError("Invalid image URL")
        else:
            result = await clownApiRequest(message)
        with open("clown_image.png", "wb") as file:
            file.write(result)

        with open("clown_image.png", "rb") as file:
            await ctx.send(file=discord.File(file, "clown_image.png"))


    @commands.command()
    async def advertise(ctx, message):
        # url = f"{API_BASE_URL}/ad?image={message}"
        """Advertise your image

        Args:
            message (image link): Provide image link ending with (.jpg, .jpeg, .png)

        Raises:
            ValueError: Provided message doesn't contain the image link
        """
        if not message.startswith("http") or not message.endswith(
            (".jpg", ".jpeg", ".png", ".gif")
        ):
            await ctx.send("Please enter valid url.")
            raise ValueError("Invalid image URL")
        else:
            result = await adApiRequest(message)
        with open("advertise_image.png", "wb") as file:
            file.write(result)

        with open("advertise_image.png", "rb") as file:
            await ctx.send(file=discord.File(file, "advertise_image.png"))


    @commands.command()
    async def uncover(ctx, message):
        """Uncover the poster 

        Args:
            message (image link): Provide image link ending with (.jpg, .jpeg, .png)

        Raises:
            ValueError: _description_
        """
        # url = f"{API_BASE_URL}/uncover?image={message}"
        if not message.startswith("http") or not message.endswith(
            (".jpg", ".jpeg", ".png", ".gif")
        ):
            await ctx.send("Please enter valid url.")
            raise ValueError("Invalid image URL")
        else:
            result = await uncoverApiRequest(message)
        with open("uncover_image.png", "wb") as file:
            file.write(result)

        with open("uncover_image.png", "rb") as file:
            await ctx.send(file=discord.File(file, "uncover_image.png"))


    @commands.command()
    async def jail(ctx, message):
        """Sends the image with adding a layer of jail bars

        Args:
            message (image link): provide image link with ending image extension (.png, .jpg, jpeg etc)

        Raises:
            ValueError: provided message doesn't contain the image link
        """
        # url = f"{API_BASE_URL}/jail?image={message}"
        # TODO: use regex to trim the link provided and add the image extension
        if not message.startswith("http") or not message.endswith(
            (".jpg", ".jpeg", ".png", ".gif")
        ):
            await ctx.send("Please enter valid url.")
            raise ValueError("Invalid image URL")
        else:
            result = await jailApiRequest(message)
        with open("jail_image.png", "wb") as file:
            file.write(result)

        with open("jail_image.png", "rb") as file:
            await ctx.send(file=discord.File(file, "jail_image.png"))
            
            
    @clown.error
    async def clown_error(self, ctx, error):
        await ctx.send(error)
    
    @jail.error
    async def jail_error(self, ctx, error):
        await ctx.send(error)
    
    @uncover.error
    async def uncover_error(self, ctx, error):
        await ctx.send(error)
        
    @advertise.error
    async def advertise_error(self, ctx, error):
        await ctx.send(error)