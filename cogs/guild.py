import utils
import discord
from discord import app_commands
from discord.ext import commands

class guild(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = utils.Config.read(None);

    @commands.Cog.listener()
    async def on_raw_member_remove(self, payload: discord.RawMemberRemoveEvent):
        await self._sendMessage(payload)

    async def _sendMessage(self, payload: discord.RawMemberRemoveEvent):
        debug_channel = self.bot.get_channel(int(self.config.get("debug_channel_id")))
        if not debug_channel:
            return
        
        await debug_channel.send(content=payload)
    
    @app_commands.command(
        name = "guildinfo",
        description = "Give it a try!"
    )
    async def guild_info(
        self,
        interaction: discord.Interaction
    ):
        try:
            await interaction.response.defer(thinking=True)
            owner = interaction.guild.owner
            if not owner:
                owner = await interaction.guild.fetch_member(interaction.guild.owner_id)

            await interaction.edit_original_response(content=f"{owner.mention} (`{interaction.guild.owner_id}`)"
                                                + " is owner of this server!\n")
        except Exception as e:
            await interaction.edit_original_response(content="Couldn't fetch info.\n"
                                                    + "Why:\n`" + str(e) + "`")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(guild(bot))