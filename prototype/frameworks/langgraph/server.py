import uuid
import copy
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Import the InsuranceAgent and State from our separate file
from agent import InsuranceAgent, State
from langchain_core.messages import AIMessage, HumanMessage
from constant import APP_HOST, APP_PORT, FAST_API_RELOAD

app = FastAPI()

# Enable CORS for development (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store mapping session IDs to their agent instance and current state.
sessions: Dict[str, Dict] = {}

# Pydantic models for API request and response bodies.
class ChatRequest(BaseModel):
    session_id: str
    message: str

class SessionResponse(BaseModel):
    session_id: str
    messages: List[Dict[str, str]]  # Each message as {"role": "...", "content": "..."}

def message_to_dict(message) -> Dict[str, str]:
    """
    Convert a message object (HumanMessage or AIMessage) to a dictionary.
    """
    role = "assistant"
    if isinstance(message, HumanMessage):
        role = "human"
    elif isinstance(message, AIMessage):
        role = "assistant"
    return {"role": role, "content": message.content}

@app.post("/start-session", response_model=SessionResponse)
def start_session():
    """
    Start a new chat session:
      - Create an InsuranceAgent instance.
      - Process the initial state (e.g. agent greeting).
      - Return a session ID and the initial conversation messages.
    """
    agent = InsuranceAgent()
    initial_state = copy.deepcopy(agent.initial_state)
    # Process the initial state (you can also call agent.process_turn if desired)
    config = {
        "configurable": {
            "thread_id": "unique_thread_identifier",
            "checkpoint_ns": "namespace_identifier",
            "checkpoint_id": "unique_checkpoint_identifier"
        }
    }
    state = agent.graph.invoke(initial_state, config=config)
    session_id = str(uuid.uuid4())
    sessions[session_id] = {"agent": agent, "state": state}
    messages = [message_to_dict(msg) for msg in state.get("messages", [])]
    return SessionResponse(session_id=session_id, messages=messages)

@app.post("/chat", response_model=SessionResponse)
def chat(chat_request: ChatRequest):
    """
    Process a chat turn:
      - Append the user's message to the state.
      - Invoke the agent's processing.
      - Return the updated conversation messages.
    """
    session_id = chat_request.session_id
    user_message = chat_request.message

    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    agent: InsuranceAgent = session["agent"]
    state = session["state"]

    new_state = agent.process_turn(state, user_input=user_message)
    session["state"] = new_state

    messages = [message_to_dict(msg) for msg in new_state.get("messages", [])]
    return SessionResponse(session_id=session_id, messages=messages)

@app.get("/session/{session_id}", response_model=SessionResponse)
def get_session(session_id: str):
    """
    (Optional) Retrieve the current conversation state for a given session.
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    state = session["state"]
    messages = [message_to_dict(msg) for msg in state.get("messages", [])]
    return SessionResponse(session_id=session_id, messages=messages)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host=APP_HOST, port=APP_PORT, reload=FAST_API_RELOAD)
