import discord
from discord.ext import commands
import math

TRATADOS_POR_NIVEL = {
    20: 1750,
    21: 2000,
    22: 2500,
    23: 3000,
    24: 5000
}

TRATADOS_SEMANA = 140
GEMAS_POR_TRATADO = 10

# ---------- MODAL ----------
class TratadosModal(discord.ui.Modal, title="📜 Cálculo de Tratados"):
    tratados_atual = discord.ui.TextInput(
        label="Quantos tratados você tem?",
        placeholder="Ex: 2000",
        required=True
    )

    nivel_farol = discord.ui.TextInput(
        label="Nível atual do Farol (20 a 24)",
        placeholder="Ex: 22",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        cog = interaction.client.get_cog("TratadosCog")

        await cog.calcular_tratados(
            interaction,
            int(self.tratados_atual.value),
            int(self.nivel_farol.value)
        )

# ---------- COG ----------
class TratadosCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def iniciar(self, interaction: discord.Interaction):
        await interaction.response.send_modal(TratadosModal())

    async def calcular_tratados(
        self,
        interaction: discord.Interaction,
        tratados_atual: int,
        nivel_atual: int,
        nivel_final: int = 25
    ):
        total = 0
        detalhes = []

        for nivel in range(nivel_atual, nivel_final):
            valor = TRATADOS_POR_NIVEL.get(nivel)
            if not valor:
                continue
            total += valor
            detalhes.append(f"🔹 {nivel} → {nivel+1}: **{valor:,}**")

        falta = max(total - tratados_atual, 0)
        semanas = math.ceil(falta / TRATADOS_SEMANA)
        meses = semanas / 4.345
        anos = meses / 12
        gemas = falta * GEMAS_POR_TRATADO

        embed = discord.Embed(
            title="📜 Resultado - Tratados",
            color=discord.Color.gold()
        )

        embed.add_field(
            name="📈 Tratados por nível",
            value="\n".join(detalhes),
            inline=False
        )

        embed.add_field(
            name="📊 Situação",
            value=(
                f"🎒 Tratados atuais: **{tratados_atual:,}**\n"
                f"❗ Falta: **{falta:,}**"
            ),
            inline=False
        )

        embed.add_field(
            name="⏱️ Tempo estimado",
            value=(
                f"🗓️ {semanas} semanas\n"
                f"📅 {meses:.1f} meses\n"
                f"🕰️ {anos:.2f} anos"
            ),
            inline=True
        )

        embed.add_field(
            name="💎 Gemas necessárias",
            value=f"**{gemas:,} gemas**",
            inline=True
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(TratadosCog(bot))
