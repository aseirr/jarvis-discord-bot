import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from commands.ask import ask_jarvis
from commands.memory import remember, recall
from keep_alive import keep_alive
from commands.conversation_memory import (
    add_message,
    get_history,
    clear_chat,
    remember_fact
)

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# Channels where Jarvis is "awake"
active_channels = set()


# ---------------- READY EVENT ----------------
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"Sync Error: {e}")

    print(f"Logged in as {bot.user}")


# ---------------- MESSAGE LISTENER ----------------
@bot.event
async def on_message(message):

    if message.author.bot:
        return

    content = message.content.strip()
    content_lower = content.lower()

    channel_id = message.channel.id
    user_id = message.author.id

    # ---------------- WAKE UP ----------------
    if content_lower == "wake up jarvis":

        active_channels.add(channel_id)

        await message.reply(
            "🟢 Jarvis activated. I'm listening."
        )
        return

    # ---------------- SLEEP ----------------
    if content_lower == "exit jarvis":

        active_channels.discard(channel_id)

        await message.reply(
            "🔴 Jarvis deactivated."
        )
        return

    triggered = False
    user_message = content

    # Jarvis already active in this channel
    if channel_id in active_channels:
        triggered = True

    # Mention "jarvis" anywhere
    elif "jarvis" in content_lower:
        triggered = True

    # Discord mention
    elif bot.user and bot.user.mentioned_in(message):
        triggered = True

    if triggered:

        msg_lower = user_message.lower()

        # Clear chat
        if "clear chat" in msg_lower:
            clear_chat(channel_id)
            await message.reply("🧹 Chat cleared.")
            return

        # Remember fact
        if "remember this" in msg_lower:
            remember_fact(user_message)
            await message.reply("🧠 Saved to memory.")
            return

        add_message(
            channel_id,
            "user",
            user_message
        )

        history = get_history(channel_id)

        answer = ask_jarvis(
            user_id,
            user_message,
            history
        )

        add_message(
            channel_id,
            "assistant",
            answer
        )

        if len(answer) > 1900:
            answer = answer[:1900] + "\n\n[truncated]"

        await message.reply(answer)

    await bot.process_commands(message)


# ---------------- SLASH: PING ----------------
@bot.tree.command(
    name="ping",
    description="Check if Jarvis is online"
)
async def ping(interaction: discord.Interaction):

    await interaction.response.send_message(
        f"🏓 Pong! {round(bot.latency * 1000)}ms"
    )


# ---------------- SLASH: ASK ----------------
@bot.tree.command(
    name="ask",
    description="Ask Jarvis anything"
)
async def ask(
    interaction: discord.Interaction,
    question: str
):

    await interaction.response.defer()

    channel_id = interaction.channel_id
    user_id = interaction.user.id

    add_message(channel_id, "user", question)

    history = get_history(channel_id)

    answer = ask_jarvis(
        user_id,
        question,
        history
    )

    add_message(
        channel_id,
        "assistant",
        answer
    )

    if len(answer) > 1900:
        answer = answer[:1900] + "\n\n[truncated]"

    await interaction.followup.send(answer)


# ---------------- SLASH: REMEMBER ----------------
@bot.tree.command(
    name="remember",
    description="Store something in Jarvis memory"
)
async def remember_command(
    interaction: discord.Interaction,
    fact: str
):

    remember(fact)

    await interaction.response.send_message(
        f"🧠 Remembered: {fact}"
    )


# ---------------- SLASH: RECALL ----------------
@bot.tree.command(
    name="recall",
    description="View Jarvis memory"
)
async def recall_command(
    interaction: discord.Interaction
):

    memory = recall()

    if not memory:
        await interaction.response.send_message(
            "I don't remember anything yet."
        )
        return

    text = "\n".join(
        f"{i+1}. {item}"
        for i, item in enumerate(memory)
    )

    await interaction.response.send_message(
        f"🧠 Memory:\n\n{text}"
    )


# ---------------- !JARVIS COMMAND ----------------
@bot.command(name="jarvis")
async def jarvis(ctx, *, message: str):

    channel_id = ctx.channel.id
    user_id = ctx.author.id

    add_message(
        channel_id,
        "user",
        message
    )

    history = get_history(channel_id)

    answer = ask_jarvis(
        user_id,
        message,
        history
    )

    add_message(
        channel_id,
        "assistant",
        answer
    )

    if len(answer) > 1900:
        answer = answer[:1900] + "\n\n[truncated]"

    await ctx.send(answer)


# ---------------- RUN BOT ----------------
keep_alive()
bot.run(TOKEN)