import discord
from discord.ext import commands
from discord import app_commands


class MenuSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Tratados",
                description="Calcular tratados até o Farol 25",
                emoji="📜",
                value="tratados"
            ),
            discord.SelectOption(
                label="Honra",
                description="Em breve",
                emoji="🏅",
                value="honra"
            ),
            discord.SelectOption(
                label="Flechas",
                description="Calcular Flechas",
                emoji="🏹",
                value="flechas"
            ),
        ]

        super().__init__(
            placeholder="Selecione o que deseja calcular...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        escolha = self.values[0]

        if escolha == "tratados":
            cog = interaction.client.get_cog("TratadosCog")

        elif escolha == "flechas":
            cog = interaction.client.get_cog("FlechasCog")

        elif escolha == "honra":
            cog = interaction.client.get_cog("HonraCog")

        else:
            cog = None

        if cog is None:
            await interaction.response.send_message(
                "❌ Sistema não disponível.",
                ephemeral=True
            )
            return

        
        await cog.iniciar(interaction)

class MenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        self.add_item(MenuSelect())

class MenuCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="menu", description="Abrir menu de cálculos")
    async def menu(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "📊 **Escolha o que deseja calcular:**",
            view=MenuView(),
            ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(MenuCog(bot))
