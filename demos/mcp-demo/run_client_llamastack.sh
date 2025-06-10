#!/bin/bash

# Instructions from: https://llama-stack.readthedocs.io/en/latest/getting_started/detailed_tutorial.html

# Run LLama Stack Client 
uv venv client 
source client/bin/activate
pip install llama-stack-client

llama-stack-client configure --endpoint http://localhost:8321 --api-key none

# Test
echo "Testing llama stack client by asking it to 'tell me a joke'" 
llama-stack-client inference chat-completion --message "tell me a joke"
