import requests
import streamlit as st

FASTAPI_URL = "http://localhost:8005"  # or your OpenShift route

def main():
    st.title("Insurance Workflow Demo (Scorer + Approver)")

    user_input = st.text_input("Enter your request:")
    if st.button("Submit"):
        if user_input.strip():
            # Call the FastAPI endpoint
            payload = {"user_input": user_input}
            resp = requests.post(f"{FASTAPI_URL}/run_insurance_workflow/", json=payload)
            if resp.status_code == 200:
                data = resp.json()
                messages = data.get("messages", [])
                for msg in messages:
                    st.write(f"**AI:** {msg}")
            else:
                st.error("Error calling the workflow endpoint.")
        else:
            st.warning("Please enter some text.")

if __name__ == "__main__":
    st.set_page_config(page_title="Insurance Scoring App")
    main()
