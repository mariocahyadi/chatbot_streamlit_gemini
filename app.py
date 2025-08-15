import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent'

st.set_page_config(page_title="Indonesian Stock Market Chatbot", page_icon="??")
st.title("Indonesian Stock Market Chatbot")
st.write("Ask anything about the Indonesian stock market!")

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Display chat history
for msg in st.session_state['messages']:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])


# System prompt to restrict answers to Indonesian stock market only
SYSTEM_PROMPT = (
    "You are an expert assistant that only answers questions about the Indonesian stock market. "
    "If the question is not about the Indonesian stock market, politely refuse to answer."
)

user_input = st.chat_input("Type your question...")

if user_input:
    st.session_state['messages'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    # Prepare Gemini API request with system prompt
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {
        "contents": [
            {"role": "system", "parts": [{"text": SYSTEM_PROMPT}]},
            {"role": "user", "parts": [{"text": user_input}]}
        ],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 512}
    }
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data, timeout=30)
        response.raise_for_status()
        gemini_reply = response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        gemini_reply = f"Error: {e}"

    st.session_state['messages'].append({'role': 'assistant', 'content': gemini_reply})
    with st.chat_message('assistant'):
        st.markdown(gemini_reply)
