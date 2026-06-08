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

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY is not set in the environment variables.")

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# Faster than 120B
MODEL = "google/gemini-flash-latest"

# Simple instant-response cache
FAST_RESPONSES = {
    "hi": "Hello!",
    "hello": "Hey!",
    "hey": "Hey there!",
    "who are you": "I'm Jarvis.",
    "good morning": "Good morning!",
    "good night": "Good night!"
}


def ask_jarvis(user_id: int, question: str, history=None):

    question_clean = question.lower().strip()

    # ---------------- INSTANT REPLIES ----------------
    if question_clean in FAST_RESPONSES:
        return FAST_RESPONSES[question_clean]

    # ---------------- TOOL CHECK ----------------
    tool_result = tool_router(question, user_id)

    if tool_result:
        return tool_result

    # ---------------- SMALL HISTORY ----------------
    history = history or []
    history = history[-5:]

    # ---------------- LOAD MEMORY ONLY WHEN NEEDED ----------------
    memory_keywords = [
        "remember",
        "memory",
        "who am i",
        "what do you know about me",
        "what did we talk about",
        "recall"
    ]

    use_memory = any(
        keyword in question_clean
        for keyword in memory_keywords
    )

    if use_memory:

        profile = get_profile(user_id)

        facts = recall_facts()[-5:]

        user_mem = get_user_memory(user_id)[-5:]

        chat_summary = summarize_chat(history)

        system_prompt = f"""
You are JARVIS.

Profile:
{profile.get("summary","")}

Facts:
{facts}

User Memory:
{user_mem}

Recent Chat:
{chat_summary}

Be concise and helpful.
"""

    else:

        system_prompt = """
You are JARVIS.

Be concise.
Give direct answers.
Avoid unnecessary words.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0.7,
        max_tokens=250
    )

    return response.choices[0].message.content