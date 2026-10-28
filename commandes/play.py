import asyncio
import subprocess
import sys

import discord
from discord.ext import commands
import yt_dlp


class Play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}
        self.voice_clients = {}
        self.current_track = {}
        self.yt_dl_options = {
            "format": "bestaudio/best",
            "noplaylist": True,
            "quiet": True,
        }

    def extract(self, query):
        """Récupère uniquement les infos (titre, URL de la page)."""
        with yt_dlp.YoutubeDL(self.yt_dl_options) as ydl:
            info = ydl.extract_info(query, download=False)
        if "entries" in info:  # résultat de recherche
            if not info["entries"]:
                raise ValueError("Aucun résultat")
            info = info["entries"][0]
        return info

    def make_source(self, url):
        """yt-dlp télécharge et envoie le flux à FFmpeg par pipe."""
        proc = subprocess.Popen(
            [sys.executable, "-m", "yt_dlp", "-f", "bestaudio",
             "--no-playlist", "-q", "-o", "-", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,  # mets sys.stderr pour déboguer
        )
        player = discord.FFmpegOpusAudio(
            proc.stdout,
            pipe=True,
            executable=r"C:\ffmpeg\bin\ffmpeg.exe",
            options='-vn -filter:a "volume=0.25"',
        )
        return player, proc

    def make_embed(self, item, header):
        embed = discord.Embed(
            title=item['title'],
            url=item['url'],
            description=header,
            color=discord.Color.red(),
        )
        if item.get('thumbnail'):
            embed.set_image(url=item['thumbnail'])  # set_thumbnail pour une petite image
        if item.get('duration'):
            m, s = divmod(int(item['duration']), 60)
            embed.set_footer(text=f"Durée : {m}:{s:02d}")
        return embed

    async def notify(self, interaction, message=None, embed=None):
        """Envoie dans le salon, sinon via followup, sinon affiche en console."""
        try:
            await interaction.channel.send(content=message, embed=embed)
        except discord.HTTPException:
            try:
                await interaction.followup.send(content=message, embed=embed)
            except discord.HTTPException:
                print(f"Impossible d'envoyer : {message or (embed.title if embed else '')}")

    @discord.app_commands.command(name="play", description="joue ou ajoute a la file un son depuis Youtube")
    async def play(self, interaction: discord.Interaction, link: str = None):
        await interaction.response.defer()
        guild_id = interaction.guild.id
        self.queues.setdefault(guild_id, [])

        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.followup.send("Tu dois être dans un salon vocal.", ephemeral=True)
            return

        voice_client = self.voice_clients.get(guild_id)
        busy = voice_client and (voice_client.is_playing() or voice_client.is_paused())

        if link is None:
            if self.queues[guild_id] and not busy:
                await self.play_from_queue(interaction, guild_id)
            else:
                await interaction.followup.send("File vide ou lecture déjà en cours.", ephemeral=True)
            return

        query = link if link.startswith(("http://", "https://")) else f"ytsearch1:{link}"
        try:
            info = await asyncio.to_thread(self.extract, query)
        except Exception as e:
            print(f"Erreur yt-dlp (recherche): {e}")
            await interaction.followup.send("Impossible de récupérer la vidéo.", ephemeral=True)
            return

        item = {
            'url': info.get("webpage_url", link),
            'title': info.get("title", "Titre indisponible"),
            'thumbnail': info.get("thumbnail"),
            'duration': info.get("duration"),
        }
        self.queues[guild_id].append(item)
        await interaction.followup.send(
            embed=self.make_embed(item, "Ajouté à la file"),
            ephemeral=True,
        )

        if not busy:
            await self.play_from_queue(interaction, guild_id)

    async def play_from_queue(self, interaction, guild_id):
        if not self.queues[guild_id]:
            self.current_track.pop(guild_id, None)
            await self.notify(interaction, "La file est vide.")
            vc = self.voice_clients.pop(guild_id, None)
            if vc and vc.is_connected():
                await vc.disconnect()
            return

        vc = self.voice_clients.get(guild_id)
        if not vc or not vc.is_connected():
            voice = interaction.user.voice
            if not voice or not voice.channel:
                await self.notify(interaction, "Je ne sais pas quel salon vocal rejoindre.")
                return
            vc = await voice.channel.connect()
            self.voice_clients[guild_id] = vc

        item = self.queues[guild_id].pop(0)
        self.current_track[guild_id] = item

        player, proc = self.make_source(item['url'])
        # Attend le premier paquet audio avant de lancer la lecture
        first = await asyncio.to_thread(player.read)
        if not first:
            proc.kill()
            await self.notify(interaction, f"Impossible de lire {item['title']}, je passe au suivant.")
            return await self.play_from_queue(interaction, guild_id)

        def after(error):
            if error:
                print(f"Erreur de lecture: {error}")
            proc.kill()
            asyncio.run_coroutine_threadsafe(
                self.play_from_queue(interaction, guild_id), self.bot.loop
            )

        vc.play(player, after=after)
        await self.notify(interaction, embed=self.make_embed(item, "Joue maintenant"))


async def setup(bot):
    await bot.add_cog(Play(bot))
