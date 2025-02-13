# 🚀 Agentic Frameworks Evaluation

## 🌍 Overview

This project evaluates multiple agentic frameworks for automating workflows using Large Language Models (LLMs). The goal is to assess their capabilities, limitations, and suitability for deploying AI-driven agents in real-world applications.

### 🔍 Frameworks Under Evaluation

- 🦙 **Llama-Stack**
- 🤖 **Autogen**
- 🐝 **BeeAI**
- 🤝 **Crewai**
- 🧠 **DSPy**
- 🔗 **Langgraph**
- 📚 **LlamaIndex**
- 🏗 **MCP-Agent**
- 🌐 **Open WebUI**
- 🛠 **Pydantic AI**

## 🦙 Llama-Stack: Agentic RAG & Code Interpreter Example

This `agent-frameworks/prototype/frameworks/llamastack` shows how to set up the Llama-Stack framework and run it with Podman as well as set up agentic RAG and the code interpreter.

## 🏦 Use Case: Insurance Automation

As an **Insurance Specialist at Parisol Insurance**, I want to:

1. **Create an AI-driven Agent** via a simple UI to automate key aspects of my workflow.
2. **Define and deploy multi-agent workflows** on OpenShift with minimal technical complexity.
3. **Use pre-defined tools and tasks** that allow agents to process insurance-related queries efficiently.

#### 🔍 Example Scenario

- I create an agent called **“Scorer”**  that generates a random insurability score (1-100) using a tool.
- The score is passed to another agent, **“Approver”** , which determines whether the score qualifies for insurance approval based on predefined logic (e.g., `if score > 50: return "approved"`).
- The **Approver** generates an acceptance or denial letter with a reason and returns it to the user.
- The entire process should be deployable on OpenShift without requiring complex LLM configurations—only specifying an endpoint for model inference.

### 🎯 Goals & Considerations

- Identify potential **limitations** and **bottlenecks** in each framework before committing to a long-term solution.
- The prototype should be a **client-server web application** using FastAPI (server) and Streamlit (client) for demonstration purposes.
- Ensure the solution is **modular**, **reusable**, and **extensible** for future automation tasks.

## 🛠 Framework Prototypes

The following frameworks are being evaluated:

- [🦙 Llama-Stack](./prototype/frameworks/llamastack/README.md) *(Setup Guide using Podman and Ollama)*
- [🤖 Autogen](./prototype/frameworks/autogen/README.md)
- [🐝 BeeAI](./prototype/frameworks/bee/README.md)
- [🤝 Crewai](./prototype/frameworks/crewai/README.md)
- [🧠 DSPy](./prototype/frameworks/dspy/README.md)
- [🔗 Langgraph](./prototype/frameworks/langgraph/README.md)
- [📚 LlamaIndex](./prototype/frameworks/llamaindexg/README.md)
- [🏗 MCP-Agent](./prototype/frameworks/mcp/README.md)
- [🌐 Open WebUI](./prototype/frameworks/openweb-ui/README.md)
- [🛠 Pydantic AI](./prototype/frameworks/pydantic-ai/README.md)

## 🦙 Llama-Stack Setup Guide

### 📁 File Structure

```
prototype/
│── frameworks/
│   ├── autogen/
│   ├── bee/
│   ├── crewai/
│   ├── dspy/
│   ├── langgraph/
│   ├── llamaindexg/
│   ├── llamastack/
│   ├── mcp/
│   ├── openweb-ui/
│   ├── pydantic-ai/
```

## 🤝 Contribution Guidelines

We welcome contributions to this evaluation project. If you would like to contribute:

1. Fork the repository and clone it locally.
2. Create a new branch for your contribution.
3. Ensure all changes are well-documented and tested.
4. Submit a pull request with a detailed explanation of your changes.

For any discussions or suggestions, please open an **📢 issue** or reach out to the maintainers.

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

