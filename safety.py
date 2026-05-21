UNSAFE_KEYWORDS = [
    "ransomware",
    "hack website",
    "bypass bank",
    "make malware",
    "steal passwords",
    "ddos",
    "phishing",
    "exploit"
]

def is_safe_prompt(prompt: str):
    prompt_lower = prompt.lower()

    for word in UNSAFE_KEYWORDS:
        if word in prompt_lower:
            return False

    return True
