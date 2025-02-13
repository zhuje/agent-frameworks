# Llama Stack Setup Guide

This guide will walk you through setting up and running the Llama Stack with Ollama using Podman instead of Docker.

---

## **1. Prerequisites**
Ensure you have the following installed:
- **Podman** (instead of Docker)
- **Python 3.10+**
- **pip** (latest version)
- **Ollama** ([Install Ollama](https://ollama.com/download))

Verify installation:
```bash
podman --version
python3 --version
pip --version
```

---

## **2. Start Ollama**
Before running Llama Stack, start the Ollama server with:
```bash
ollama run llama3.2:3b-instruct-fp16 --keepalive 60m
```
This ensures the model stays loaded in memory for 60 minutes.

---

## **3. Set Up Environment Variables**
Set up the required environment variables:
```bash
export INFERENCE_MODEL="meta-llama/Llama-3.2-3B-Instruct"
export LLAMA_STACK_PORT=8321
```

---

## **4. Run Llama Stack Server with Podman**
Pull the required image:
```bash
podman pull docker.io/llamastack/distribution-ollama
```
Run the server using:
```bash
podman run --privileged -it \
  -p $LLAMA_STACK_PORT:$LLAMA_STACK_PORT \
  -v ~/.llama:/root/.llama \
  --env INFERENCE_MODEL=$INFERENCE_MODEL \
  --env OLLAMA_URL=http://host.containers.internal:11434 \
  llamastack/distribution-ollama \
  --port $LLAMA_STACK_PORT
```
If needed, create and use a network:
```bash
podman network create llama-net
podman run --privileged --network llama-net -it \
  -p $LLAMA_STACK_PORT:$LLAMA_STACK_PORT \
  llamastack/distribution-ollama \
  --port $LLAMA_STACK_PORT
```

Verify the container is running:
```bash
podman ps
```

---

## **5. Set Up Python Environment**
Create a virtual environment using `venv`:
```bash
python3 -m venv llama-stack-env
source llama-stack-env/bin/activate  # macOS/Linux
# On Windows: llama-stack-env\Scripts\activate
```
Install Llama Stack Client:
```bash
pip install --upgrade pip
pip install llama-stack-client
```
Verify installation:
```bash
pip list | grep llama-stack-client
```

---

## **6. Configure the Client**
Set up the client to connect to the Llama Stack server:
```bash
llama-stack-client configure --endpoint http://localhost:$LLAMA_STACK_PORT
```
List available models:
```bash
llama-stack-client models list
```

---

## **7. Run a RAG Agent**
Run the Python script (`rag.py`):
```python
import os
import uuid
from pathlib import Path
from termcolor import cprint
from dotenv import load_dotenv
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client.types.agent_create_params import AgentConfig
from llama_stack_client.types import Document

load_dotenv()

# Configuration
LLAMA_STACK_PORT = os.environ.get("LLAMA_STACK_PORT", "8321")
INFERENCE_MODEL = os.environ.get("INFERENCE_MODEL", "meta-llama/Llama-3.2-3B-Instruct")
FILE_PATHS = ["document/cake.rst", "document/car.rst", "document/house.rst", "document/technology.rst"]
VECTOR_DB_PROVIDER = "faiss"
EMBEDDING_MODEL = "/Users/kcogan/.llama/checkpoints/sentence-transformers/all-MiniLM-L6-v1"
EMBEDDING_DIMENSION = 384
CHUNK_SIZE = 512
TOP_K = 3
MAX_TOKENS_IN_CONTEXT = 4096
MAX_CHUNKS = 2


def create_http_client():
    from llama_stack_client import LlamaStackClient
    return LlamaStackClient(base_url=f"http://localhost:{LLAMA_STACK_PORT}")


def create_library_client(template="ollama"):
    from llama_stack import LlamaStackAsLibraryClient
    client = LlamaStackAsLibraryClient(template)
    client.initialize()
    return client


client = create_library_client()  # or create_http_client() depending on the environment

# Load documents for RAG
documents = [
    Document(
        document_id=f"num-{i}",
        content=Path(file_path).read_text(encoding="utf-8"),
        mime_type="text/plain",
        metadata={}
    )
    for i, file_path in enumerate(FILE_PATHS) if Path(file_path).exists()
]

# Print warnings for missing files
missing_files = [file for file in FILE_PATHS if not Path(file).exists()]
if missing_files:
    print(f"Warning: {', '.join(missing_files)} not found. Skipping...")

# Register a vector database
vector_db_id = f"test-vector-db-{uuid.uuid4().hex}"
client.vector_dbs.register(
    provider_id=VECTOR_DB_PROVIDER,
    vector_db_id=vector_db_id,
    embedding_model=EMBEDDING_MODEL,
    embedding_dimension=EMBEDDING_DIMENSION,
)

# Insert documents into the vector database
client.tool_runtime.rag_tool.insert(
    documents=documents,
    vector_db_id=vector_db_id,
    chunk_size_in_tokens=CHUNK_SIZE,
)

# Define agent configuration
agent_config = AgentConfig(
    model=INFERENCE_MODEL,
    instructions=(
        "You are a highly reliable, concise, and precise assistant. "
        "When answering user queries, adhere to the following guidelines:\n"
        "1. **Strict Context Usage**: Base your response exclusively on the provided retrieved context.\n"
        "2. **Clarity and Brevity**: Provide clear, focused, and concise responses.\n"
        "3. **Handling Insufficient Information**: If the context lacks sufficient details, state that the necessary information is unavailable.\n"
        "4. **Avoid Inference or Speculation**: Stick to explicit context without speculation.\n"
        "5. **Disambiguation**: If a query is ambiguous, seek clarification before responding.\n"
        "6. **Neutral Tone**: Maintain objectivity in your responses.\n"
        "7. **User-Centric**: Ensure accessibility and clarity for a general audience.\n"
    ),
    enable_session_persistence=False,
    max_infer_iters=2,
    toolgroups=[
        {
            "name": "builtin::rag",
            "args": {
                "vector_db_ids": [vector_db_id],
                "top_k": TOP_K,
                "query_config": {
                    "max_tokens_in_context": MAX_TOKENS_IN_CONTEXT,
                    "max_chunks": MAX_CHUNKS,
                    "query_generator_config": {
                        "type": "default",
                        "separator": "\n"
                    }
                }
            }
        }
    ],
    tool_choice="auto"
)

rag_agent = Agent(client, agent_config)
session_id = rag_agent.create_session("test-session")

user_prompts = [
    "Give me a recipe to make a cake step by step.",
]

# Run the agent loop
for prompt in user_prompts:
    cprint(f"User> {prompt}", "green")
    response = rag_agent.create_turn(
        messages=[{"role": "user", "content": prompt}],
        session_id=session_id,
    )
    for log in EventLogger().log(response):
        log.print()

# Unregister all vector databases
for item in client.vector_dbs.list():
    print(f"Unregistering vector database: {item.identifier}")
    client.vector_dbs.unregister(vector_db_id=item.identifier)

```
Run the script:
```bash
python rag.py
```

---
## **7. Run a Llama-Stack Code Interpreter Agent**
Run the Python script (`coding-agent.py`):
```python
import os
import sys
from termcolor import cprint  # Used for colored terminal output
from llama_stack_client import LlamaStackClient  # Main client for Llama Stack
from llama_stack_client.lib.agents.agent import Agent  # Agent class for AI interactions
from llama_stack_client.lib.agents.event_logger import EventLogger  # Event logging utility
from llama_stack_client.types.agent_create_params import AgentConfig  # Configuration for agent creation
from llama_stack_client.types import Document  # Document type for Llama Stack interactions
import uuid  # For generating unique identifiers


def create_http_client():
    """Creates an HTTP client for communicating with the Llama Stack server."""
    from llama_stack_client import LlamaStackClient

    return LlamaStackClient(
        base_url=f"http://localhost:{os.environ['LLAMA_STACK_PORT']}"
    )


def create_library_client(template="ollama"):
    """Creates a library-based client for Llama Stack."""
    from llama_stack import LlamaStackAsLibraryClient

    client = LlamaStackAsLibraryClient(template)
    if not client.initialize():
        print("Llama Stack not built properly")
        sys.exit(1)
    return client


# Initialize the Llama Stack client, choosing between library or HTTP client
client = create_http_client()  # Switch to create_library_client() if needed

# Define agent configuration
agent_config = AgentConfig(
    model=os.getenv("INFERENCE_MODEL"),  # Fetch model from environment variable
    instructions=(
        "You are a highly reliable, concise, and precise assistant always show the generated code presented to you never generate your own code and never anticipate the result. "
        "When answering user queries, adhere to the following guidelines:\n"
        "1. **Strict Context Usage**: Base your response exclusively on the provided retrieved context.\n"
        "2. **Clarity and Brevity**: Provide clear, focused, and concise responses.\n"
        "3. **Handling Insufficient Information**: If the context lacks sufficient details, state that the necessary information is unavailable.\n"
        "4. **Avoid Inference or Speculation**: Stick to explicit context without speculation.\n"
        "5. **Disambiguation**: If a query is ambiguous, seek clarification before responding.\n"
        "6. **Neutral Tone**: Maintain objectivity in your responses.\n"
        "7. **User-Centric**: Ensure accessibility and clarity for a general audience.\n"
    ),  # General AI instructions
    
    # Enable tool usage for additional functionalities (e.g., RAG, code execution)
    toolgroups=[
        "builtin::code_interpreter",  # Enables execution of code within the AI
    ],
    
    max_infer_iters=5,  # Maximum inference iterations per response
    
    sampling_params={  # Defines sampling strategy for AI response generation
        "strategy": {"type": "greedy", "temperature": 0.7, "top_p": 0.95},
        "max_tokens": 2048,  # Token limit per response
    },
    enable_session_persistence=True  # Ensures session persistence across interactions
)

# Create an agent instance with the configured settings
agent = Agent(client, agent_config)

# Start a monitored session
session_id = agent.create_session("monitored_session")

# Send a user query to the AI agent
response = agent.create_turn(
    messages=[{"role": "user", 
               "content": """Run this code: import requests

# URL of the website you want to scrape
url = "https://example.com"  # Replace with your target URL

# Send a GET request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Website Content:")
    print(response.text)  # Print the HTML content
else:
    print(f"Failed to retrieve the website. Status code: {response.status_code}")

"""
               }],
    session_id=session_id,  # Ensure session ID is correctly passed
)

# Monitor and log each execution step
for log in EventLogger().log(response):
    log.print()
```
Run the script:
```bash
python code-agent.py
```
---

## **9. Debugging Common Issues**
**Check if Podman is Running:**
```bash
podman ps
```

**Ensure the Virtual Environment is Activated:**
```bash
source llama-stack-env/bin/activate
```

**Reinstall the Client if Necessary:**
```bash
pip uninstall llama-stack-client
pip install llama-stack-client
```

**Test Importing the Client in Python:**
```bash
python -c "from llama_stack_client import LlamaStackClient; print(LlamaStackClient)"
```

---
