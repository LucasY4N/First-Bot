import discord
from discord.ext import commands
import math

FLECHAS_POR_NIVEL = {
    20: 1750,
    21: 2000,
    22: 2500,
    23: 3000,
    24: 5000
}

FLECHAS_POR_OBSCURO = 2
FLECHAS_POR_VIP = 50


class FlechasModal(discord.ui.Modal, title="🏹 Cálculo de Flechas"):
    flechas_atual = discord.ui.TextInput(
        label="Quantas flechas você tem?",
        placeholder="Ex: 500",
        required=True
    )

    nivel_farol = discord.ui.TextInput(
        label="Qual o level atual da sua Torre?",
        placeholder="Ex: 20",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            flechas = int(self.flechas_atual.value)
            nivel = int(self.nivel_farol.value)
        except ValueError:
            await interaction.response.send_message(
                "❌ Use apenas números.",
                ephemeral=True
            )
            return

        cog = interaction.client.get_cog("FlechasCog")

        if cog is None:
            await interaction.response.send_message(
                "❌ Cog de Flechas não carregada.",
                ephemeral=True
            )
            return


        await interaction.response.defer(ephemeral=True)

        await cog.calcular_flechas(
            interaction,
            flechas,
            nivel
        )

class FlechasCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def iniciar(self, interaction: discord.Interaction):
        await interaction.response.send_modal(FlechasModal())

    async def calcular_flechas(
        self,
        interaction: discord.Interaction,
        flechas_atual: int,
        nivel_atual: int,
        nivel_final: int = 25
    ):
        total_necessario = 0
        detalhes = []

        for nivel in range(nivel_atual, nivel_final):
            valor = FLECHAS_POR_NIVEL.get(nivel)
            if not valor:
                continue
            total_necessario += valor
            detalhes.append(f"🔹 {nivel} → {nivel+1}: **{valor:,}**")

        faltando = max(total_necessario - flechas_atual, 0)

        flechas_4 = FLECHAS_POR_OBSCURO * 4
        flechas_5 = FLECHAS_POR_OBSCURO * 5

        obscuros_4 = math.ceil(faltando / flechas_4)
        obscuros_5 = math.ceil(faltando / flechas_5)

        total_4 = obscuros_4 * flechas_4 + FLECHAS_POR_VIP
        total_5 = obscuros_5 * flechas_5 + FLECHAS_POR_VIP

        melhor = "5 marchas 🏆" if total_5 >= total_4 else "4 marchas 🏆"

        embed = discord.Embed(
            title="🏹 Resultado - Flechas",
            color=discord.Color.gold()
        )

        embed.add_field(
            name="📈 Flechas por nível",
            value="\n".join(detalhes),
            inline=False
        )

        embed.add_field(
            name="📊 Situação",
            value=(
                f"🎒 Flechas atuais: **{flechas_atual:,}**\n"
                f"❗ Falta: **{faltando:,}**"
            ),
            inline=False
        )

        embed.add_field(
            name="⚔️ 4 marchas",
            value=(
                f"👁️ Obscuros: **{obscuros_4:,}**\n"
                f"🏹 Flechas finais: **{total_4:,}**"
            ),
            inline=True
        )

        embed.add_field(
            name="🔥 5 marchas",
            value=(
                f"👁️ Obscuros: **{obscuros_5:,}**\n"
                f"🏹 Flechas finais: **{total_5:,}**"
            ),
            inline=True
        )

        embed.add_field(
            name="✅ Melhor opção",
            value=melhor,
            inline=False
        )

        embed.set_footer(text="Inclui +50 flechas semanais do VIP")


        await interaction.followup.send(
            embed=embed,
            ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(FlechasCog(bot))
