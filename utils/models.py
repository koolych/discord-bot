import utils
import discord
from discord.ext import commands

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.presences = True
        intents.members = True
        intents.guilds = True
        intents.message_content = True

        super().__init__(
            command_prefix = "/", 
            intents = intents)
    
    async def setup_hook(self):
        for file in utils.Cogs.get():
            if file.is_dir():
                continue
            
            extension = f"cogs.{file.stem}"
            await self.load_extension(extension)
            print(f"Loaded \"{extension}\"!")
            return
        
        print("No loaded cogs.")
    
    async def on_ready(self):
        await self.tree.sync()
        await self.tree.sync(guild=discord.Object(1465563872458047653))
        print(f"Proudly presented to you by Discord.py {discord.__version__}\nBot: {self.user}\nID: {self.user.id}")
        if self.user.avatar:
            utils.bot_avatar = self.user.avatar.url

