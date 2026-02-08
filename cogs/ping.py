import utils
import discord
from discord import app_commands
from discord.ext import commands

class ping(commands.Cog, name = "ping"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.config = utils.Config.read()

    @app_commands.command(
        name = "ping",
        description = "Give it a try!"
    )
    async def ping(
        self,
        interaction: discord.Interaction
    ):
        await interaction.response.send_message(content="Pong!")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ping(bot))