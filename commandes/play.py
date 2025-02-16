import discord
from discord.ext import commands
import yt_dlp
import urllib.parse
import urllib.request
import re
import asyncio

class Play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}
        self.voice_clients = {}
        self.youtube_base_url = 'https://www.youtube.com/'
        self.youtube_results_url = self.youtube_base_url + 'results?'
        self.youtube_watch_url = self.youtube_base_url + 'watch?v='
        #self.yt_dl_options = {"format": "bestaudio/best"}
        self.yt_dl_options = {
            "format": "bestaudio/best",
            "noplaylist": True,
            "quiet": True,
            "extractaudio": True,
            "nocheckcertificate": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        }
        self.current_track = {}
        self.ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn -filter:a "volume=0.25"'}

    @discord.app_commands.command(name="play", description="joue ou ajoute a la file un son depuis Youtube")
    async def play(self, interaction: discord.Interaction, link: str = None):
        await interaction.response.defer()

        guild_id = interaction.guild.id
        if guild_id not in self.queues:
            self.queues[guild_id] = []

        voice_client = self.voice_clients.get(guild_id)

        if link is None:
            if self.queues[guild_id]:
                await self.play_from_queue(interaction, guild_id)
            else:
                await interaction.followup.send("The queue is empty and no link was provided.", ephemeral=True)
            return

        if "www.youtube.com" not in link:
            query_string = urllib.parse.urlencode({'search_query': link})
            try:
                with urllib.request.urlopen(self.youtube_results_url + query_string) as response:
                    content = response.read().decode('utf-8')
                search_results = re.findall(r'/watch\?v=(.{11})', content)
                if not search_results or len(search_results[0]) != 11:
                    await interaction.followup.send("Aucun résultat valide trouvé.", ephemeral=True)
                    return
                # if not search_results:
                #     await interaction.followup.send("Auccun résultat trouvé.", ephemeral=True)
                #     return
                link = self.youtube_watch_url + search_results[0]
            except Exception as e:
                await interaction.followup.send(f"Error retrieving YouTube URL: {e}", ephemeral=True)
                return

        try:
            with yt_dlp.YoutubeDL(self.yt_dl_options) as ydl:
                video_data = ydl.extract_info(link, download=False)
                video_title = video_data.get('title', 'Title unavailable')
        except Exception as e:
            await interaction.followup.send("Failed to retrieve video information.", ephemeral=True)
            return

        queue_item = {'url': link, 'title': video_title}
        self.queues[guild_id].append(queue_item)
        await interaction.followup.send(f"Ajouté a la file: {video_title}", ephemeral=True)

        if not voice_client or not voice_client.is_playing():
            await self.play_from_queue(interaction, guild_id)
        else:
            await interaction.followup.send(f"{video_title} sera jouer bientot.", ephemeral=True)

    async def play_from_queue(self, interaction, guild_id):
        if not self.queues[guild_id]:
            await interaction.followup.send("La file est vide.", ephemeral=True)
            if guild_id in self.current_track:
                del self.current_track[guild_id]  # Effacez le track en cours si la file est vide
                #await self.voice_clients[guild_id].disconnect()
            return

        queue_item = self.queues[guild_id].pop(0)
        self.current_track[guild_id] = queue_item # Mettre à jour le track en cours
        title = queue_item['title']
        link = queue_item['url']

        voice_channel = interaction.user.voice.channel
        if voice_channel and (not self.voice_clients.get(guild_id) or not self.voice_clients[guild_id].is_connected()):
            self.voice_clients[guild_id] = await voice_channel.connect()
            print("bot connecter au vocal")
        with yt_dlp.YoutubeDL(self.yt_dl_options) as ydl:
            video_data = ydl.extract_info(link, download=False)
            song_url = video_data['url']
        player = discord.FFmpegOpusAudio(song_url, **self.ffmpeg_options)
        print("lancement de", title)
        #self.voice_clients[guild_id].play(player, after=lambda e: self.bot.loop.create_task(self.play_from_queue(interaction, guild_id)))
        self.voice_clients[guild_id].play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_from_queue(interaction, guild_id), self.bot.loop))

        await interaction.followup.send(f"joue maintenant: {title}")

async def setup(bot):
    await bot.add_cog(Play(bot))