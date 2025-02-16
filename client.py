import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import commandes.next, commandes.pause, commandes.play, commandes.playlist, commandes.resume, commandes.stop
from commandes.next import Next
from commandes.pause import Pause
from commandes.play import Play
from commandes.playlist import Playlist
from commandes.resume import Resume
from commandes.stop import Stop


intents = discord.Intents().all()
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} Connecté! (ID: {bot.user.id})')
    await load_cogs()
    await bot.tree.sync()
    print('Slash commands syncro!')

extentions = [
    "commandes.next",
    "commandes.pause",
    "commandes.play",
    "commandes.playlist",
    "commandes.resume",
    "commandes.stop"
]

async def load_cogs():
    for ext in extentions:
        await bot.load_extension(f'{ext}')
        print(f'Chargement Reussi {ext}')

bot.run(TOKEN)