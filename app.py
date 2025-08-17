
import streamlit as st
import requests
import os
from dotenv import load_dotenv
import yfinance as yf
def get_indonesia_stock_price(ticker):
    """
    Fetch latest price for an Indonesian stock using Yahoo Finance (e.g., 'BBCA.JK').
    Returns (price, currency) or (None, None) if not found.
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        if not data.empty:
            price = data['Close'].iloc[-1]
            currency = stock.info.get('currency', 'IDR')
            return price, currency
    except Exception:
        pass
    return None, None

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = os.getenv('GEMINI_API_URL')



st.set_page_config(page_title="Indonesian Stock Market Chatbot", page_icon="??")
# Centered logo at the top using Streamlit columns
col1, col2, col3 = st.columns([1,1,1])
with col1:
    st.write("")
with col2:
    st.image("logo.png", width=160)
with col3:
    st.write("")

st.title("Indonesian Stock Market Chatbot")
st.write("Ask anything about the Indonesian stock market!")

# --- Indonesia Stock Price Lookup UI ---
with st.expander("?? Check Indonesia Stock Price (Yahoo Finance)"):
    stock_code = st.text_input("Enter Stock Code (e.g. BBCA.JK, TLKM.JK):", "BBCA.JK")
    if st.button("Get Price"):
        price, currency = get_indonesia_stock_price(stock_code)
        if price:
            st.success(f"Latest price for {stock_code}: {price:.2f} {currency}")
        else:
            st.error(f"Could not fetch price for {stock_code}. Check the code and try again.")

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


    # Prepare Gemini API request for Gemini 2.5 (system prompt + user input as one part)
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_input}"
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 512}
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        # Debug: print the full response to Streamlit
        # st.write("Gemini API raw response:", result)
        # Try to extract the reply text robustly
        gemini_reply = None
        try:
            gemini_reply = result['candidates'][0]['content']['parts'][0]['text']
        except Exception:
            # Try alternative extraction if structure is different
            gemini_reply = result['candidates'][0]['content'].get('text', str(result))
        if not gemini_reply:
            gemini_reply = str(result)
    except Exception as e:
        gemini_reply = f"Error: {e}"

    st.session_state['messages'].append({'role': 'assistant', 'content': gemini_reply})
    with st.chat_message('assistant'):
        st.markdown(gemini_reply)

# Fixed footer at the bottom using custom CSS
st.markdown(
    """
    <style>
    .footer-mario {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: white;
        border-top: 1px solid #eee;
        text-align: right;
        color: gray;
        padding: 0.5em 1.5em 0.5em 0;
        z-index: 100;
        font-size: 0.85em;
        font-style: italic;
    }
    </style>
    <div class='footer-mario'>by Mario Cahyadi</div>
    """,
    unsafe_allow_html=True
)
