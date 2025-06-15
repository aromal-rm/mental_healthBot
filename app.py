import streamlit as st
import os
import json
from utils.sentiment import get_sentiment_score
from utils.safety import detect_risk
from utils.ai_engine import generate_response
from utils.memory import load_memory, save_memory, update_memory, extract_memory_context

st.set_page_config(page_title="AntarAtma", layout="wide")
#test

# Load exercises
@st.cache_data
def load_exercises():
    base_path = os.path.join(os.path.dirname(__file__), "exercises")
    exercises = {}
    for ex in ["breathing", "journaling", "grounding"]:
        try:
            with open(os.path.join(base_path, f"{ex}.json")) as f:
                exercises[ex] = json.load(f)
        except Exception as e:
            exercises[ex] = {"error": f"Could not load {ex} exercise: {e}"}
    return exercises

exercises = load_exercises()

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "input_triggered" not in st.session_state:
    st.session_state.input_triggered = False

# Header
st.markdown("<h1 style='text-align: center;'>🧘 AntarAtma</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Your AI-powered mental wellness companion</p>", unsafe_allow_html=True)

# Style
# Style
st.markdown("""
<style>
html, body {
    background-color: #f6f9fc;
    color: #222831;
    font-family: 'Segoe UI', sans-serif;
    padding-bottom: 120px;
}

/* Header */
h1 {
    background: linear-gradient(135deg, #a1c4fd, #c2e9fb);
    color: #333;
    padding: 1.2rem;
    text-align: center;
    border-radius: 0 0 24px 24px;
    margin: -1rem -1rem 1rem -1rem;
    font-size: 2rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}

p {
    text-align: center;
    color: #555;
    font-size: 1.05rem;
    margin-bottom: 1.5rem;
}

/* Input container */
.input-container {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #ffffff;
    padding: 12px 5%;
    border-top: 1px solid #dde6f0;
    backdrop-filter: blur(6px);
    box-shadow: 0 -4px 12px rgba(0,0,0,0.05);
    z-index: 999;
}

.stTextInput > div > div > input {
    height: 45px;
    font-size: 16px;
    border-radius: 24px;
    padding-left: 16px;
    background-color: #f0f4f8;
    color: #222;
    border: 1px solid #a0b8d8;
}

/* Scrollable chat container */
.chat-scroll {
    max-height: 75vh;
    overflow-y: auto;
    padding-bottom: 140px;
    position: relative;
}

/* Fading effect at top */
.chat-scroll::before {
    content: '';
    position: sticky;
    top: 0;
    height: 40px;
    background: linear-gradient(to bottom, #f6f9fc, rgba(246,249,252,0));
    z-index: 5;
    pointer-events: none;
}

/* Chat message bubbles */
.chat-msg {
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
    border-radius: 20px;
    font-size: 16px;
    max-width: 85%;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    word-wrap: break-word;
    line-height: 1.6;
}

/* User bubble */
.user-msg {
    background: #c2f0f9;
    color: #073a47;
    margin-left: auto;
    text-align: right;
}

/* Bot bubble */
.bot-msg {
    background: #e9d2ff;
    color: #3b1e5e;
    margin-right: auto;
    text-align: left;
}

/* Expander header */
.stExpanderHeader {
    font-weight: 600;
    color: #3c3c3c;
}

/* Buttons */
.stButton>button {
    border-radius: 24px;
    background: linear-gradient(135deg, #7ed6df, #70a1ff);
    border: none;
    color: white;
    padding: 10px 24px;
    font-size: 15px;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #53c4cc, #576fe5);
    color: #fff;
}
</style>
""", unsafe_allow_html=True)


# Chat history display
with st.container():
    for i in range(0, len(st.session_state.history), 2):
        user_msg = st.session_state.history[i]["parts"][0]
        bot_msg = st.session_state.history[i + 1]["parts"][0] if i + 1 < len(st.session_state.history) else ""
        st.markdown(f"<div class='chat-msg user-msg'><b>You:</b> {user_msg}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-msg bot-msg'><b>AntarAtma:</b> {bot_msg}</div>", unsafe_allow_html=True)

# ✅ Process input BEFORE rendering widget
if st.session_state.input_triggered:
    user_input = st.session_state.user_input.strip()

    if user_input:
        risk = detect_risk(user_input)
        sentiment = get_sentiment_score(user_input)
        st.session_state.history.append({"role": "user", "parts": [user_input]})

        if risk:
            response = generate_response(user_input, crisis_mode=True)
        else:
            memory_context = extract_memory_context(user_input, st.session_state.memory)
            response = generate_response(user_input, st.session_state.history, memory_context)

            update_memory(user_input, st.session_state.memory)
            save_memory(st.session_state.memory)

            if sentiment < -0.2:
                st.info("You seem to be feeling low. Here's a helpful breathing technique:")
                st.json(exercises["breathing"])

        st.session_state.history.append({"role": "model", "parts": [response]})

    # Reset state BEFORE widget renders again
    st.session_state.user_input = ""
    st.session_state.input_triggered = False
    st.experimental_rerun()

# Input field
st.markdown('<div class="input-container">', unsafe_allow_html=True)
user_input = st.text_input(
    "Type your message here:",
    key="user_input",
    label_visibility="collapsed",
    placeholder="How are you feeling today?",
    on_change=lambda: st.session_state.update({"input_triggered": True})
)
st.markdown('</div>', unsafe_allow_html=True)

# Memory viewer
with st.expander("🧠 View remembered info"):
    st.json(st.session_state.memory)

# Reset
if st.button("🔄 Reset Session"):
    st.session_state.history = []
    st.session_state.memory = {}
    st.session_state.input_triggered = False

    # safely remove user_input if it exists
    if "user_input" in st.session_state:
        del st.session_state["user_input"]

    save_memory({})
    st.experimental_rerun()

st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
st.caption("🛡️ AntarAtma is a self-help companion, not a substitute for professional care.")
