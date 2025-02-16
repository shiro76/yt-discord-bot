import discord
from discord.ext import commands

class Playlist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="playlist", description="Affiche la playlist actuelle")
    @discord.app_commands.describe(page="Numéro de la page de la playlist à afficher")
    async def playlist(self, interaction: discord.Interaction, page: int = 1):
        guild_id = interaction.guild.id

        # Supposons que tu as un cog 'Play' qui gère les queues et les tracks en cours
        play_cog = self.bot.get_cog('Play')
        if not play_cog:
            await interaction.response.send_message("Le module de lecture n'est pas chargé.")
            return

        queue = play_cog.queues.get(guild_id, [])
        current_track = play_cog.current_track

        if not queue and guild_id not in current_track:
            await interaction.response.send_message("Aucune musique en cours et la file d'attente est vide.", ephemeral=True)
            return

        message = "Playlist:\n"

        # Ajouter la piste en cours à la liste
        if guild_id in current_track:
            current = current_track[guild_id]
            message += f"En cours : {current['title']} (URL: {current['url']})\n"

        # Pagination pour la file d'attente
        items_per_page = 10
        pages = (len(queue) + items_per_page - 1) // items_per_page
        page = max(1, min(page, pages))
        start = (page - 1) * items_per_page
        end = start + items_per_page

        # Ajouter les éléments de la file à la liste
        for index, item in enumerate(queue[start:end], start=start + 1):
            message += f"{index}. {item['title']}\n"

        await interaction.response.send_message(message)

async def setup(bot):
    await bot.add_cog(Playlist(bot))
