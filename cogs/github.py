import discord
from discord.ext import commands
import aiohttp


class Github(commands.Cog):
    """
    A cog (module) in a Discord bot that allows users to fetch information about a GitHub repository.

    This class provides a command that allows users to fetch information about a GitHub repository.
    It makes an HTTP request to the GitHub API and retrieves data about the repository.
    It then formats the data into an embedded message and sends it to the Discord server.

    Attributes:
        bot (discord.ext.commands.Bot): The Discord bot instance.

    Example Usage:
        k!github owner repo
    """

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="github")
    async def github_command(self, ctx, owner, repo):
        """
        A command that allows users to fetch information about a GitHub repository.

        Args:
            owner (str): The owner of the GitHub repository.
            repo (str): The name of the GitHub repository.
        """
        if owner == "" or repo == "":
            await ctx.send("Error: Please provide both owner and repo.")
            return
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.github.com/repos/{owner}/{repo}"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    embed = discord.Embed(
                        title=data["name"],
                        description=data["description"],
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="Stars", value=data["stargazers_count"])
                    embed.add_field(name="Forks", value=data["forks_count"])
                    embed.add_field(name="Watchers", value=data["subscribers_count"])
                    embed.add_field(name="Latest Commit", value=data["pushed_at"])
                    embed.add_field(
                        name="License",
                        value=data["license"]["name"] if data["license"] else "None",
                    )
                    embed.add_field(name="Issues", value=data["open_issues_count"])
                    embed.add_field(
                        name="Pull Requests", value=data["open_issues_count"]
                    )
                    embed.add_field(name="Repository URL", value=data["html_url"])
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(
                        f"Error: {response.status} - Unable to fetch repository information."
                    )
