from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client.types.agent_create_params import AgentConfig
from termcolor import cprint
import os
from llama_stack_client import LlamaStackClient
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Access the environment variables
inference_model = os.getenv("INFERENCE_MODEL")
llama_stack_port = os.getenv("LLAMA_STACK_PORT")
ollama_url = os.getenv("OLLAMA_URL")
tavily_search_api_key = os.environ["TAVILY_SEARCH_API_KEY"]

print(f"Model: {inference_model}")
print(f"Llama Stack Port: {llama_stack_port}")
print(f"Ollama URL: {ollama_url}")

# Initialize the Llama Stack client, choosing between library or HTTP client
client = LlamaStackClient(
        base_url=f"http://localhost:{llama_stack_port}", # return LlamaStackClient(base_url="http://localhost:8321", timeout = 6000)
        provider_data = {"tavily_search_api_key": tavily_search_api_key}  # according to https://llama-stack.readthedocs.io/en/latest/building_applications/tools.html
    )

# `agent_config` is deprecated. Use inlined parameters instead.
agent = Agent(
    client, 
    model=os.getenv("INFERENCE_MODEL"),
    instructions=(
        "You are a highly knowledgeable and helpful web search assistant. "
        "Your primary goal is to provide accurate and reliable information to the user. "
        "Whenever you encounter a query, make sure to use the websearch tools specifically use travil search tool to look up the most current and precise information available. "
        "name the tool called."
    ),
    tools=["builtin::websearch"],
)

user_prompts = [
    "Hello",
    "How US performed in the olympics?",
]

session_id = agent.create_session("test-session")
for prompt in user_prompts:
    cprint(f"User> {prompt}", "green")
    response = agent.create_turn(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        session_id=session_id,
    )
    for log in EventLogger().log(response):
        log.print()