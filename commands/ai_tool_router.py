from commands.tool_schema import get_tools


def ai_decide_tool(client, model, user_message: str):

    tools = get_tools()

    tool_list = "\n".join(
        f"- {t['name']}: {t['description']}"
        for t in tools
    )

    messages = [
        {
            "role": "system",
            "content": f"""
You are a tool decision engine.

Available tools:
{tool_list}

RULES:
- Decide the best tool for the user request
- If none needed, reply ONLY: none
- Only reply with ONE word:
  time, calculator, memory, web, none
"""
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content.strip().lower()