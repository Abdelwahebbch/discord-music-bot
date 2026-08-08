import discord
import wavelink

from discord import app_commands
from discord.ext import commands


class Music(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def get_player(
        self,
        interaction: discord.Interaction,
    ) -> wavelink.Player | None:

        if not interaction.guild:
            return None

        voice_state = interaction.user.voice

        if voice_state is None or voice_state.channel is None:
            await interaction.followup.send(
                "❌ You must join a voice channel first."
            )
            return None

        player = interaction.guild.voice_client

        if player is None:
            player = await voice_state.channel.connect(
                cls=wavelink.Player
            )

        elif player.channel != voice_state.channel:
            await interaction.followup.send(
                "❌ You must be in my current voice channel."
            )
            return None

        return player

    @app_commands.command(
        name="play",
        description="Play a song."
    )
    @app_commands.describe(
        query="Song name or URL"
    )
    async def play(
        self,
        interaction: discord.Interaction,
        query: str,
    ):

        await interaction.response.defer()

        player = await self.get_player(interaction)

        if player is None:
            return

        tracks = await wavelink.Playable.search(query)

        if not tracks:
            await interaction.followup.send(
                "❌ No results found."
            )
            return

        track = tracks[0]

        await player.play(track)

        await interaction.followup.send(
            f"▶️ Now playing: **{track.title}**"
        )

    @app_commands.command(
        name="pause",
        description="Pause the current song."
    )
    async def pause(
        self,
        interaction: discord.Interaction,
    ):

        player = interaction.guild.voice_client

        if not isinstance(player, wavelink.Player):
            await interaction.response.send_message(
                "❌ I'm not playing anything."
            )
            return

        await player.pause(True)

        await interaction.response.send_message(
            "⏸️ Music paused."
        )

    @app_commands.command(
        name="resume",
        description="Resume the current song."
    )
    async def resume(
        self,
        interaction: discord.Interaction,
    ):

        player = interaction.guild.voice_client

        if not isinstance(player, wavelink.Player):
            await interaction.response.send_message(
                "❌ I'm not playing anything."
            )
            return

        await player.pause(False)

        await interaction.response.send_message(
            "▶️ Music resumed."
        )

    @app_commands.command(
        name="stop",
        description="Stop the music."
    )
    async def stop(
        self,
        interaction: discord.Interaction,
    ):

        player = interaction.guild.voice_client

        if not isinstance(player, wavelink.Player):
            await interaction.response.send_message(
                "❌ I'm not playing anything."
            )
            return

        await player.stop()

        await interaction.response.send_message(
            "⏹️ Music stopped."
        )

    @app_commands.command(
        name="leave",
        description="Leave the voice channel."
    )
    async def leave(
        self,
        interaction: discord.Interaction,
    ):

        player = interaction.guild.voice_client

        if player is None:
            await interaction.response.send_message(
                "❌ I'm not in a voice channel."
            )
            return

        await player.disconnect()

        await interaction.response.send_message(
            "👋 Disconnected."
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))