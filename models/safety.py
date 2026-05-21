UNSAFE_PATTERNS = [

    "how to make a bomb",
    "build malware",
    "steal password",
    "phishing attack",
    "credit card fraud",
    "hack website",
    "make ransomware",
    "sql injection",
    "bypass security",
    "ddos attack"

]

def is_safe_prompt(prompt):

    prompt_lower = prompt.lower()

    for pattern in UNSAFE_PATTERNS:

        if pattern in prompt_lower:
            return False

    return True
