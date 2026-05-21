import os
from openai import OpenAI
from guardrails.safety import check_safety

# =====================================================
# OPENAI CLIENT
# =====================================================

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# =====================================================
# MEMORY
# =====================================================

conversation_history = []

# =====================================================
# RESPONSE FUNCTION
# =====================================================

def generate_frontier_response(user_input):

    # -----------------------------
    # SAFETY CHECK
    # -----------------------------

    safe, reason = check_safety(user_input)

    if not safe:
        return f"⚠️ Blocked by safety layer: {reason}"

    # -----------------------------
    # SAVE USER MESSAGE
    # -----------------------------

    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    # -----------------------------
    # CALL GPT
    # -----------------------------

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=conversation_history[-10:]
    )

    assistant_reply = response.choices[0].message.content

    # -----------------------------
    # SAVE MEMORY
    # -----------------------------

    conversation_history.append({
        "role": "assistant",
        "content": assistant_reply
    })

    return assistant_reply
