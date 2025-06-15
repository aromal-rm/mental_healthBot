import streamlit as st
import os
import json
from utils.sentiment import get_sentiment_score
from utils.safety import detect_risk
from utils.ai_engine import generate_response
from utils.memory import load_memory, save_memory, update_memory, extract_memory_context

st.set_page_config(
    page_title="AntarAtma",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🧘"
)

# Helper function to clean AI responses
def clean_response(response):
    """Clean HTML artifacts from AI responses while preserving formatting"""
    if not response:
        return ""
    
    import re
    
    # Remove specific problematic HTML artifacts
    cleaned = response.replace('</div>', '').replace('<div>', '')
    cleaned = cleaned.replace('</41tv>', '').replace('<41tv>', '')
    
    # Remove any malformed or unknown tags but preserve common formatting tags
    # This regex removes tags that are not common formatting tags
    allowed_tags = r'(?!/?(?:strong|b|em|i|u|br|p|ul|ol|li|h[1-6]|blockquote|code|pre)\b)'
    cleaned = re.sub(r'<' + allowed_tags + r'[^>]*>', '', cleaned)
    
    # Clean up multiple spaces but preserve line breaks
    cleaned = re.sub(r'[ \t]+', ' ', cleaned)  # Multiple spaces/tabs to single space
    cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)  # Multiple newlines to double newline
    cleaned = cleaned.strip()
    
    return cleaned

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

# Custom CSS for the app
st.markdown("""
<style>
/* Base styles */
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --user-color: #4f46e5;
    --bot-color: #7c3aed;
    --text-color: #1e293b;
    --light-bg: #f8fafc;
    --dark-bg: #ffffff;
    --border-radius: 12px;
    --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
    --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
    --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-color);
    background-color: var(--light-bg);
}

/* Header */
.header {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    padding: 1.5rem 1rem;
    text-align: center;
    border-radius: 0 0 var(--border-radius) var(--border-radius);
    margin: -1rem -1rem 1.5rem -1rem;
    box-shadow: var(--shadow-md);
}

.header h1 {
    font-weight: 700;
    font-size: 2rem;
    margin-bottom: 0.25rem;
}

.header p {
    font-size: 1rem;
    opacity: 0.9;
    margin: 0;
}

/* Chat container */
.chat-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 1rem 6rem;
}

/* Message bubbles */
.message {
    display: flex;
    margin-bottom: 1rem;
    align-items: flex-end;
    max-width: 85%;
}

.user-message {
    margin-left: auto;
    justify-content: flex-end;
}

.bot-message {
    margin-right: auto;
    justify-content: flex-start;
}

.message-content {
    padding: 0.75rem 1rem;
    border-radius: var(--border-radius);
    line-height: 1.5;
    font-size: 0.95rem;
    box-shadow: var(--shadow-sm);
    max-width: 100%;
    word-wrap: break-word;
}

.user-message .message-content {
    background-color: var(--user-color);
    color: white;
    border-bottom-right-radius: 4px;
}

.bot-message .message-content {
    background-color: var(--dark-bg);
    color: var(--text-color);
    border-bottom-left-radius: 4px;
    box-shadow: var(--shadow-sm);
    border: 1px solid #e2e8f0;
}

.message-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 0.5rem;
    flex-shrink: 0;
    font-weight: bold;
    color: white;
}

.user-message .message-avatar {
    background-color: var(--user-color);
}

.bot-message .message-avatar {
    background-color: var(--bot-color);
}

/* Input area */
.input-area {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: white;
    padding: 1rem;
    border-top: 1px solid #e2e8f0;
    box-shadow: var(--shadow-lg);
    z-index: 100;
}

.input-container {
    max-width: 800px;
    margin: 0 auto;
    display: flex;
    gap: 0.5rem;
    align-items: center;
}

.stTextInput>div>div>input {
    border-radius: var(--border-radius);
    padding: 0.75rem 1rem;
    border: 1px solid #e2e8f0;
    box-shadow: var(--shadow-sm);
    font-size: 0.95rem;
}

.stTextInput>div>div>input:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}

/* Buttons */
.stButton>button {
    border-radius: var(--border-radius);
    background: var(--primary-color);
    border: none;
    color: white;
    padding: 0.75rem 1.5rem;
    font-size: 0.95rem;
    transition: all 0.2s;
    height: auto;
}

.stButton>button:hover {
    background: var(--secondary-color);
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
}

/* Exercise cards */
.exercise-card {
    background: white;
    border-radius: var(--border-radius);
    padding: 1rem;
    margin: 1rem 0;
    box-shadow: var(--shadow-sm);
    border: 1px solid #e2e8f0;
}

.exercise-card h3 {
    color: var(--primary-color);
    margin-top: 0;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
    background: #c7d2fe;
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--primary-color);
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .chat-container {
        padding: 0 0.5rem 6rem;
    }
    
    .message {
        max-width: 90%;
    }
    
    .input-container {
        padding: 0 0.5rem;
    }
}

/* Animation for new messages */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.message {
    animation: fadeIn 0.3s ease-out;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h1>🧘 AntarAtma</h1>
    <p>Your AI-powered mental wellness companion</p>
</div>
""", unsafe_allow_html=True)

# Main chat container
with st.container():
    chat_container = st.empty()
    
    with chat_container.container():
        for i, msg in enumerate(st.session_state.history):
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="message user-message">
                    <div class="message-content">
                        {msg["parts"][0]}
                    </div>
                    <div class="message-avatar">Y</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Clean the response before displaying
                cleaned_response = clean_response(msg["parts"][0])
                st.markdown(f"""
                <div class="message bot-message">
                    <div class="message-avatar">A</div>
                    <div class="message-content">
                        {cleaned_response}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Process input
if st.session_state.input_triggered:
    user_input = st.session_state.user_input.strip()

    if user_input:
        # Add user message to history
        st.session_state.history.append({"role": "user", "parts": [user_input]})
        
        # Analyze input
        risk = detect_risk(user_input)
        sentiment = get_sentiment_score(user_input)

        if risk:
            response = generate_response(user_input, crisis_mode=True)
        else:
            memory_context = extract_memory_context(user_input, st.session_state.memory)
            response = generate_response(user_input, st.session_state.history, memory_context)
            
            # Update memory
            update_memory(user_input, st.session_state.memory)
            save_memory(st.session_state.memory)

            # Suggest exercises if negative sentiment
            if sentiment < -0.2:
                with st.container():
                    st.markdown(f"""
                    <div class="exercise-card">
                        <h3>🧘 Breathing Exercise</h3>
                        <p>You seem to be feeling low. Try this breathing technique:</p>
                        <p><strong>{exercises["breathing"]["name"]}</strong>: {exercises["breathing"]["description"]}</p>
                        <p>Steps: {exercises["breathing"]["steps"]}</p>
                    </div>
                    """, unsafe_allow_html=True)

        # Add response to history (clean it before storing)
        cleaned_response = clean_response(response)
        st.session_state.history.append({"role": "model", "parts": [cleaned_response]})

    # Reset input state
    st.session_state.input_triggered = False
    st.session_state.user_input = ""
    st.rerun()

# Input area at bottom
st.markdown('<div class="input-area">', unsafe_allow_html=True)
col1, col2 = st.columns([6, 1])
with col1:
    user_input = st.text_input(
        "Type your message...",
        key="user_input",
        label_visibility="collapsed",
        placeholder="How are you feeling today?",
        on_change=lambda: st.session_state.update({"input_triggered": True})
    )
with col2:
    if st.button("Send", use_container_width=True):
        st.session_state.input_triggered = True
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Sidebar for additional features
with st.sidebar:
    st.markdown("### 🧠 Memory Context")
    st.json(st.session_state.memory)
    
    st.markdown("### ⚙️ Settings")
    if st.button("🔄 Reset Session"):
        st.session_state.history = []
        st.session_state.memory = {}
        if "user_input" in st.session_state:
            del st.session_state["user_input"]
        save_memory({})
        st.rerun()
    
    st.markdown("### 💡 Quick Exercises")
    for ex_name, ex_data in exercises.items():
        with st.expander(f"{ex_name.capitalize()} Exercise"):
            st.json(ex_data)
    
    st.markdown("---")
    st.caption("🛡️ AntarAtma is a self-help companion, not a substitute for professional care.")