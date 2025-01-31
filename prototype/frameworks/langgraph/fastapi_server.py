# fastapi_server.py

from fastapi import FastAPI, Body
from typing import Optional, Dict

import uvicorn

# Import the workflow runner
from insurance_workflow import run_insurance_workflow

app = FastAPI(title="Insurance Automation")

# In-memory store for definitions (Agents, Tools, Workflows)
DEFINITIONS_STORE: Dict[str, dict] = {
    "agents": {},
    "tools": {},
    "workflows": {}
}

@app.get("/")
def read_root():
    return {"msg": "Hello from Insurance Automation FastAPI!"}

# ---------- Agents ----------
@app.post("/definitions/agents/")
def create_agent(name: str, description: Optional[str] = None):
    if name in DEFINITIONS_STORE["agents"]:
        return {"error": f"Agent '{name}' already exists."}
    DEFINITIONS_STORE["agents"][name] = {
        "name": name,
        "description": description or "No description",
    }
    return {"message": f"Agent '{name}' created successfully."}

@app.get("/definitions/agents/")
def list_agents():
    return DEFINITIONS_STORE["agents"]

# ---------- Tools ----------
@app.post("/definitions/tools/")
def create_tool(name: str, description: Optional[str] = None):
    if name in DEFINITIONS_STORE["tools"]:
        return {"error": f"Tool '{name}' already exists."}
    DEFINITIONS_STORE["tools"][name] = {
        "name": name,
        "description": description or "No description",
    }
    return {"message": f"Tool '{name}' created successfully."}

@app.get("/definitions/tools/")
def list_tools():
    return DEFINITIONS_STORE["tools"]

# ---------- Workflows ----------
@app.post("/definitions/workflows/")
def create_workflow(name: str, description: Optional[str] = None):
    if name in DEFINITIONS_STORE["workflows"]:
        return {"error": f"Workflow '{name}' already exists."}
    DEFINITIONS_STORE["workflows"][name] = {
        "name": name,
        "description": description or "No description",
        # Potentially store a reference to actual logic, or config
    }
    return {"message": f"Workflow '{name}' created successfully."}

@app.get("/definitions/workflows/")
def list_workflows():
    return DEFINITIONS_STORE["workflows"]

# ---------- Run Our Insurance Workflow ----------
@app.post("/run_insurance_workflow/")
def run_workflow(user_input: str = Body(..., embed=True)):
    """
    Endpoint to run the pre-defined insurance workflow with the
    user's text input. Returns the list of messages from the AI.
    """
    messages = run_insurance_workflow(user_input)
    return {"messages": messages}

# For local debugging
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
