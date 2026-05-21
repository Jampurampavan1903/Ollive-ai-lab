from transformers import pipeline
from guardrails.safety import check_safety

# =====================================================
# LOAD MODEL
# =====================================================

pipe = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct",
    device_map="auto"
)

# =====================================================
# MEMORY
# =====================================================

conversation_history = []

# =====================================================
# RESPONSE FUNCTION
# =====================================================

def generate_oss_response(user_input):

    # =========================
    # SAFETY CHECK
    # =========================

    safe, reason = check_safety(user_input)

    if not safe:
        return f"⚠️ Blocked by safety layer: {reason}"

    # =========================
    # STORE USER MESSAGE
    # =========================

    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    # Keep short-term memory
    memory_window = conversation_history[-6:]

    # =========================
    # SYSTEM PROMPT
    # =========================

    messages = [
        {
            "role": "system",
            "content": (
                "You are Ollive AI Lab assistant. "
                "Be concise, professional, safe, and helpful. "
                "Remember previous messages in the conversation."
            )
        }
    ]

    # Add memory
    messages.extend(memory_window)

    # =========================
    # GENERATE
    # =========================

    response = pipe(
        messages,
        max_new_tokens=180,
        temperature=0.7,
        do_sample=True
    )

    generated_text = response[0]["generated_text"][-1]["content"]

    # =========================
    # STORE ASSISTANT RESPONSE
    # =========================

    conversation_history.append({
        "role": "assistant",
        "content": generated_text
    })

    return generated_text
