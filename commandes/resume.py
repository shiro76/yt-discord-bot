import discord
from discord.ext import commands

class Resume(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="resume", description="Reprend la lecture de la musique mise en pause")
    async def resume(self, interaction: discord.Interaction):
        await interaction.response.defer()  # Prépare la réponse pour des opérations potentiellement longues
        guild_id = interaction.guild.id
        
        # Obtention du cog de lecture pour accéder aux clients vocaux
        play_cog = self.bot.get_cog('Play')
        if not play_cog:
            await interaction.followup.send("Le module de lecture n'est pas chargé.")
            return

        # Vérification si un client vocal est connecté et en pause
        voice_client = play_cog.voice_clients.get(guild_id)
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await interaction.followup.send("La musique a été reprise.")
        else:
            if voice_client and voice_client.is_playing():
                await interaction.followup.send("La musique est déjà en cours de lecture.")
            else:
                await interaction.followup.send("Aucune musique n'est en pause actuellement ou le bot n'est pas connecté à un canal vocal.")

async def setup(bot):
    await bot.add_cog(Resume(bot))
