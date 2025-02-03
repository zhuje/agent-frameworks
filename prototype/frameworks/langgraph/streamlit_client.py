import streamlit as st
import requests
from constant import APP_HOST, APP_PORT

# URL for the FastAPI server (adjust the port/host as needed)
API_URL = f"http://{APP_HOST}:{APP_PORT}"

def start_session():
    response = requests.post(f"{API_URL}/start-session")
    if response.status_code == 200:
        session_data = response.json()
        if "messages" in session_data and session_data["messages"]:
            session_data["messages"].pop(0)  # Remove the first message
        return session_data
    else:
        st.error("Failed to start session")
        return None

def send_message(session_id, message):
    payload = {"session_id": session_id, "message": message}
    response = requests.post(f"{API_URL}/chat", json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to send message")
        return None

# Initialize session state if needed.
if "session_id" not in st.session_state:
    session_data = start_session()
    if session_data:
        st.session_state.session_id = session_data["session_id"]
        st.session_state.chat_history = session_data.get("messages", [])
else:
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

# Set page configuration
st.set_page_config(
    page_title="Insurance Agent Chatbot",
    page_icon=":robot_face:"
)

st.title("Insurance Agent Chatbot")

# Display chat messages
for msg in st.session_state.chat_history:
    role = "user" if msg["role"] == "human" else "assistant"
    with st.chat_message(role):
        st.markdown(msg["content"])

# Get user input
if prompt := st.chat_input("Enter your message:"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "human", "content": prompt})
    # Display spinner while processing
    with st.spinner("Processing..."):
        # Send message to FastAPI server
        response = send_message(st.session_state.session_id, prompt)
        if response:
            # Display assistant response
            assistant_response = response["messages"][-1]["content"]
            with st.chat_message("assistant"):
                st.markdown(assistant_response)
            # Add assistant response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})