import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import bot
from google import genai
from google.genai import types
from bot.IA.Tools import TOOLS, SYSTEM_INSTRUCTION

gemini = genai.Client()

async def ask_gemini(prompt: str):
    response = await asyncio.to_thread(
        gemini.models.generate_content,
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(function_declarations=TOOLS)],
            system_instruction=SYSTEM_INSTRUCTION,
        ),
    )
    return response

async def execute_action(b : commands.Bot ,name:str , args:dict ,message:discord.Message)-> str:
    music_cog =  b.get_cog("Music")
    if not music_cog:
        return "❌ Music cog is not loaded."

    guild = message.guild
    user_voice = message.author.voice.channel if (message.author and message.author.voice) else None

    if name == "play_music":
        query = args.get("query", "")
        return await music_cog.play_track(guild, user_voice, query)

    if name == "pause_music":
        return await music_cog.pause_track(guild)

    if name == "resume_music":
        return await music_cog.resume_track(guild)

    if name == "stop_music":
        return await music_cog.stop_track(guild)

    if name == "leave_music":
        return await music_cog.leave_channel(guild)

    return "❌ Unknown action."
