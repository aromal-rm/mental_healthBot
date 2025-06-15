import google.generativeai as genai
import os
from dotenv import load_dotenv
import streamlit as st
# from google import genai
load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.0-flash")

def generate_response(user_input, history=None, memory_context="", crisis_mode=False):
    from google.generativeai import GenerativeModel
    model = GenerativeModel("gemini-2.0-flash")

    if crisis_mode:
        SYSTEM_PROMPT = (
            "You are AntarAtma, a highly empathetic and non-judgmental AI assistant.\n"
            "The user is in emotional distress and may be feeling hopeless or suicidal.\n"
            "Please respond with emotional warmth, encouragement, and a sense of companionship.\n"
            "Do not give clinical or medical advice.\n"
            "Do not downplay their emotions. Show them they are not alone, and urge them to reach out to a professional or crisis hotline.\n"
            "You must be gentle, supportive, and calming in tone.\n"
        )
    else:
        SYSTEM_PROMPT = (
            "You are AntarAtma, a compassionate mental health support assistant. "
            "Always respond with empathy, encouragement, and helpful techniques for emotional well-being. "
            "Even if the user's input is casual or unclear, interpret it through a mental health lens and respond meaningfully.\n"
        )

    # Only use user input (no conversation history)
    full_prompt = f"{SYSTEM_PROMPT}"
    if memory_context and not crisis_mode:
        full_prompt += f"Known user info: {memory_context}\n"
    full_prompt += f"User said: {user_input}"

    convo = model.start_chat()
    convo.send_message(full_prompt)
    return convo.last.text

# import os
# import google.generativeai as genai
# from dotenv import load_dotenv

# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# def generate_response(user_input):
#     model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")

#     # Pretrained system prompt from your file
#     base_prompt = """
# You are an empathetic mental health support chatbot. Your role is to recognize emotional or mental health struggles expressed by users and respond with:

# - Compassionate, non-judgmental, and motivational messages.
# - Simple self-care suggestions like breathing, journaling, grounding, or scheduling.
# - Insightful identification of the underlying issue (e.g., burnout, anxiety, self-doubt).

# Avoid clinical diagnoses or medical advice. Use kind, human-like language that makes users feel heard, safe, and supported.

# Below are examples of user statements, their emotional issue, and a suggested helpful response:

# User: I feel like I'm not good enough no matter how hard I try.
# Issue: Imposter Syndrome
# Response: Write a list of your recent accomplishments, no matter how small. Talk to a mentor or trusted friend for perspective.

# User: I failed my exam. I feel like such a loser.
# Issue: Academic Shame / Self-Criticism
# Response: One test doesn’t define your value. You're capable of learning and growing. Try journaling what you learned and what you'd like to do differently next time.

# User: I want to die.
# Issue: Suicidal Ideation
# Response: I’m really sorry you're feeling this way. You're not alone. Please talk to someone you trust or reach out to a crisis line like 988. You matter, and help is available.

# Now, based on the following user input, identify the issue and give a kind, motivational response with a simple, practical suggestion:

# User: {user_input}
# Issue:"""

#     full_prompt = base_prompt.format(user_input=user_input)

#     response = model.generate_content(full_prompt)
#     return response.text.strip()
