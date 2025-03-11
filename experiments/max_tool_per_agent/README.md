# Evaluating Tool Selection and Scalability in LlamaStack
## Objective
Assess LlamaStack’s ability to handle an increasing number of tools, evaluate tool selection accuracy, and determine whether providing a subset of relevant tools as input improves performance. Also how model series, model size affect performance.
## Key Research Questions
* Scalability: What is the maximum number of tools an agent can handle before performance degrades?
* Tool Selection Accuracy: How well does the agent pick the correct tool for a given query?
* Guided Tool Selection: Does providing a relevant subset of tools in the prompt improve accuracy?
* Model factor: How does model architecture (series, size) affect LlamaStack's tool execution and selection performance?
## Methodology
* Tools:  
  - 3 built-in tools (websearch, wolfram_alpha, code_interpreter).  
  - Dynamically generated N client tools to test scalability (N = 5, 10, 20, 50).
  - also mcp tools (less priority)
* Queries:  
A diverse set of tasks designed to require specific tools.
* Metrics:  
  - Scalability Limit (max tool count before performance drops).  
  - Tool Selection Accuracy (% correct, incorrect, or missing tool calls by assert response.steps).  
  - Latency (response time vs. tool count).
* Logging:  
Structured logs (CSV/JSON) capturing query, available tools, selected tool, expected tool, execution success, and latency.


Currently, we have multiple builtin tool script available. more systematic evaluation still WIP.

### Test multi-builtin-tool
The current version works with 0.1.6. If running with previous versions, ensure that `run.yaml` has all three tools configured.
step 1. `ollama run llama3.2:3b-instruct-fp16 --keepalive 60m`
step 2.
```
export INFERENCE_MODEL="meta-llama/Llama-3.2-3B-Instruct"
export LLAMA_STACK_PORT=8321
```
step 3: `llama stack run --image-type conda ~/llama-stack/llama_stack/templates/ollama/run.yaml` (I'm using conda env, follow this(https://llama-stack.readthedocs.io/en/latest/distributions/building_distro.html) if not using conda)
step 4: run `python multi-builtintools.py`