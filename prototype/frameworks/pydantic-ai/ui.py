import streamlit as st
import requests
import json

AGENT_SERVICE_ENDPOINT = "http://localhost:8000"


st.title("PydanticAI Agent Demo")
st.markdown("[PydanticAI](https://ai.pydantic.dev/)")
st.divider()


tool_list = requests.get(f"{AGENT_SERVICE_ENDPOINT}/tools")
tool_list = json.loads(tool_list.content)["tools"]

# Agents
agent_list = requests.get(f"{AGENT_SERVICE_ENDPOINT}/agents")
agent_list = json.loads(agent_list.content)["agents"]
selected_agents = st.multiselect(label="Select agents", options = agent_list, max_selections=1)
for agent in selected_agents:
    agent_info = requests.get(f"{AGENT_SERVICE_ENDPOINT}/agents/{agent}")
    agent_info = json.loads(agent_info.content)["agent"]
    with st.form(f"{agent} info"):
        system_prompt = st.text_input(label="system prompt", value=agent_info["system_prompt"])
        tools = st.multiselect(label="tools", options = tool_list )
        submitted = st.form_submit_button("Submit")
        if submitted:
            requests.post(f"{AGENT_SERVICE_ENDPOINT}/agents/{agent}", 
                          json={"name":agent,
                                "system_prompt":system_prompt,
                                 "tools": tools})
    
# Tasks
task_list = requests.get(f"{AGENT_SERVICE_ENDPOINT}/tasks")
task_list = json.loads(task_list.content)["tasks"]
selected_tasks = st.multiselect(label="Select tasks", options = task_list, max_selections=1)
for task in selected_tasks:
    task_info = requests.get(f"{AGENT_SERVICE_ENDPOINT}/tasks/{task}")
    task_info = json.loads(task_info.content)["task"]
    with st.form(f"{task} info"):
        description = st.text_input(label = "description", value=task_info["description"])
        expected_output = st.text_input(label = "expected_output", value=task_info["expected_output"])
        agent = st.multiselect(label = "agent", options = agent_list, max_selections=1)
        submitted = st.form_submit_button("Submit")
        if submitted:
            requests.post(f"{AGENT_SERVICE_ENDPOINT}/tasks/{task}",
                          json={"name": task,
                                "description": description,
                                "expected_output": expected_output,
                                "agent": agent[0]})

# Workflow
if 'button' not in st.session_state:
    st.session_state.button = False

def click_button():
    st.session_state.button = not st.session_state.button 

def get_workflow():
    with open("compiled_workflow_test.py", "r") as f:
        file = f.read()
    st.code(file)

st.button(label="Show workflow file", on_click=click_button)

if st.session_state.button:
    get_workflow()

if st.button(label="Compile Workflow"):
    requests.post(f"{AGENT_SERVICE_ENDPOINT}/compile_workflow")

if st.button("run workflow"):
    with st.spinner():
        r = requests.post(f"{AGENT_SERVICE_ENDPOINT}/run_workflow")
        st.markdown(json.loads(r.content))
