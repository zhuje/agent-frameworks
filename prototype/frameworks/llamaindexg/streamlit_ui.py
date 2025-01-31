import streamlit as st
import requests

# Streamlit interface
def run_chat_interface():
    st.title("Insurance Agent")
    st.write("Welcome! Chat with the agent to calculate your insurance score and eligibility.")

    # Text input for user query
    user_input = st.text_area("Describe your driving history and insurance details:", 
                              height=150, placeholder="Tell the agent about your driving habits...")

    if st.button("Submit"):
        if user_input:
            # Call FastAPI backend with the user input
            url = "http://127.0.0.1:8000/process_input/"
            response = requests.post(url, json={"text": user_input})

            if response.status_code == 200:
                result = response.json()
                st.write(f"Generated Insurance Score: {result['response']}")
                st.write(f"Approval Status: {result['approval_status']}")
            else:
                st.write("There was an error processing the request.")
        else:
            st.write("Please enter some information about your driving history.")

if __name__ == "__main__":
    run_chat_interface()
