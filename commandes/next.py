import discord
from discord.ext import commands

class Next(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def play_next(self, interaction):
        # Accéder directement aux files d'attente depuis le cog de lecture si disponible
        play_cog = self.bot.get_cog('Play')
        if play_cog and play_cog.queues[interaction.guild.id]:
            link = play_cog.queues[interaction.guild.id].pop(0)
            await play_cog.play_song(interaction, link)

    @discord.app_commands.command(name="next", description="Passer à la chanson suivante")
    async def next(self, interaction: discord.Interaction):
        await interaction.response.defer()

        guild_id = interaction.guild.id
        play_cog = self.bot.get_cog('Play')
        if not play_cog:
            await interaction.followup.send("Le module de lecture n'est pas chargé.")
            return

        voice_client = play_cog.voice_clients.get(guild_id)

        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await interaction.followup.send("Passage à la chanson suivante...")
            await self.play_next(interaction)
        else:
            await interaction.followup.send("Aucune chanson n'est actuellement jouée.")

async def setup(bot):
    await bot.add_cog(Next(bot))
