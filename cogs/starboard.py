import json
import os
import discord
from discord.ext import commands
import utils

STARBOARD_FILE = "starboard_messages.json"

class Starboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = utils.Config.read(None)
        channel_id = self.config.get("starboard_channel_id")
        self.starboard_channel_id = int(channel_id) if channel_id else None
        self.star_threshold = self.config.get("star_threshold", 2)
        self.star_emoji = self.config.get("star_emoji", "⭐")
        self.starboard_messages = self.load_starboard_messages()

    def load_starboard_messages(self):
        if os.path.exists(STARBOARD_FILE):
            with open(STARBOARD_FILE, 'r', encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def save_starboard_messages(self):
        with open(STARBOARD_FILE, 'w', encoding="utf-8") as f:
            json.dump(self.starboard_messages, f, indent=4)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        await self._update_starboard(payload)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        await self._update_starboard(payload)

    async def _update_starboard(self, payload: discord.RawReactionActionEvent):
        if str(payload.emoji) != self.star_emoji:
            return

        if not self.starboard_channel_id:
            return

        channel = self.bot.get_channel(payload.channel_id)
        if not channel or channel.id == self.starboard_channel_id:
            return

        try:
            message = await channel.fetch_message(payload.message_id)
        except discord.NotFound:
            return

        star_count = 0
        for reaction in message.reactions:
            if str(reaction.emoji) == self.star_emoji:
                star_count = reaction.count
                break

        if star_count >= self.star_threshold:
            await self.post_to_starboard(message, star_count)
        else:
            await self.remove_from_starboard(message)

    async def post_to_starboard(self, message: discord.Message, star_count: int):
        starboard_channel = self.bot.get_channel(self.starboard_channel_id)
        if not starboard_channel:
            return

        embed = discord.Embed(
            description=message.content,
            color=discord.Color.gold(),
            timestamp=message.created_at
        )

        embed.set_author(
            name=f"{message.author.display_name}",
            icon_url=message.author.display_avatar.url
            )
        embed.set_footer(text=f"ID: {message.id}")
        embed.add_field(
            name="Original",
            value=f"[Jump to Message]({message.jump_url})",
            inline=False
            )

        image_set = False
        if message.attachments:
            for attachment in message.attachments:
                if not image_set and attachment.content_type and attachment.content_type.startswith('image/'):
                    embed.set_image(url=attachment.url)
                    image_set = True
                else:
                    # Add a field for other attachments or subsequent images
                    embed.add_field(name="Attachment", value=f"[{attachment.filename}]({attachment.url})", inline=False)

        content = f"{self.star_emoji} **{star_count}** | {message.channel.mention}"

        message_id_str = str(message.id)
        if message_id_str in self.starboard_messages:
            starboard_message_id = self.starboard_messages[message_id_str]
            try:
                starboard_message = await starboard_channel.fetch_message(starboard_message_id)
                await starboard_message.edit(content=content, embed=embed)
            except discord.NotFound:
                new_starboard_message = await starboard_channel.send(content=content, embed=embed)
                self.starboard_messages[message_id_str] = new_starboard_message.id
                self.save_starboard_messages()
        else:
            new_starboard_message = await starboard_channel.send(content=content, embed=embed)
            self.starboard_messages[message_id_str] = new_starboard_message.id
            self.save_starboard_messages()

    async def remove_from_starboard(self, message: discord.Message):
        message_id_str = str(message.id)
        if message_id_str not in self.starboard_messages:
            return

        starboard_channel = self.bot.get_channel(self.starboard_channel_id)
        if not starboard_channel:
            return

        try:
            starboard_message_id = self.starboard_messages[message_id_str]
            starboard_message = await starboard_channel.fetch_message(starboard_message_id)
            await starboard_message.delete()
        except discord.NotFound:
            pass
        finally:
            del self.starboard_messages[message_id_str]
            self.save_starboard_messages()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Starboard(bot))
