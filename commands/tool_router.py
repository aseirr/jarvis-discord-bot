from commands.tools import run_tool
from commands.web_tool import web_search


def tool_router(message: str, user_id: int):
    text = message.lower()

    # ---------------- FAST RULES (NO AI CALL) ----------------
    if "time" in text or "date" in text:
        return run_tool("time", user_id)

    if any(op in text for op in ["+", "-", "*", "/", "**"]):
        return run_tool(message, user_id)

    if text.startswith("web ") or "search" in text:
        return web_search(message)

    if "clear chat" in text:
        return run_tool("clear chat", user_id)

    return None