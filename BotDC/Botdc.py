import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

class CodCalculator(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.load_extension("cogs.menu_ui")
        await self.load_extension("cogs.tratados_cog")
        await self.tree.sync()
        print("✅ Cogs carregadas")

    async def on_ready(self):
        print(f"🤖 {self.user} está ONLINE")

bot = CodCalculator()
bot.run(TOKEN)
