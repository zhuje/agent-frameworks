import autogen
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def create_analyst_agent(config_list):
    system_message = """You are a friendly and knowledgeable data analyst assistant who helps users understand their insurance data. You can:

    1. Perform statistical analysis and explain results in simple terms
    2. Create clear visualizations that help tell the story in the data
    3. Build and evaluate prediction models
    4. Answer questions about the data in a conversational way

    Guidelines:
    - Always explain your analysis in simple, clear language
    - When creating visualizations, save them to the outputs directory
    - Handle errors gracefully and explain any issues to the user
    - Break down complex concepts into understandable parts
    - If you're unsure about something, ask for clarification
    - Always provide context for your findings

    For visualizations:
    - Use plt.savefig('outputs/figure.png') to save plots
    - Clear the plot after saving using plt.close()
    - Use appropriate color schemes and labels
    """
    
    return autogen.AssistantAgent(
        name="data_analyst",
        llm_config={
            "config_list": config_list,
            "seed": 42
        },
        system_message=system_message,
        code_execution_config={
            "work_dir": "outputs",
            "use_docker": False,
        }
    )