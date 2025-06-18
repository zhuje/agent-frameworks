#!/bin/bash

# Instructions from: https://llama-stack.readthedocs.io/en/latest/getting_started/detailed_tutorial.html

# Pull model # TODO check if image already exists and check if its already running 
ollama pull llama3.2:3b
ollama pull llama3.2:3b-instruct-fp16
nohup ollama run llama3.2:3b --keepalive 60m > ollama.log 2>&1 &
ollama ps 

# Setup Virtual environment 
# uv init #  TODO: create a condition around this to check if already initiatlized 
uv sync 
source .venv/bin/activate

# Variables 
export INFERENCE_MODEL="llama3.2:3b"
export LLAMA_STACK_PORT=8321
mkdir -p ~/.llama

# Run ollama stack 
linux_docker_cmd="docker run -it \
  --pull always \
  -p $LLAMA_STACK_PORT:$LLAMA_STACK_PORT \
  -v ~/.llama:/root/.llama \
  --network=host \
  llamastack/distribution-ollama \
  --port $LLAMA_STACK_PORT \
  --env INFERENCE_MODEL=$INFERENCE_MODEL \
  --env OLLAMA_URL=http://localhost:11434"

## TODO: Need to create condition to get OS for image to pull AMD or ARM 
docker_cmd="docker run -it \
    --platform linux/amd64 \
    --pull always \
    -p $LLAMA_STACK_PORT:$LLAMA_STACK_PORT \
    -v ~/.llama:/root/.llama \
    llamastack/distribution-ollama:0.2.7 \
    --port $LLAMA_STACK_PORT \
    --env INFERENCE_MODEL=$INFERENCE_MODEL \
    --env OLLAMA_URL=http://host.docker.internal:11434"

podman_cmd="podman run -it \
        --pull always \
        -p $LLAMA_STACK_PORT:$LLAMA_STACK_PORT \
        -v ~/.llama:/root/.llama \
        llamastack/distribution-ollama \
        --port $LLAMA_STACK_PORT \
        --env INFERENCE_MODEL=$INFERENCE_MODEL \
        --env OLLAMA_URL=http://host.container.internal:11434"

if command -v docker &> /dev/null && docker info &> /dev/null; then
  echo "Using container engine: Docker"
  eval "$docker_cmd"
elif command -v podman &> /dev/null && podman info &> /dev/null; then
    echo "Using container engine: Podman"
    eval "$podman_cmd"
else
  echo "Neither Docker nor Podman is installed or running. Exiting script..."
  exit 1 
fi

