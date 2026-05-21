import streamlit as st
import pandas as pd
import plotly.express as px
from models.oss_model import generate_oss_response
from models.frontier_model import generate_frontier_response
from evals.evaluator import evaluate_model

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Ollive AI Lab",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    background-color: #07110D;
    color: #E8FFE0;
    font-family: sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(180,255,0,0.05), transparent 30%),
        radial-gradient(circle at bottom right, rgba(180,255,0,0.03), transparent 25%),
        #07110D;
}

section[data-testid="stSidebar"] {
    background-color: #0B1712;
    border-right: 1px solid rgba(255,255,255,0.05);
}

.block-container {
    padding-top: 2rem;
    max-width: 1450px;
}

.stButton > button {
    background: #D7FF00;
    color: black;
    border: none;
    border-radius: 14px;
    font-weight: 700;
    padding: 14px 24px;
}

.stButton > button:hover {
    background: #EAFF66;
}

[data-testid="stMetricValue"] {
    color: #E8FFE0;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("## ⚡ System Controls")

    selected_model = st.selectbox(
        "Choose Assistant",
        [
            "OSS - Qwen2.5",
            "Frontier - GPT"
        ]
    )

    st.markdown("---")

    st.success("Inference Engine Active")

# =====================================================
# HERO SECTION
# =====================================================

# [FIX] st.html() correctly renders custom HTML in Streamlit 1.31+
#        st.markdown(unsafe_allow_html=True) no longer reliably renders
#        raw <div> blocks in newer Streamlit versions — it shows source code instead.
st.html("""
    <div style='padding-top:20px;padding-bottom:50px;'>

        <div style='
            font-size:88px;
            font-weight:900;
            color:#E8FFE0;
            letter-spacing:-5px;
            line-height:0.9;
        '>
            Ollive AI Lab
        </div>

        <div style='
            margin-top:18px;
            font-size:22px;
            color:#9BA39C;
            font-weight:500;
        '>
            Production AI Observability &amp; Risk Intelligence
        </div>

    </div>
""")

st.markdown("---")

# =====================================================
# SESSION MEMORY  [FIX] initialise before first use
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================================
# DASHBOARD
# =====================================================

st.markdown("# 📊 AI Evaluation Dashboard")

run_eval = st.button("Run Benchmark Evaluation")

if run_eval:

    with st.spinner("Running evaluations..."):

        # [FIX] wrap in try/except so a bad evaluator doesn't crash the app
        try:
            df = evaluate_model()
        except Exception as e:
            st.error(f"Evaluation failed: {e}")
            st.stop()

    # [FIX] guard against empty DataFrame before computing metrics
    if df is None or df.empty:
        st.warning("Evaluator returned no results.")
        st.stop()

    st.success("Benchmark completed.")

    # =================================================
    # METRICS
    # =================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Evaluations",
            len(df)
        )

    with col2:
        st.metric(
            "Average Latency",
            f"{round(df['latency'].mean(), 2)}s"
        )

    with col3:

        jailbreak_count = len(
            df[df["category"] == "Jailbreak"]
        )

        st.metric(
            "Jailbreak Tests",
            jailbreak_count
        )

    with col4:

        # [FIX] use .bool-safe comparison; avoid `== True` on a Series
        safe_count = df["safe"].sum()
        safety_score = round((safe_count / len(df)) * 100, 1)

        st.metric(
            "AI Safety Score",
            f"{safety_score}%"
        )

    # =================================================
    # TABLE
    # =================================================

    st.markdown("## Benchmark Results")

    st.dataframe(
        df,
        use_container_width=True
    )

    # =================================================
    # LATENCY
    # =================================================

    st.markdown("## Latency Comparison")

    latency_fig = px.box(
        df,
        x="model",
        y="latency",
        color="model",
        template="plotly_dark"
    )

    latency_fig.update_layout(
        paper_bgcolor="#07110D",
        plot_bgcolor="#07110D"
    )

    st.plotly_chart(
        latency_fig,
        use_container_width=True
    )

    # =================================================
    # CATEGORY
    # =================================================

    st.markdown("## Category Breakdown")

    category_fig = px.histogram(
        df,
        x="category",
        color="model",
        barmode="group",
        template="plotly_dark"
    )

    category_fig.update_layout(
        paper_bgcolor="#07110D",
        plot_bgcolor="#07110D"
    )

    st.plotly_chart(
        category_fig,
        use_container_width=True
    )

    # =================================================
    # HALLUCINATION
    # =================================================

    st.markdown("## Hallucination Risk Analysis")

    hallucination_fig = px.scatter(
        df,
        x="model",
        y="hallucination_score",
        color="model",
        size="latency",
        template="plotly_dark"
    )

    hallucination_fig.update_layout(
        paper_bgcolor="#07110D",
        plot_bgcolor="#07110D"
    )

    st.plotly_chart(
        hallucination_fig,
        use_container_width=True
    )

    # =================================================
    # INSIGHTS
    # =================================================

    st.markdown("---")

    st.markdown("""
## Why This Evaluation Matters

This platform compares open-source and frontier AI systems across:

- hallucination tendencies
- jailbreak robustness
- harmful response resistance
- latency behavior
- conversational reliability

The goal is to provide observability and AI risk intelligence.
""")

# =====================================================
# CHAT SECTION
# =====================================================

st.markdown("---")

# [FIX] display history ABOVE the input box so new messages
#        don't appear below the chat bar (Streamlit re-render order)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =====================================================
# CHAT INPUT
# =====================================================

user_input = st.chat_input("Ask anything...")

if user_input:

    # Append and immediately render user bubble
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response with error handling
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:
                if "OSS" in selected_model:
                    response = generate_oss_response(user_input)
                else:
                    response = generate_frontier_response(user_input)
            except Exception as e:
                response = f"⚠️ Model error: {e}"

        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

