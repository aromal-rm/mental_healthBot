import json
import os
import re

MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_memory(memory_dict):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory_dict, f, indent=2)

def update_memory(text, memory):
    # Store known phrases
    if "my name is" in text.lower():
        name = text.lower().split("my name is")[-1].strip().split(" ")[0].capitalize()
        memory["Name"] = name
    if "i am from" in text.lower():
        location = text.lower().split("i am from")[-1].strip().split(" ")[0].capitalize()
        memory["Location"] = location

def extract_memory_context(text, memory):
    context = []
    for k, v in memory.items():
        if k.lower() not in text.lower():
            context.append(f"{k}: {v}")
    return ", ".join(context)
