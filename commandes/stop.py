import discord
from discord.ext import commands

class Stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="stop", description="Stop le bot de musique et le deconnecte du vocal")
    async def stop(self, interaction):
        await interaction.response.defer()  # Assure que tu as le temps de répondre à la commande
        guild_id = interaction.guild.id

        play_cog = self.bot.get_cog('Play')
        if not play_cog:
            await interaction.followup.send("Le module de lecture n'est pas chargé.")
            return

        voice_client = play_cog.voice_clients.get(guild_id)
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await voice_client.disconnect()
            del voice_client
            await interaction.followup.send("La musique a été mise en pause.")
        else:
            await interaction.followup.send("Aucune musique n'est actuellement jouée ou le bot n'est pas connecté à un canal vocal.")

async def setup(bot):
    await bot.add_cog(Stop(bot))
