import streamlit as st
import requests
import json
from datetime import datetime

# FastAPI backend URL
BASE_URL = "http://localhost:8000"

# Session state
if "user" not in st.session_state:
    st.session_state.user = None
if "token" not in st.session_state:
    st.session_state.token = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "bot"

st.set_page_config(page_title="WhatsEase Chat", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .user-message {
        text-align: right;
        background-color: #007bff;
        color: white;
        padding: 10px 15px;
        margin: 5px 0;
        border-radius: 18px 18px 4px 18px;
        max-width: 70%;
        word-wrap: break-word;
        float: right;
        clear: both;
    }
    .bot-message {
        text-align: left;
        background-color: #f1f1f1;
        color: black;
        padding: 10px 15px;
        margin: 5px 0;
        border-radius: 18px 18px 18px 4px;
        max-width: 70%;
        word-wrap: break-word;
        float: left;
        clear: both;
    }
    .message-container {
        overflow: hidden;
        margin-bottom: 10px;
    }
    .timestamp {
        font-size: 0.8em;
        color: #888;
        margin-top: 2px;
    }
    .sidebar-header {
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Login function
def login(email, password):
    response = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
    if response.status_code == 200:
        data = response.json()
        st.session_state.token = data["access_token"]
        st.session_state.user = email
        return True
    return False

# Get messages from API
def load_messages(recipient):
    if st.session_state.token:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.get(f"{BASE_URL}/messages/{recipient}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            st.session_state.messages = data["messages"]

# Send message via API
def send_message(recipient, content):
    if st.session_state.token:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        message_data = {
            "message_id": f"{st.session_state.user}_{datetime.utcnow().isoformat()}",
            "recipient": recipient,
            "content": content,
            "is_bot_response": False
        }
        response = requests.post(f"{BASE_URL}/messages", json=message_data, headers=headers)
        if response.status_code == 200:
            load_messages(recipient)  # Refresh messages

# Login UI
if st.session_state.user is None:
    st.title("WhatsEase Chat Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(email, password):
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Login failed. Check credentials.")
else:
    st.title("WhatsEase Chat")
    st.sidebar.success(f"Logged in as: {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.token = None
        st.rerun()

    # Chat selection
    chat_options = ["bot", "user1@example.com"]  # Expand as needed
    selected_chat = st.sidebar.selectbox("Select Chat", chat_options, key="chat_select")
    st.session_state.current_chat = selected_chat

    # Load messages
    load_messages(selected_chat)

    # Display messages
    st.subheader(f"Chat with {selected_chat}")
    st.markdown('<div class="message-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        timestamp_str = datetime.fromisoformat(msg["timestamp"].replace('Z', '+00:00')).strftime("%Y-%m-%d %H:%M")
        if msg["sender"] == st.session_state.user:
            st.markdown(
                f'<div class="user-message">{msg["content"]}<br><span class="timestamp">{timestamp_str}</span></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="bot-message">{msg["content"]}<br><span class="timestamp">{timestamp_str}</span></div>',
                unsafe_allow_html=True
            )
    st.markdown('</div>', unsafe_allow_html=True)

    # Input area
    user_input = st.text_input("Type your message", key="input")
    if st.button("Send") and user_input.strip():
        if selected_chat == "bot":
            # For bot, send message and expect response via refresh
            send_message(selected_chat, user_input)
        else:
            send_message(selected_chat, user_input)
        st.rerun()

    # Auto-refresh for real-time
    if st.button("Refresh Messages"):
        load_messages(selected_chat)
        st.rerun()
