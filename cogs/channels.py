import utils
import discord
from discord import app_commands
from discord.ext import commands

class channels(commands.GroupCog, name = "channels"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.config = utils.Config.read(None)

    @app_commands.command(
        name = "test",
        description = "Give it a try!"
    )
    async def test(
        self,
        interaction: discord.Interaction
    ):
        await interaction.response.defer(thinking=True)
        overwrites = interaction.channel.overwrites

        if not overwrites:
            await interaction.edit_original_response(content="This channel has no permission overwrites.")
            return
        
        channel_managers = []

        for target, overwrite in overwrites.items():
            if overwrite.manage_channels is True:
                channel_managers.append(f"- {target.mention} ({'Role' if isinstance(target, discord.Role) else 'Member'})")

        if channel_managers:
            await interaction.edit_original_response(
                content=f"Users/Roles with **\"Manage Channel\"** in this channel:\n" + "\n".join(channel_managers))
        else:
            await interaction.edit_original_response(
                content="No users or roles with explicit `manage_channels` permission found in this channel's overwrites.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(channels(bot))