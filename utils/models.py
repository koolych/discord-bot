import utils
import discord
from discord.ext import commands

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.presences = True
        intents.members = True
        intents.guilds = True
        intents.reactions = True
        intents.message_content = True

        super().__init__(
            command_prefix = "/", 
            intents = intents)
    
    async def setup_hook(self):
        cog_count = 0
        for file in utils.Cogs.get():
            if file.is_dir():
                continue
            
            extension = f"cogs.{file.stem}"
            await self.load_extension(extension)
            print(f"Loaded \"{extension}\"!")
            cog_count += 1

        if cog_count == 0:
            print("No loaded cogs.")

    async def on_message(self, message):
        if message.author.bot:
            return

    async def on_ready(self):
        await self.tree.sync()
        await self.tree.sync(guild=discord.Object(1465563872458047653))
        print(f"Proudly presented to you by Discord.py {discord.__version__}\nBot: {self.user}\nID: {self.user.id}")
        if self.user.avatar:
            utils.bot_avatar = self.user.avatar.url
        
        await self.change_presence(
            activity = discord.Activity(
                name=f"{len(self.guilds)} Servers",
                type=discord.ActivityType.listening),
            status = discord.Status.online
        )

class Buttons(discord.ui.view):
    role = discord.Object
    def __init__(self, *, timeout=30, role: discord.Role):
        self.role = role
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Get Role!",style=discord.ButtonStyle.primary)
    async def add_sub_roles(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await interaction.user.add_roles(self.role)
        await interaction.response.send_message(
            ephemeral=True,
            content=f"Added {self.role.mention} to you!\nYou are now subscribed to this channel.")