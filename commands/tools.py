import datetime
import math

from commands.conversation_memory import (
    clear_chat,
    remember_fact
)


def calculator(expr: str):

    try:

        allowed_names = {
            k: v
            for k, v in math.__dict__.items()
            if not k.startswith("__")
        }

        return str(
            eval(
                expr,
                {"__builtins__": {}},
                allowed_names
            )
        )

    except:
        return "Invalid math expression"


def run_tool(text, channel_id):

    t = text.lower()

    # Time
    if "time" in t:
        return f"🕒 {datetime.datetime.now().strftime('%H:%M:%S')}"

    # Date
    if "date" in t:
        return f"📅 {datetime.date.today()}"

    # Clear chat
    if "clear chat" in t:
        clear_chat(channel_id)
        return "🧹 Chat cleared."

    # Memory
    if "remember" in t:
        remember_fact(text)
        return "🧠 Saved to memory."

    # Calculator
    if any(op in t for op in ["+", "-", "*", "/", "**"]):
        return f"🧮 Result: {calculator(text)}"

    return None