from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import yaml
import requests
import os

load_dotenv()

class AgentName(str, Enum):
    scorer = "scorer"
    approver = "approver"

class Agent(BaseModel):
    name: str = Field(examples = ["scorer"])
    role: str = Field(examples = ["You are an expert insurance agent"])
    goal: str = Field(examples = ["You score users based on how good they are as insurance customers"])
    backstory: str = Field(examples = ["You've been working for Parasol Insurance for for 20 years"])
    tools: list = Field(examples= [["RandomNumber"]])

class TaskName(str, Enum):
    score_task = "score_task"
    approval_task = "approval_task"
    plan_task = "plan_task"

class Task(BaseModel):
    name: str = Field(examples = ["task"])
    description: str = Field(examples = ["Task Description"])
    expected_output: str = Field(examples = ["Expected Output"])
    agent: str = Field(examples = ["agent"])
    context: list = Field(examples = [[""]])

class ToolName(str, Enum):
    webSearch = "webSearch"
    vectordbSearch = "vectordbSearc"
    RandomNumber = "RandomNumber"

class Tool(BaseModel):
    name: str = Field(examples = ["RandomNumber"])
    input_args: list = Field(examples = ["number"] )

class LLMName(str, Enum):
    local = "local"
    remote = "remote"

class LLM(BaseModel):
    name: str = Field(examples = ["local"]) 
    model: str = Field(examples=["model_name"])
    base_url: str = Field(examples=["http://localhost:8001/v1"])

local = LLM(
    name = "local",
    model = os.getenv("MODEL_NAME"),
    base_url = os.getenv("BASE_URL"),
)

RandomNumber = Tool(
    name = "RandomNumber",
    input_args=["number"])

db = {"tools": [RandomNumber],
      "agents": [],
      "tasks": [],
      "llms": [local]}

def initialize_db(agent_config, task_config, db):
    with open(agent_config, "r") as file:
        agents = yaml.safe_load(file)
    for agent in agents:
        new_agent = Agent(
            name = agent,
            role = agents[agent]["role"],
            goal = agents[agent]["goal"],
            backstory = agents[agent]["backstory"],
            tools = agents[agent]["tools"],
        )
        db["agents"].append(new_agent)
    
    with open(task_config, "r") as file:
            tasks = yaml.safe_load(file)
    for task in tasks:
        new_task = Task(
            name = task,
            description = tasks[task]["description"],
            expected_output = tasks[task]["expected_output"],
            agent = tasks[task]["agent"],
            context = tasks[task]["context"],
        )
        db["tasks"].append(new_task)

initialize_db("compiled_crew/config/agents.yaml",
              "compiled_crew/config/tasks.yaml",
              db)

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Welcome to the Parasol Insurance Agent Hub!"}

@app.get("/db")
async def get_data():
    return db

## Agents
@app.get("/agents")
async def get_agents():
    return db["agents"]

@app.get("/agents/{agent_name}")
async def get_agent(agent_name: AgentName):
    requested_agent = [agent for agent in db["agents"] if agent.name == agent_name ]
    if not requested_agent:
        return {"message": f"The agent {agent_name.name} does not exist"}
    return requested_agent[0]

@app.get("/llm/{llm_name}")
async def get_llm(llm_name: LLMName):
    requested_llm = [llm for llm in db["llms"] if llm.name == llm_name ]
    if not requested_llm:
        return {"message": f"The llm {llm_name.name} does not exist"}
    return requested_llm[0]

@app.post("/agents/new/{agent_name}")
async def add_agent(agent: Agent):
    
    requested_agent = [ x for x in db["agents"] if x.name == agent.name ]
    if requested_agent:
        return {"message": f"Agent {agent.name} already exists!"}
    
    new_agent = Agent(name = agent.name,
                      role = agent.role,
                      goal = agent.goal,
                      backstory = agent.backstory,
                      tools = agent.tools 
                      )

    db["agents"].append(new_agent)
    return {"message": "f{new_agent.name} added to database",
            "agent": new_agent}

@app.post("/update_agent_config")
async def update_agents_config():
    output_new = ""
    for agent in db["agents"]:
        entry = f"""{agent.name}:
  role: {agent.role}
  goal: {agent.goal}
  backstory: {agent.backstory}
"""
        if agent.tools:
            entry += f"""  tools: {agent.tools}
"""
        else:
            entry += """  tools: []
"""
        output_new += entry+"\n"
    
    with open("compiled_crew/config/agents.yaml", "w") as f:
        f.write(output_new)
    
    return {"message": "agents config added to database"}

### Tasks 
@app.get("/tasks")
async def get_tasks():
    return db["tasks"]

@app.post("/tasks/new/{task_name}")
async def add_task(task: Task):
    
    requested_task = [ x for x in db["tasks"] if x.name == task.name ]
    if requested_task:
        return {"message": f"task {task.name} already exists!"}
    
    new_task = Task(name = task.name,
                      description = task.description,
                      expected_output = task.expected_output,
                      agent = task.agent,
                      context = task.context)

    db["tasks"].append(new_task)
    return {"message": "f{new_task.name} added to database",
            "task": new_task}

@app.post("/update_task_config")
async def update_task_config():
    output_new = ""
    for task in db["tasks"]:
        entry = f"""{task.name}:
  description: {task.description}
  expected_output: {task.expected_output}
  agent: {task.agent}
"""
        if task.context:
            entry += f"""  context: {task.context}
"""
            print(task.context)
        else:
            entry += """  context: []
"""
        output_new += entry+"\n"
    
    with open("compiled_crew/config/tasks.yaml", "w") as f:
        f.write(output_new)
    
    return {"message": "tasks config added to database"}

### Tools

@app.get("/tools")
async def get_tools():
    return db["tools"]

@app.get("/tools/{tool_name}")
async def get_tool(tool_name: ToolName):
    requested_tool = [tool for tool in db["tools"] if tool.name == tool_name ]
    if not requested_tool:
        return {"message": f"The tool {tool_name.name} does not exist"}
    return requested_tool[0]


### Compile + Run

@app.post("/compile")
def compile_crew():
    from crewai_builder import agent_factory, task_factory, tool_factory, crew_compiler
    
    r = requests.get(url="http://localhost:8000/agents")
    agent_list = yaml.safe_load(r.content)
    agent_blocks = agent_factory(agent_list=agent_list)

    r = requests.get(url="http://localhost:8000/tasks")
    task_list = yaml.safe_load(r.content)
    task_blocks = task_factory(task_list=task_list)

    r = requests.get(url="http://localhost:8000/tools")
    tool_list = yaml.safe_load(r.content)
    tool_blocks = tool_factory(tool_list=tool_list)
    
    crew_compiler("compiled_crew/test_compiled_crew.py", "compiled_crew", agent_blocks, task_blocks, tool_list, tool_blocks)

    return {"message": "compiled crew"}

@app.post("/run")
def run_crew(topic:str = "AI LLMS"):
    from compiled_crew.test_compiled_crew import ConstructedCrew
    inputs = {
        'topic' : topic
    }

    agent_response = ConstructedCrew().crew().kickoff(inputs=inputs,)
    return {"agent_response": agent_response}
