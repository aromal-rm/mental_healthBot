import re

DANGER_PATTERNS = [
    r"suicid(al|e)?", r"kill myself", r"end my life", r"worthless", r"hopeless",
    r"i want to die", r"i hate my life", r"i'm done", r"i can't go on"
]

def detect_risk(text):
    for pattern in DANGER_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False
