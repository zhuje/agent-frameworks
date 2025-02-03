import os

APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT = os.environ.get("APP_PORT", 8005)
FAST_API_RELOAD=os.environ.get("FAST_API_RELOAD", True)


# Ollama Model configuration
MODEL_NAME=os.environ.get("MODEL_NAME", "llama3-groq-tool-use:8b-q8_0")
BASE_URL=os.environ.get("BASE_URL", "http://localhost:11434")
API_KEY=os.environ.get("API_KEY", None)
MODEL_TEMPERATURE=0


# LangGraph Memory Saver
THREAD_ID=os.environ.get("THREAD_ID")
CHECKPOINT_NS=os.environ.get("CHECKPOINT_NS")
CHECKPOINT_ID=os.environ.get("CHECKPOINT_ID")


BASE_PROMPT = """You are a helpful insurance agent.
Greet the customer.

When given an input, first call the 'scorer' tool to generate an insurability score.
Then call the 'approver' tool to decide if the application should be approved.

Always call these functions rather than providing a direct answer.
"""
