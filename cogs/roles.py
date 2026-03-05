import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import utils
from utils import NoManageRoles

class Roles(commands.GroupCog, name = "roles"):
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

            await interaction.edit_original_response(
                content=f"The role {role.mention} has been created and assigned to you!")
        except ValueError:
            await interaction.edit_original_response(
                content="Invalid colour format. Please use a hex code (`#FFFFFF`).")

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

            await interaction.edit_original_response(
                content = "You have the permission to do that.")

        except NoManageRoles as error:
            await interaction.edit_original_response(content = str(error))

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
        special_server_roles = ''
        admin_server_roles = ''
        special_role_members = 0

        total_valid_roles = 0
        bot_roles = 0

        for role in fetch_roles:
            if role.is_default():
                pass
            elif role.is_bot_managed():
                bot_roles += 1
            elif role.permissions.kick_members:
                admin_server_roles += f"{role.mention}\n> {len(role.members)} Members have it\n"
                total_valid_roles += 1
            elif not role.managed:
                special_server_roles += f"{role.mention} "
                special_role_members += len(role.members)
                total_valid_roles += 1
            else:
                server_roles += f"{role.mention}\n> {len(role.members)} Members have it\n"
                server_roles += "-# Get one for yourself using Linked Roles!\n\n"
                total_valid_roles += 1

        await asyncio.sleep(1)

        server_roles += admin_server_roles
        server_roles += "-# Be cool with everyone! (to get these)"
        server_roles += "\n"

        await interaction.edit_original_response(content=None, embed=discord.Embed(
            title=f"{interaction.guild.name} Roles: {total_valid_roles}",
            description=f"{server_roles}\n"+
            "==== Special Roles! ==== \n"+
            f"{special_server_roles}\n"+
            "========================\n"+
            "-# Use </roles add:1467783938067005744>\n\n"+
            f"Bot Managed Roles: {bot_roles}"
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
    await bot.add_cog(Roles(bot))
