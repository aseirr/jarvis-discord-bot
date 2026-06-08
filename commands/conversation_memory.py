import json
import os

CHAT_FILE = "chat_memory.json"
USER_FILE = "user_memory.json"
FACT_FILE = "global_facts.json"
PROFILE_FILE = "user_profile.json"


# ---------------- LOAD SAFE ----------------
def load(file):
    if not os.path.exists(file):
        return {}

    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


chat_memory = load(CHAT_FILE)
user_memory = load(USER_FILE)
fact_memory = load(FACT_FILE)
user_profile = load(PROFILE_FILE)


# ---------------- SAVE ----------------
def save(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ---------------- CHAT ----------------
def add_message(channel_id, role, message):
    cid = str(channel_id)

    chat_memory.setdefault(cid, [])
    chat_memory[cid].append({"role": role, "message": message})

    chat_memory[cid] = chat_memory[cid][-20:]
    save(CHAT_FILE, chat_memory)


def get_history(channel_id):
    return chat_memory.get(str(channel_id), [])


# ---------------- FACTS ----------------
def remember_fact(fact):
    fact_memory.setdefault("facts", [])
    fact_memory["facts"].append(fact)
    fact_memory["facts"] = fact_memory["facts"][-200:]
    save(FACT_FILE, fact_memory)


def recall_facts():
    return fact_memory.get("facts", [])


# ---------------- USER MEMORY ----------------
def get_user_memory(user_id):
    return user_memory.get(str(user_id), [])


def remember_user(user_id, fact):
    uid = str(user_id)

    user_memory.setdefault(uid, [])
    user_memory[uid].append(fact)

    user_memory[uid] = user_memory[uid][-50:]
    save(USER_FILE, user_memory)


# ---------------- PROFILE ----------------
def get_profile(user_id):
    return user_profile.get(str(user_id), {
        "summary": "",
        "interests": [],
        "preferences": []
    })


# ---------------- 🧠 NEW: MEMORY SUMMARIZER ----------------
def summarize_chat(history):
    """
    Turns long chat into a compact memory summary
    """
    if not history:
        return ""

    # keep only last few messages
    last = history[-10:]

    summary = []

    for m in last:
        summary.append(f"{m['role']}: {m['message']}")

    return " | ".join(summary)


# ---------------- UTIL ----------------
def clear_chat(channel_id):
    chat_memory[str(channel_id)] = []
    save(CHAT_FILE, chat_memory)