from commands.tools import run_tool
from commands.web_tool import web_search


def tool_router(message: str, channel_id: int):

    text = message.lower()

    # Time
    if "time" in text:
        return run_tool("time", channel_id)

    # Date
    if "date" in text:
        return run_tool("date", channel_id)

    # Calculator
    if any(op in text for op in ["+", "-", "*", "/", "**"]):
        return run_tool(message, channel_id)

    # Web Search
    if (
        text.startswith("search ")
        or "search for" in text
        or "look up" in text
        or text.startswith("web ")
    ):
        return web_search(message)

    # Clear chat
    if "clear chat" in text:
        return run_tool("clear chat", channel_id)

    return None