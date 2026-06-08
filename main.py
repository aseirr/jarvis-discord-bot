import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from commands.ask import ask_jarvis
from commands.memory import remember, recall
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


# ---------------- READY EVENT ----------------
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"Sync Error: {e}")

    print(f"Logged in as {bot.user}")


# ---------------- SLASH: PING ----------------
@bot.tree.command(name="ping", description="Check if Jarvis is online")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"🏓 Pong! {round(bot.latency * 1000)}ms"
    )


# ---------------- SLASH: ASK (MAIN AI) ----------------
@bot.tree.command(name="ask", description="Ask Jarvis anything")
async def ask(interaction: discord.Interaction, question: str):

    await interaction.response.defer()

    channel_id = interaction.channel_id
    user_id = interaction.user.id

    # save user message
    add_message(channel_id, "user", question)

    # get history
    history = get_history(channel_id)

    # AI response
    answer = ask_jarvis(user_id, question, history)

    # save bot response
    add_message(channel_id, "assistant", answer)

    if len(answer) > 1900:
        answer = answer[:1900] + "\n\n[truncated]"

    await interaction.followup.send(answer)


# ---------------- SLASH: MEMORY ----------------
@bot.tree.command(name="remember", description="Store something in Jarvis memory")
async def remember_command(interaction: discord.Interaction, fact: str):

    remember(fact)

    await interaction.response.send_message(
        f"🧠 Remembered: {fact}"
    )


@bot.tree.command(name="recall", description="View Jarvis memory")
async def recall_command(interaction: discord.Interaction):

    memory = recall()

    if not memory:
        await interaction.response.send_message("I don't remember anything yet.")
        return

    text = "\n".join(f"{i+1}. {item}" for i, item in enumerate(memory))

    await interaction.response.send_message(f"🧠 Memory:\n\n{text}")


# ---------------- NORMAL CHAT COMMAND (ULTRA MODE) ----------------
@bot.command(name="jarvis")
async def jarvis(ctx, *, message: str):

    channel_id = ctx.channel.id
    user_id = ctx.author.id

    msg_lower = message.lower()

    # ---------------- SIMPLE COMMAND DETECTION ----------------
    if "clear chat" in msg_lower:
        clear_chat(channel_id)
        await ctx.send("🧹 Chat cleared.")
        return

    if "remember this" in msg_lower:
        remember_fact(message)
        await ctx.send("🧠 Saved to memory.")
        return

    # ---------------- NORMAL AI FLOW ----------------
    add_message(channel_id, "user", message)

    history = get_history(channel_id)

    answer = ask_jarvis(user_id, message, history)

    add_message(channel_id, "assistant", answer)

    if len(answer) > 1900:
        answer = answer[:1900] + "\n\n[truncated]"

    await ctx.send(answer)


# ---------------- RUN BOT ----------------
bot.run(TOKEN)