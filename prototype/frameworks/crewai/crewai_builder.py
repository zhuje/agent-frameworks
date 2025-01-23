from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, tool
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

def agent_factory(agent_list):
    agent_blocks = ""
    
    for agent in agent_list:
        agent_block = f"""
    @agent
    def {agent['name']}(self) -> Agent:
        llm = LLM(
        model = os.getenv("MODEL_NAME"),
        api_key = os.getenv("API_KEY"),
        base_url = os.getenv("BASE_URL"),)
        return Agent(
            config = self.agents_config["{agent['name']}"],
            verbose = True,
            llm = llm
        )
    """
        agent_blocks += agent_block
    
    return agent_blocks

def task_factory(task_list):
    task_blocks = ""
    
    for task in task_list:
        task_block = f"""
    @task
    def {task['name']}(self) -> Task:
        return Task(
            config = self.tasks_config["{task['name']}"],
        )
    """
        task_blocks += task_block
    
    return task_blocks

def tool_factory(tool_list):
    tool_blocks = ""
    
    for tool in tool_list:
        tool_args = "".join(tool["input_args"])
        tool_block = f"""
    @tool
    def {tool['name']}({tool_args}):
        return {tool["name"]}()
    """
        tool_blocks += tool_block
    
    return tool_block


def crew_compiler(file_name: str,
                  directory: str,
                  agent_blocks: str,
                  task_blocks: list,
                  tool_list: list,
                  tool_blocks: list,
                  crew_name: str = "ConstructedCrew"):
    
    imports = f"""# This file is generate running crewai_builder.crew_compiler(). 
# Do not make changes directly to this file.
import requests
import json
import os
from dotenv import load_dotenv

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, tool
from .tools.custom_tools import {"".join([tool["name"] for tool in tool_list])}

load_dotenv()
""" 

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    crew_py = f"""{imports}
@CrewBase
class {crew_name}():
    agents_config = "{agents_config}"
    tasks_config = "{tasks_config}"

    {tool_blocks}
    {agent_blocks}
    {task_blocks}

    @crew
    def crew(self) -> Crew:
        return Crew(
        agents = self.agents,
        tasks = self.tasks,
        process = Process.sequential,
        verbose=True,)

"""
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(crew_py)
    with open(f"{directory}/__init__.py", "w", encoding="utf-8") as f:
        f.write("# empty init\n")
    
    return 0





