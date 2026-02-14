import discord
from discord.ext import commands
import math


HONRA_POR_NIVEL = {
    8: 35_000,
    9: 75_000,
    10: 150_000,
    11: 250_000,
    12: 350_000,
    13: 500_000,
    14: 750_000,
    15: 1_000_000
}

HONRA_POR_DIA = 400  


def formatar(numero):
    return f"{numero:,}".replace(",", ".")

# ---------- MODAL ----------
class HonraModal(discord.ui.Modal, title="🏅 Cálculo de Honra VIP"):

    honra_atual = discord.ui.TextInput(
        label="Quanta honra você tem?",
        placeholder="Ex: 120000",
        required=True
    )

    nivel_desejado = discord.ui.TextInput(
        label="Qual VIP você quer alcançar? (8 a 15)",
        placeholder="Ex: 14",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        cog = interaction.client.get_cog("HonraCog")

        await cog.calcular_honra(
            interaction,
            int(self.honra_atual.value),
            int(self.nivel_desejado.value)
        )


class HonraCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def iniciar(self, interaction: discord.Interaction):
        await interaction.response.send_modal(HonraModal())

    async def calcular_honra(
        self,
        interaction: discord.Interaction,
        honra_atual: int,
        nivel_desejado: int
    ):

        if nivel_desejado not in HONRA_POR_NIVEL:
            await interaction.response.send_message(
                "❌ VIP inválido. Escolha entre 8 e 15.",
                ephemeral=True
            )
            return

        honra_necessaria = HONRA_POR_NIVEL[nivel_desejado]
        falta = max(honra_necessaria - honra_atual, 0)

        dias = math.ceil(falta / HONRA_POR_DIA)
        meses = dias / 30
        anos = meses / 12

        embed = discord.Embed(
            title="🏅 Resultado - Honra VIP",
            color=discord.Color.purple()
        )

        embed.add_field(
            name="📊 Situação",
            value=(
                f"🎒 Honra atual: **{formatar(honra_atual)}**\n"
                f"🎯 VIP {nivel_desejado} precisa: **{formatar(honra_necessaria)}**\n"
                f"❗ Falta: **{formatar(falta)}**"
            ),
            inline=False
        )

        embed.add_field(
            name="⏱️ Tempo estimado (400 por dia)",
            value=(
                f"📅 {dias} dias\n"
                f"🗓️ {meses:.1f} meses\n"
                f"🕰️ {anos:.2f} anos"
            ),
            inline=False
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(HonraCog(bot))
