import discord
from discord import app_commands
from discord.ext import commands

class PerfilCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ship", description="Shippa duas pessoas 💕")
    async def ship(self, interaction: discord.Interaction, user1: discord.User, user2: discord.User):
        await interaction.response.send_message(
            f"💖 {user1.mention} combina com {user2.mention}!"
        )

async def setup(bot):
    await bot.add_cog(PerfilCog(bot))
