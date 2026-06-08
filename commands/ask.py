import os
from dotenv import load_dotenv
from openai import OpenAI

from commands.tool_router import tool_router
from commands.conversation_memory import (
    recall_facts,
    get_user_memory,
    get_profile,
    summarize_chat
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "openai/gpt-oss-120b"


def ask_jarvis(user_id: int, question: str, history=None):

    history = history or []
    history = history[-10:]  # smaller context = faster

    # ---------------- FAST TOOL CHECK (NO AI CALL) ----------------
    tool_result = tool_router(question, user_id)

    if tool_result:
        return tool_result

    # ---------------- MINIMAL MEMORY ----------------
    profile = get_profile(user_id)

    facts = recall_facts()[-10:]      # reduced
    user_mem = get_user_memory(user_id)[-10:]
    chat_summary = summarize_chat(history)

    # ---------------- SMALLER PROMPT (FASTER TOKENS) ----------------
    system_prompt = f"""
You are JARVIS.

Profile: {profile.get("summary","")}

Facts: {facts}
Memory: {user_mem}
Chat: {chat_summary}

Be concise.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    return response.choices[0].message.content