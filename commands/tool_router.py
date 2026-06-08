from commands.tools import run_tool
from commands.web_tool import web_search


def tool_router(message: str, channel_id: int):

    text = message.lower().strip()

    # ---------------- TIME ----------------
    if "time" in text:
        return run_tool("time", channel_id)

    # ---------------- DATE ----------------
    if "date" in text:
        return run_tool("date", channel_id)

    # ---------------- CALCULATOR ----------------
    if any(op in text for op in ["+", "-", "*", "/", "**"]):
        return run_tool(message, channel_id)

    # ---------------- WEB SEARCH ----------------
    if (
        "search" in text
        or "look up" in text
        or text.startswith("web ")
        or text.startswith("google ")
    ):
        return web_search(message)

    # ---------------- CLEAR CHAT ----------------
    if "clear chat" in text:
        return run_tool("clear chat", channel_id)

    # ---------------- MEMORY ----------------
    if "remember this" in text:
        return run_tool(message, channel_id)

    return None