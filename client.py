import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

EXTENSIONS = [
    "commandes.next",
    "commandes.pause",
    "commandes.play",
    "commandes.playlist",
    "commandes.resume",
    "commandes.stop",
]

class MonBot(commands.Bot):
    async def setup_hook(self):
        for ext in EXTENSIONS:
            await self.load_extension(ext)
            print(f'Chargement réussi {ext}')
        await self.tree.sync()
        print('Slash commands synchro !')

bot = MonBot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user} connecté ! (ID: {bot.user.id})')

bot.run(TOKEN)