import discord
from discord.ext import commands
from discord import app_commands

class SlashsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="tratados", description="Calcular tratados até Farol 25")
    async def tratados(self, interaction: discord.Interaction):
        await interaction.response.send_message("📜 Calculadora de tratados")

    @app_commands.command(name="flechas", description="Calcular flechas necessárias")
    async def flechas(self, interaction: discord.Interaction):
        await interaction.response.send_message("🏹 Calculadora de flechas")

async def setup(bot):
    await bot.add_cog(SlashsCog(bot))
