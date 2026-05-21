import json
from datetime import datetime

LOG_FILE = "logs/usage_logs.json"

def log_interaction(
    model,
    prompt,
    response,
    latency,
    safe=True
):

    log_entry = {

        "timestamp": str(datetime.now()),

        "model": model,

        "prompt": prompt,

        "response": response,

        "latency": latency,

        "response_length": len(response),

        "safe": safe
    }

    try:

        with open(LOG_FILE, "r") as f:
            logs = json.load(f)

    except:
        logs = []

    logs.append(log_entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)
