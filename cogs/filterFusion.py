import io
import re
import discord
from discord.ext import commands
import requests


class FilterFusion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.invert_api = "https://filter-fusion.vercel.app/api/filter/invert"

    @commands.command()
    async def invert(self, ctx: commands.Context):
        messageId = ctx.message.reference.message_id
        referencedMessage: discord.Message = await ctx.fetch_message(messageId)
        messageContent = referencedMessage.content

        pattern = r"\b((https:).*(\.(png)|(jpg)|(jpeg)|(webp)))"

        matches = re.findall(pattern, messageContent)

        try:
            if matches:
                print(matches[0][0])
                image_url = matches[0][0]
                data = {"image_url": image_url}
                response = requests.request("POST", self.invert_api, data=data)
            # print("RESPONSE", response)
            # print("RESPONSE CONTENT", response.content)

            else:
                await discord.Attachment.save(
                    referencedMessage.attachments[0], "image.png"
                )
                image = "image.png"
                files = {"image": open(image, "rb")}
                response = requests.post(
                    self.invert_api,
                    files=files,
                )

            with io.BytesIO(response.content) as image_file:
                image_file.seek(0)
                await ctx.typing()
                await ctx.send(file=discord.File(image_file, "inverted_image.png"))
                await ctx.message.delete()
                # await referencedMessage.delete()
        except Exception as e:
            print(e)
            await ctx.send(f"```{e}```")
