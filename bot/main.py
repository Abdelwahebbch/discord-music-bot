import os
import logging

import discord
import wavelink
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
LAVALINK_HOST = os.getenv("LAVALINK_HOST", "localhost")
LAVALINK_PORT = int(os.getenv("LAVALINK_PORT", "2333"))
LAVALINK_PASSWORD = os.getenv("LAVALINK_PASSWORD")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


class MusicBot(commands.Bot):

    def __init__(self):
        intents = discord.Intents.default()

        super().__init__(
            command_prefix="!",
            intents=intents,
        )

    async def setup_hook(self):
        node = wavelink.Node(
            uri=f"http://{LAVALINK_HOST}:{LAVALINK_PORT}",
            password=LAVALINK_PASSWORD,
        )

        await wavelink.Pool.connect(
            nodes=[node],
            client=self,
            cache_capacity=100,
        )

        await self.load_extension("bot.music")

        await self.tree.sync()

        logging.info("Slash commands synchronized.")

    async def on_ready(self):
        logging.info(
            "Logged in as %s (%s)",
            self.user,
            self.user.id,
        )


bot = MusicBot()


if __name__ == "__main__":
    bot.run(TOKEN)