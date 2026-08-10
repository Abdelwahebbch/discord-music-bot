from google.genai import types


TOOLS = [
    types.FunctionDeclaration(
        name="play_music",
        description="Search YouTube for a song/video and play it in the user's current voice channel. Adds to queue if something is already playing.",
        parameters={
            "type": "OBJECT",
            "properties": {
                "query": {
                    "type": "STRING",
                    "description": "Song name, artist, or search terms, e.g. 'Bohemian Rhapsody Queen'",
                }
            },
            "required": ["query"],
        },
    ),
    types.FunctionDeclaration(
        name="skip_music",
        description="Skip the currently playing song and move to the next one in the queue.",
        parameters={"type": "OBJECT", "properties": {}},
    ),
    types.FunctionDeclaration(
        name="pause_music",
        description="Pause the currently playing song.",
        parameters={"type": "OBJECT", "properties": {}},
    ),
    types.FunctionDeclaration(
        name="resume_music",
        description="Resume a paused song.",
        parameters={"type": "OBJECT", "properties": {}},
    ),
    types.FunctionDeclaration(
        name="stop_music",
        description="Stop playback, clear the queue, and leave the voice channel.",
        parameters={"type": "OBJECT", "properties": {}},
    ),
]

SYSTEM_INSTRUCTION = (
    "You are a helpful Discord bot assistant Your owner is Abdelwaheb Bouchahwa. If the user's message asks you to "
    "play, pause, resume, skip, or stop music, call the matching tool. "
    "Otherwise, just reply conversationally in plain text. Keep replies short."
    "Always respond in the Tunisian Arabic dialect (Derja) unless the user explicitly asks you to use another language."
)
