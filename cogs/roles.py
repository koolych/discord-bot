import asyncio
import utils
from utils import NoManageRoles, MayDoSo
import discord
from discord import app_commands
from discord.ext import commands

class roles(commands.GroupCog, name = "roles"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.config = utils.Config.read()
    
    @app_commands.command(
        name = "add",
        description = "Give out a custom role for yourself."
    )
    async def add(
        self,
        interaction: discord.Interaction,
        name: str,
        colour: str
    ):
        await interaction.response.defer(thinking=True)
        try:
            colour_obj = discord.Colour.from_str(colour)

            role = await interaction.guild.create_role(
                name=name,
                colour=colour_obj,
                reason=f"{interaction.user.name} asked me to",
                permissions=discord.Permissions.none())
            await interaction.user.add_roles(role)

            

            await interaction.edit_original_response(content=f"The role {role.mention} has been created and assigned to you!")
        except ValueError:
            await interaction.edit_original_response(content="Invalid colour format. Please use a hex code (e.g., `#FF5733` or `FF5733`).")

    @app_commands.command(
            name = "assign",
            description = "Add a role to the list (Admin)"
    )
    async def assign(
        self,
        interaction: discord.Interaction,
        role: discord.Role
    ):
        await interaction.response.send_message(content = "Thinking")
        try:
            if interaction.guild.owner.id == interaction.user.id:
                pass
            elif interaction.user.guild_permissions.manage_roles:
                raise NoManageRoles()
            
            await interaction.edit_original_response(content = "You have the permission to do that.")

        except Exception as error:
            await interaction.edit_original_response(content = error.__str__())

    @app_commands.command(
            name = "list",
            description = "Lists the roles?"
    )
    async def list(
            self,
            interaction: discord.Interaction
    ):
        await interaction.response.send_message(content = "Listing...", embed=discord.Embed(
            title="Loading..."
        ))
        fetch_roles = await interaction.guild.fetch_roles()
        server_roles = ''
        total_valid_roles = 0
        bot_roles = 0
        for role in fetch_roles:
            if role.is_default():
                pass
            elif role.is_bot_managed():
                bot_roles += 1
            elif not(role.managed):
                server_roles += f"{role.mention}\n> {role.members.__len__()} Members have it\n"
                total_valid_roles += 1
            else:
                server_roles += f"{role.mention}\n> {role.members.__len__()} Members have it\n"
                server_roles += "-# Get one for yourself using Linked Roles!"
                total_valid_roles += 1
            server_roles += "\n"

        await asyncio.sleep(1)

        await interaction.edit_original_response(content=None, embed=discord.Embed(
            title=f"{interaction.guild.name} Roles: {total_valid_roles}",
            description=f"{server_roles}\nBot Managed Roles: {bot_roles}"
        ))

    @app_commands.describe(
        role = "Select a role"
    )
    @app_commands.command(
        name = "pick",
        description = "Pick a role of your liking!"
    )
    async def pick(
        self,
        interaction: discord.Interaction,
        role: discord.Role
    ):
        await interaction.response.send_message(content = "Test")
    
    @app_commands.command(
        name = "remove",
        description = "Remove a role"
    )
    async def remove(
        self,
        interaction: discord.Interaction,
        role: discord.Role = None
    ):
        await interaction.response.send_message(content = "Test")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(roles(bot))