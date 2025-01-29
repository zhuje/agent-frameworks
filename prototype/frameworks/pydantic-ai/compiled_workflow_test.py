from pydantic_ai import Agent, Tool
from pydantic_ai.messages import ToolCallPart, ToolReturnPart
from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv
import asyncio
import random
import json
import os

load_dotenv()

from custom_tools import generate_random_number, is_approved

## Model
model = OpenAIModel(
    model_name=os.getenv("MODEL_NAME"),
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
)

approver = Agent(
    model,
    system_prompt="You approve everything above 50.",
    tools=[is_approved],
    model_settings={},
    )

scorer = Agent(
    model,
    system_prompt="You score everything",
    tools=[generate_random_number],
    model_settings={},
    )

def run():
    approve_result = asyncio.run(approver.run(f'you approve everything \n Approve(value=score)'))
    history = approve_result.new_messages()

    score_result = asyncio.run(scorer.run(f'you score everything. \n Must be a structured in the following format: Score(value=score)',message_history=history))

    return {"message": score_result.data}
