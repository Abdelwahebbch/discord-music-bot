import io
import os

import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps


class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.welcome_channel_id = 800062474874781736
        self.left_channel_id = 886725073904472074

    async def generate_welcome_card(self, member: discord.Member) -> discord.File:
        bg_path = "/app/background.png"
        if os.path.exists(bg_path):
            background = Image.open(bg_path).convert("RGBA").resize((800, 300))
        else:
            background = Image.new("RGBA", (800, 300), color=(24, 25, 28, 255))


        draw = ImageDraw.Draw(background)
        avatar_asset = member.display_avatar.with_size(256)
        avatar_bytes = await avatar_asset.read()
        avatar_img = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")
        avatar_size = (140, 140)
        avatar_img = avatar_img.resize(avatar_size)
        # Create circle mask
        mask = Image.new("L", avatar_size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, avatar_size[0], avatar_size[1]), fill=255)

        # Apply circular mask to avatar
        circular_avatar = ImageOps.fit(avatar_img, avatar_size, centering=(0.5, 0.5))
        circular_avatar.putalpha(mask)

        # --- 3. DRAW AVATAR BORDER RING & PASTE ---
        avatar_pos = (50, 80)
        # Draw accent circle outline around avatar
        draw.ellipse(
            [avatar_pos[0] - 5, avatar_pos[1] - 5, avatar_pos[0] + avatar_size[0] + 5,
             avatar_pos[1] + avatar_size[1] + 5],
            outline=(88, 101, 242, 255),  # Discord Blurple color
            width=5
        )
        background.paste(circular_avatar, avatar_pos, circular_avatar)

        # --- 4. FONTS & TEXT CUSTOMIZATION ---
        font_path = "/app/font.ttf"
        if os.path.exists(font_path):
            font_title = ImageFont.truetype(font_path, 42)
            font_subtitle = ImageFont.truetype(font_path, 26)
        else:
            font_title = ImageFont.load_default()
            font_subtitle = ImageFont.load_default()

        # Render Text Elements
        draw.text((220, 95), f"WELCOME, {member.name}!", fill=(255, 255, 255), font=font_title)
        draw.text((220, 155), f"Member #{member.guild.member_count}", fill=(180, 190, 205), font=font_subtitle)

        # --- 5. EXPORT TO DISCORD FILE ---
        buffer = io.BytesIO()
        background.save(buffer, format="PNG")
        buffer.seek(0)

        return discord.File(buffer, filename="welcome_card.png")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = member.guild.get_channel(self.welcome_channel_id)
        if channel is None or not isinstance(channel, discord.TextChannel):
            return
        welcome_file = await self.generate_welcome_card(member)
        await channel.send(
            content=f"Welcome to the server, {member.mention} !  🎉",
            file=welcome_file
        )

    @commands.Cog.listener()
    async def on_member_remove(self , member :discord.Member):
        channel = member.guild.get_channel(self.left_channel_id)
        if channel is None or not isinstance(channel, discord.TextChannel):
            return
        await channel.send(
            content=f"Barra zammer {member.name} ",
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(Welcome(bot))