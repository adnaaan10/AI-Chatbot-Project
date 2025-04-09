import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Streamlit page setup
st.set_page_config(page_title="AI-Powered Personal Companion", page_icon="🧠", layout="centered")
st.title("🤖 AI-Powered Personal Companion")

# Session state to hold chat history per user
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# Chat input box
user_message = st.chat_input("Type your message here...")

if user_message:
    # Display and store user message
    st.chat_message("user").markdown(user_message)
    st.session_state.chat_history.append({"role": "user", "content": user_message})

    # Build context prompt from previous chat history
    prompt = "\n".join([
        f"User: {msg['content']}" if msg["role"] == "user" else f"Bot: {msg['content']}"
        for msg in st.session_state.chat_history
    ])
    prompt += f"\nUser: {user_message}\nBot:"

    # Generate response using Gemini
    response = model.generate_content(prompt)
    bot_reply = response.text if response.text else "Sorry, I couldn't generate a response."

    # Display and store bot response
    st.chat_message("assistant").markdown(bot_reply, unsafe_allow_html=True)
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
