import yaml
import custom_tools
from inspect import getmembers, isfunction

def get_tools():
    tools = getmembers(custom_tools, isfunction)
    tools_list = [tool[0] for tool in tools]
    return f"from custom_tools import {", ".join(tools_list)}"

def agent_factory(agent_file):
    with open(agent_file, "r") as file:
        agents = yaml.safe_load(file)
    
    result = ""
    for agent in agents:
        tools = ", ".join(agents[agent]["tools"])
        agent_template = f"""
{agent} = Agent(
    model,
    system_prompt="{agents[agent]["system_prompt"]}",
    tools=[{tools}],
    model_settings={agents[agent]["model_setting"]},
    )
"""
        result += agent_template
    
    return result
        

def build_runner(tasks_file):
    with open(tasks_file, "r") as file:
        tasks = yaml.safe_load(file)
    result = """def run():
    """
    for i, task in enumerate(tasks):
        if i == 0:
            run_template = f"""{task}_result = asyncio.run({tasks[task]["agent"]}.run(f'{tasks[task]["description"]} \\n {tasks[task]["expected_output"]}'))
    history = {task}_result.new_messages()
"""
        else:
            run_template = f"""
    {task}_result = asyncio.run({tasks[task]["agent"]}.run(f'{tasks[task]["description"]} \\n {tasks[task]["expected_output"]}',message_history=history))
"""
        
        result += run_template
    
    output_message = f""""message": {task}_result.data"""
    output = f"""
    return {{{output_message}}}"""
    result += output
    
    return result
    

def compile_workflow():

    imports = """from pydantic_ai import Agent, Tool
from pydantic_ai.messages import ToolCallPart, ToolReturnPart
from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv
import asyncio
import random
import json
import os

load_dotenv()
"""

    models = """
## Model
model = OpenAIModel(
    model_name=os.getenv("MODEL_NAME"),
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
)"""

    tool_imports = get_tools()
    agents = agent_factory("agents.yaml")
    run = build_runner("tasks.yaml")

    workflow_file =  f"""{imports}
{tool_imports}
{models}
{agents}
{run}
"""

    with open("compiled_workflow_test.py", "w") as file:
        file.write(workflow_file)
