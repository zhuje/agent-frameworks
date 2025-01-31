# LangGraph Agentic Insurance Workflow

This project demonstrates an AI-driven insurance workflow using **FastAPI**, **Streamlit**, and **LangGraph**. It simulates an automated decision-making system for processing insurance requests, scoring applicants, and determining approval based on predefined rules.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Deployment to OpenShift](#deployment-to-openshift)
- [License](#license)

---

## Overview
This application provides:
1. A **Streamlit UI** where users can submit insurance applications.
2. A **FastAPI backend** that:
   - Defines and manages Agents, Tools, and Workflows.
   - Runs a **LangGraph-based AI workflow** for evaluating insurance eligibility.
3. A **Dockerized deployment** setup for OpenShift.

---

## Features
- **AI-powered insurance approval process** using LangGraph and ChatOllama.
- **Workflow automation** with a decision-making pipeline:
  - *Insurance Specialist* decides if scoring is required.
  - *Scorer* generates a random insurability score (1-100).
  - *Approver* approves or denies based on a score threshold (>50).
- **FastAPI for backend** to manage agents, tools, and workflows.
- **Streamlit for frontend UI** to submit insurance requests.
- **Deployable on OpenShift** as a containerized application.

---

## Technology Stack
- **FastAPI** (REST API framework)
- **Streamlit** (Frontend UI)
- **LangGraph** (Graph-based AI workflow execution)
- **Ollama Chat** (LLM model integration)
- **Docker** (Containerization for deployment)

---

## Installation
### 1. Clone the repository
```sh
git clone https://github.com/redhat-et/agent-frameworks.git
cd insurance-workflow
```

### 2. Create and activate a virtual environment
```sh
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate    # For Windows
```

### 3. Install dependencies
```sh
pip install -r requirements.txt
```

---

## Running the Application
### 1. Start the FastAPI server
```sh
python fastapi_server.py
```

### 2. Start the Streamlit frontend
```sh
streamlit run streamlit_client.py
```

### 3. Access the application
- **FastAPI API Docs:** [http://localhost:8005/docs](http://localhost:8005/docs)
- **Streamlit UI:** [http://localhost:8501](http://localhost:8501)

---

## API Endpoints
### 1. Root Endpoint
- **GET /** → `{"msg": "Hello from Insurance Automation FastAPI!"}`

### 2. Manage Agents, Tools, Workflows
- **POST /definitions/agents/** → Create an agent
- **GET /definitions/agents/** → List all agents
- **POST /definitions/tools/** → Create a tool
- **GET /definitions/tools/** → List all tools
- **POST /definitions/workflows/** → Create a workflow
- **GET /definitions/workflows/** → List all workflows

### 3. Run the Insurance Workflow
- **POST /run_insurance_workflow/** → Runs the insurance workflow and returns AI messages

#### Example Request:
```sh
curl -X POST "http://localhost:8005/run_insurance_workflow/" \
     -H "Content-Type: application/json" \
     -d '{"user_input": "I would like to apply for insurance."}'
```
#### Example Response:
```json
{
  "messages": [
    "The Scorer will now determine your insurability score.",
    "Generated insurability score: 65. Sending to Approver...",
    "✅ Approved! Your insurability score of 65 qualifies you for insurance."
  ]
}
```

---

## Deployment to OpenShift
### 1. Build the Docker image
```sh
docker build -t your-registry/insurance-workflow:latest .
```

### 2. Push the image to your container registry
```sh
docker push your-registry/insurance-workflow:latest
```

### 3. Deploy to OpenShift
```sh
oc new-app your-registry/insurance-workflow:latest
oc expose svc/insurance-workflow
```

### 4. Access the application
- **Streamlit UI:** `https://your-openshift-route`
- **FastAPI API:** `https://your-openshift-route/api`

---

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---

## Contributors
- [Kevin Cogan](https://github.com/kevincogan)
- [Hema Veeradhi](https://github.com/hemajv)
