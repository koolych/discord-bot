import utils

import discord
from discord import app_commands
from discord.ext import commands

class ping(commands.GroupCog, name = "ping"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.config = utils.Config.read()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ping(bot))