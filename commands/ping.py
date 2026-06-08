import discord
from discord import app_commands

def setup(bot):

    @bot.tree.command(
        name="ping",
        description="Check if Jarvis is online"
    )
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message(
            "🏓 Pong!"
        )