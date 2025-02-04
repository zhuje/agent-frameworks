from fastapi import FastAPI
import yaml
import custom_tools
from inspect import getmembers, isfunction
from pydantic import BaseModel, Field 

class Agent(BaseModel):
    name: str = Field(examples = ["approver"])
    system_prompt: str = Field(examples=["Hey"])
    tools: list = Field(examples =[[]])

class Task(BaseModel):
    name: str = Field(examples = ["approve"])
    description: str = Field(examples =[""])
    expected_output: str = Field(examples = [""])
    agent: str = Field(examples = ["scorer"])

app = FastAPI()

@app.get("/agents")
def get_agents():
    with open("agents.yaml", "r", encoding='utf-8') as file:
        yaml_file = yaml.safe_load(file)
    agents_list = [agent for agent in yaml_file]
    return {"agents": agents_list}

@app.get("/agents/{agent_name}")
def get_agent(agent_name):
    with open("agents.yaml", "r", encoding='utf-8') as file:
        yaml_file = yaml.safe_load(file)
    return {"agent": yaml_file[agent_name]}

@app.post("/agents/{agent_name}")
async def update_agent(agent: Agent, agent_name):
    with open("agents.yaml", "r", encoding='utf-8') as file:
        yaml_file = yaml.safe_load(file)
    
    if agent_name != agent.name:
        return "names must match"
    yaml_file[agent_name]["system_prompt"] = agent.system_prompt
    yaml_file[agent_name]["tools"] = agent.tools

    with open("agents.yaml", "w", encoding='utf-8') as file:
        yaml.safe_dump(yaml_file, file)
    
    return {"message": f"{agent_name} updated."}

@app.get("/tasks")
def get_tasks():
    with open("tasks.yaml", "r", encoding="utf-8") as file:
        yaml_file = yaml.safe_load(file)
    tasks_list = [task for task in yaml_file]
    return {"tasks": tasks_list}

@app.get("/tasks/{task_name}")
def get_task(task_name):
    with open("tasks.yaml", "r", encoding = "utf-8") as file:
        yaml_file = yaml.safe_load(file)
    return {"task": yaml_file[task_name]}

@app.post("/tasks/{task_name}")
def update_task(task: Task, task_name):
    with open("tasks.yaml", "r", encoding='utf-8') as file:
        yaml_file = yaml.safe_load(file)

    if task_name != task.name:
        return "Names must match"
    yaml_file[task_name]["description"] = task.description
    yaml_file[task_name]["expected_output"] = task.expected_output
    yaml_file[task_name]['agent'] = task.agent

    with open("tasks.yaml", "w", encoding='utf-8') as file:
        yaml.safe_dump(yaml_file, file)

    return {"message": f"{task_name} updated."}

@app.get("/tools")
def get_tools():
    tools = getmembers(custom_tools, isfunction)
    tools_list = [tool[0] for tool in tools]
    return {"tools": tools_list}

@app.post("/compile_workflow")
def compile():
    from compile_workflow import compile_workflow
    compile_workflow()

@app.post("/run_workflow")
def workflow():
    from compiled_workflow_test import run
    return run()
