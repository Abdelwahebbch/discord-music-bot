# NAYZEK-X : 🎵 Discord Music AI Bot

A modern, feature-rich Discord bot built with **discord.py v2**, **Wavelink (Lavalink)** for audio streaming, **Google Gemini AI** for intelligent interactions, and **Pillow** for automated dynamic welcome cards.

---

## 🌟 Key Features

* 🎶 **High-Quality Audio Playback**: Stream music using Lavalink & Wavelink.
* 🤖 **AI-Driven Actions**: Execute commands and play music via natural prompt processing powered by Gemini AI.
* ⚡ **Slash Commands**: Modern Discord interface (`/play`, `/pause`, `/resume`, `/stop`, `/leave`).
* 🎨 **Dynamic Welcome Cards**: Automatically generate and send custom welcome images upon user join events.
* 🐳 **Docker-Ready**: Fully containerized using `Docker` and `docker-compose`.

---

## 📂 Project Structure

```text
├── bot/
│   ├── main.py              # Bot entry point and command tree sync
│   ├── cogs/
│   │   ├── music.py         # Wavelink audio player cog
│   │   └── welcome.py       # Dynamic welcome card event listener
│   └── IA/
│       ├── aiActions.py     # AI action router and command parser
│       └── gemini.py        # Gemini API client integration
├── assets/
│   ├── background.png       # Welcome card template (800x300)
│   └── font.ttf             # Custom font file
├── Dockerfile               # Container build instructions
├── docker-compose.yml       # Docker deployment configuration
├── requirements.txt         # Python dependencies
└── README.md
