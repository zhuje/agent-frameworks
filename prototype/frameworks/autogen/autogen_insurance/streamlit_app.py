import streamlit as st
import autogen
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from agents.analyst_agent import create_analyst_agent

# Initialize session state variables
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'data' not in st.session_state:
    st.session_state.data = None
if 'agents_initialized' not in st.session_state:
    st.session_state.agents_initialized = False

def initialize_agents(api_key):
    """Initialize AutoGen agents with the provided API key"""
    config_list = [{
        "model": "gpt-4o-mini",
        "api_key": api_key
    }]
    
    # Create agents
    analyst = create_analyst_agent(config_list)
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        code_execution_config={
            "work_dir": "outputs",
            "use_docker": False,
        }
    )
    
    return analyst, user_proxy

def generate_analysis_prompt(analysis_type, custom_query=None):
    """Generate appropriate prompts based on analysis type"""
    base_context = """You are analyzing insurance data. Please provide clear explanations and save any visualizations to the outputs directory."""
    
    prompts = {
        "Basic Statistics": base_context + " Perform basic statistical analysis including summary statistics, distributions, and key insights.",
        "Visualization": base_context + " Create appropriate visualizations to show key patterns and relationships in the data.",
        "Prediction Model": base_context + " Build and evaluate a prediction model for the insurance score, explaining your methodology and results.",
        "Custom Query": base_context + f" Answer the following specific query: {custom_query}"
    }
    
    return prompts.get(analysis_type, prompts["Custom Query"])

def main():
    st.title("Insurance Data Analysis Assistant")
    
    # Sidebar for API key and file upload
    with st.sidebar:
        api_key = st.text_input("Enter your OpenAI API key", type="password")
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
        
        if uploaded_file is not None:
            st.session_state.data = pd.read_csv(uploaded_file)
            st.write("Data Preview:")
            st.dataframe(st.session_state.data.head())
        
        if api_key:
            if not st.session_state.agents_initialized:
                st.session_state.analyst, st.session_state.user_proxy = initialize_agents(api_key)
                st.session_state.agents_initialized = True
                st.success("Agents initialized successfully!")

    # Main chat interface
    st.subheader("Chat with your Data Analyst")
    
    # Analysis type selector
    analysis_type = st.selectbox(
        "Select Analysis Type",
        ["Basic Statistics", "Visualization", "Prediction Model", "Custom Query"]
    )
    
    # Custom query input if selected
    if analysis_type == "Custom Query":
        custom_query = st.text_input("Enter your specific query")
    else:
        custom_query = None
    
    # Message input
    message = st.chat_input("Ask me about your data...")
    
    # Display chat history
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.write(chat["content"])
            # Display images if any were generated
            if chat["role"] == "assistant":
                for file in os.listdir("outputs"):
                    if file.endswith((".png", ".jpg")):
                        st.image(f"outputs/{file}")
                        os.remove(f"outputs/{file}")  # Clean up after displaying
    
    # Handle new messages
    if message and st.session_state.agents_initialized and st.session_state.data is not None:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": message})
        
        # Generate appropriate prompt based on analysis type
        full_prompt = generate_analysis_prompt(analysis_type, custom_query)
        full_prompt += f"\n\nUser query: {message}"
        
        # Run analysis
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                st.session_state.user_proxy.initiate_chat(
                    st.session_state.analyst,
                    message=full_prompt
                )
                response = st.session_state.user_proxy.last_message()
                
                # Add assistant response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                # Display response
                st.write(response)
                
                # Display any generated images
                for file in os.listdir("outputs"):
                    if file.endswith((".png", ".jpg")):
                        st.image(f"outputs/{file}")
    
    # Display warnings if necessary
    if not api_key:
        st.warning("Please enter your OpenAI API key in the sidebar.")
    if st.session_state.data is None:
        st.warning("Please upload a CSV file in the sidebar.")

if __name__ == "__main__":
    # Create outputs directory if it doesn't exist
    os.makedirs("outputs", exist_ok=True)
    main()