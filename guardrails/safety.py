UNSAFE_KEYWORDS = [
    "make ransomware",
    "hack website",
    "bypass bank security",
    "build malware",
    "steal password",
    "ddos",
    "phishing",
    "credit card fraud"
]

BIAS_KEYWORDS = [
    "which gender is smarter",
    "which race is smarter",
    "superior race",
    "inferior gender"
]

def check_safety(user_input):

    text = user_input.lower()

    for keyword in UNSAFE_KEYWORDS:
        if keyword in text:
            return False, f"Detected unsafe content: {keyword}"

    for keyword in BIAS_KEYWORDS:
        if keyword in text:
            return False, f"Detected biased or harmful prompt: {keyword}"

    return True, "safe"
