# CrewAI Example

> This example uses [uv](https://docs.astral.sh/uv/) to mange dependencies. Please make sure its [installed](https://docs.astral.sh/uv/getting-started/installation/#pypi) before proceeding.

Setup your `.env` file with the correct values for `MODEL_NAME`, `BASE_URL` and `API_KEY` for your LLM server. You can copy `.env.example` and rename it to `.env` to make things simpler. 

Start the agent service with the following command:
```bash
uv run fastapi dev main.py
```
Navigate to `http://localhost:8000/docs#` to interact with the API.

![](/prototype/frameworks/crewai/assets/fastapi_docs.png)


Start the Streamlit UI with the following command:
```bash
 uv run streamlit run ui.py
```
Navigate to `http://localhost:8501` to interact with the app.

![](/prototype/frameworks/crewai/assets/agent_factory_ui.png)

If you simply click each button in order; `Add Agent`, `Add Task`,
`Compile crew.py`, and `Run Agent`, the default values should be sufficient to see a two agent, two task one tool example. 