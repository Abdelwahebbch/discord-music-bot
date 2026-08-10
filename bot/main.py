import os
import logging
import discord
import wavelink
from discord.ext import commands
from dotenv import load_dotenv
from bot.IA.aiActions import ask_gemini, execute_action

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

        await self.load_extension("bot.cogs.music")

        await self.tree.sync()

        logging.info("Slash commands synchronized.")

    async def on_ready(self):
        logging.info(
            "Logged in as %s (%s)",
            self.user,
            self.user.id,
        )
    async def on_message(self, message: discord.Message, ) :
        if message.author.bot :
            return
        if self.user not in message.mentions and not isinstance(message.channel, discord.DMChannel) :
            return
        content = message.content.replace(f"<@{self.user.id}>", "").strip()
        if not content :
            return
        async with message.channel.typing():
            response = await ask_gemini(content)

            candidate = response.candidates[0]
            function_call = None
            text_reply = None

            for p in candidate.content.parts :
                if getattr(p,"function_call",None):
                    function_call = p.function_call
                elif getattr(p,"text",None):
                    text_reply = p.text
            if function_call :
                result = await execute_action(bot,
                    function_call.name , dict(function_call.args) , message
                )
                await message.channel.send(result)
            elif text_reply :
                await message.channel.send(text_reply)
            else :
                await message.channel.send("Mmmmmmmm ma3endich fekra")



bot = MusicBot()


if __name__ == "__main__":
    bot.run(TOKEN)