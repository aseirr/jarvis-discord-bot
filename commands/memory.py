import json

MEMORY_FILE = "data/memory.json"


def load_memory():

    try:
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)

    except:
        return []


def save_memory(data):

    with open(MEMORY_FILE, "w") as file:
        json.dump(data, file, indent=4)


def remember(fact):

    memory = load_memory()

    memory.append(fact)

    save_memory(memory)


def recall():

    return load_memory()


def memory_as_text():

    memory = load_memory()

    if not memory:
        return "No memories stored."

    return "\n".join(memory)