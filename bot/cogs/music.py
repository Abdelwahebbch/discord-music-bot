import discord
import wavelink
from discord import app_commands
from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def get_player(
            self,
            guild: discord.Guild | None,
            voice_channel: discord.VoiceChannel | discord.StageChannel | None,
    ) -> tuple[wavelink.Player | None, str | None]:
        """
        Retrieves or creates a Wavelink player for a given guild and channel.
        Returns a tuple of (Player, error_message).
        """
        if not guild:
            return None, "❌ Commands must be used within a server."

        if not voice_channel:
            return None, "❌ You must join a voice channel first."

        player: wavelink.Player | None = guild.voice_client

        if player is None:
            player = await voice_channel.connect(cls=wavelink.Player)
        elif player.channel != voice_channel:
            return None, "❌ You must be in my current voice channel."

        return player, None

    async def play_track(
            self,
            guild: discord.Guild | None,
            voice_channel: discord.VoiceChannel | discord.StageChannel | None,
            query: str,
    ) -> str:
        player, error = await self.get_player(guild, voice_channel)
        if error or not player:
            return error or "❌ Could not establish voice connection."

        tracks = await wavelink.Playable.search(query)
        if not tracks:
            return "❌ No results found."

        track = tracks[0]
        await player.play(track)
        return f"▶️ Now playing: **{track.title}**"

    async def pause_track(self, guild: discord.Guild | None) -> str:
        if not guild or not isinstance(guild.voice_client, wavelink.Player):
            return "❌ I'm not playing anything."

        player: wavelink.Player = guild.voice_client
        await player.pause(True)
        return "⏸️ Music paused."

    async def resume_track(self, guild: discord.Guild | None) -> str:
        if not guild or not isinstance(guild.voice_client, wavelink.Player):
            return "❌ I'm not playing anything."

        player: wavelink.Player = guild.voice_client
        await player.pause(False)
        return "▶️ Music resumed."

    async def stop_track(self, guild: discord.Guild | None) -> str:
        if not guild or not isinstance(guild.voice_client, wavelink.Player):
            return "❌ I'm not playing anything."

        player: wavelink.Player = guild.voice_client
        await player.stop()
        return "⏹️ Music stopped."

    async def leave_channel(self, guild: discord.Guild | None) -> str:
        if not guild or guild.voice_client is None:
            return "❌ I'm not in a voice channel."

        await guild.voice_client.disconnect()
        return "👋 Disconnected."

    # --- SLASH COMMANDS ---

    @app_commands.command(name="play", description="Play a song.")
    @app_commands.describe(query="Song name or URL")
    async def play(self, interaction: discord.Interaction, query: str):
        await interaction.response.defer()

        user_voice = interaction.user.voice.channel if (interaction.user and interaction.user.voice) else None
        response = await self.play_track(interaction.guild, user_voice, query)

        await interaction.followup.send(response)

    @app_commands.command(name="pause", description="Pause the current song.")
    async def pause(self, interaction: discord.Interaction):
        response = await self.pause_track(interaction.guild)
        await interaction.response.send_message(response)

    @app_commands.command(name="resume", description="Resume the current song.")
    async def resume(self, interaction: discord.Interaction):
        response = await self.resume_track(interaction.guild)
        await interaction.response.send_message(response)

    @app_commands.command(name="stop", description="Stop the music.")
    async def stop(self, interaction: discord.Interaction):
        response = await self.stop_track(interaction.guild)
        await interaction.response.send_message(response)

    @app_commands.command(name="leave", description="Leave the voice channel.")
    async def leave(self, interaction: discord.Interaction):
        response = await self.leave_channel(interaction.guild)
        await interaction.response.send_message(response)


async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))