# This file is generate running crewai_builder.crew_compiler(). 
# Do not make changes directly to this file.
import requests
import json
import os
from dotenv import load_dotenv

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, tool
from .tools.custom_tools import RandomNumber

load_dotenv()

@CrewBase
class ConstructedCrew():
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    
    @tool
    def RandomNumber(number):
        return RandomNumber()
    
    
    @agent
    def scorer(self) -> Agent:
        llm = LLM(
        model = os.getenv("MODEL_NAME"),
        api_key = os.getenv("API_KEY"),
        base_url = os.getenv("BASE_URL"),)
        return Agent(
            config = self.agents_config["scorer"],
            verbose = True,
            llm = llm
        )
    
    
    @task
    def score_task(self) -> Task:
        return Task(
            config = self.tasks_config["score_task"],
        )
    

    @crew
    def crew(self) -> Crew:
        return Crew(
        agents = self.agents,
        tasks = self.tasks,
        process = Process.sequential,
        verbose=True,)

