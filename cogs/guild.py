import utils
import discord
from discord.ext import commands

class guild(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = utils.Config.read(None);

    @commands.Cog.listener()
    async def on_raw_member_remove(self, payload: discord.RawMemberRemoveEvent):
        await self._sendMessage(payload)

    async def _sendMessage(self, payload: discord.RawMemberRemoveEvent):
        debug_channel = self.bot.get_channel(int(self.config.get("starboard_channel_id")))
        if not debug_channel:
            return
        
        await debug_channel.send(content=payload)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(guild(bot))