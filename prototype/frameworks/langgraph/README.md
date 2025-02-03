# LangGraph Agentic Insurance Workflow

This project demonstrates an AI-driven insurance workflow using **FastAPI**, **Streamlit**, and **LangGraph**. It simulates an automated decision-making system for processing insurance requests, scoring applicants, and determining approval based on predefined rules.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [License](#license)
- [Contributors](#contributors)

---

## Overview
This application provides:
1. A **Streamlit UI** where users can submit insurance applications and interact with the chatbot.
2. A **FastAPI backend** that:
   - Defines and manages Agents, Tools, and Workflows.
   - Runs a **LangGraph-based AI workflow** for evaluating insurance eligibility.

---

## Features
- **AI-powered insurance approval process** using LangGraph and ChatOllama.
- **Workflow automation** with a decision-making pipeline:
  - *Scorer* generates a random insurability score (0-100).
  - *Approver* approves or denies based on a score threshold (>50).
- **FastAPI for backend** to manage agents, tools, and workflows.
- **Streamlit for frontend UI** to submit insurance requests and interact with the chatbot.
- **Session-based interactions** allowing users to have multiple independent conversations.

---

## Technology Stack
- **FastAPI** (Backend API framework)
- **Streamlit** (Frontend UI for interaction)
- **LangGraph** (Graph-based AI workflow execution)
- **Ollama Chat** (LLM model integration)
- **Pydantic** (Data validation)
- **Uvicorn** (ASGI server for FastAPI)

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

### 4. Set up environment variables
Rename `sample.env` to `.env` and update values as needed.

---

## Running the Application
### 1. Start the FastAPI server
```sh
python server.py
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
### 1. Start a new session
- **POST /start-session/** → Creates a new chat session and returns session ID with initial messages.

### 2. Send a message
- **POST /chat/** → Sends a user message and processes AI responses.

#### Example Request:
```sh
curl -X POST "http://localhost:8005/chat" \
     -H "Content-Type: application/json" \
     -d '{"session_id": "your-session-id", "message": "I would like to apply for insurance."}'
```

#### Example Response:
```json
{
  "session_id": "your-session-id",
  "messages": [
    {"role": "human", "content": "I would like to apply for insurance."},
    {"role": "assistant", "content": "The Scorer will now determine your insurability score."},
    {"role": "assistant", "content": "Generated insurability score: 65. Sending to Approver..."},
    {"role": "assistant", "content": "✅ Approved! Your insurability score of 65 qualifies you for insurance."}
  ]
}
```

### 3. Retrieve session messages
- **GET /session/{session_id}** → Returns the chat history of a specific session.

---

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---

## Contributors
- [Kevin Cogan](https://github.com/kevincogan)
- [Hema Veeradhi](https://github.com/hemajv)

