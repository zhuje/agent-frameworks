import streamlit as st
import requests
import json


def get_agents():
    r = requests.get(url="http://localhost:8000/agents")
    agents = json.loads(r.content)
    return agents

def get_tasks():
    r = requests.get(url="http://localhost:8000/tasks")
    tasks = json.loads(r.content)
    return tasks


def get_tools():
    r = requests.get(url="http://localhost:8000/tools")
    tools = json.loads(r.content)
    return tools

agents = get_agents()
agent_names = [agent["name"] for agent in agents]

tasks = get_tasks()
task_names = [task["name"] for task in tasks]

tools = get_tools()
tool_names = [tool["name"] for tool in tools]

st.title("Agent Factory")
st.divider()

st.markdown("agent.yaml")   
with open("compiled_crew/config/agents.yaml" ,"r", encoding="utf-8") as f:
    agents_yaml = f.read()

st.code(agents_yaml)
st.markdown("New Agent")
with st.form("New Agent"):
    name = st.text_input(label="name" ,value="approver")
    role = st.text_input(label="role" ,value="You are responsible for approving or denying service based on customers scores.")
    goal = st.text_input(label="goal" ,value="Write a polite, professional and detailed letter to customers about the results of their insurance eligibility score. It MUST be less than 3 paragraphs.")
    backstory = st.text_input(label="backstory" ,value="You have worked at Parasol insurance for 20 years.")
    tools = st.multiselect(label="tools", options=tool_names)
    if st.form_submit_button("Add Agent"):
        # add agent
        requests.post(f"http://localhost:8000/agents/new/{name}",
                       json={"name": name,
                                "role": role,
                               "goal": goal,
                               "backstory" : backstory,
                               "tools": tools
                               })
        #update config
        requests.post("http://localhost:8000/update_agent_config")


st.markdown("tasks.yaml")
with open("compiled_crew/config/tasks.yaml" ,"r", encoding="utf-8") as f:
    tasks_yaml = f.read()
st.code(tasks_yaml)

st.markdown("New Task")
with st.form("New Task"):
    name = st.text_input(label="name" ,value="approve_task")
    description = st.text_input(label="description" ,value="A polite, professional and detailed letter to customers about the results of their insurance eligibility score. It must include if they were approved or denied. A higher number is better. A score above 50 is approved a score below 50 is denied.")
    expected_output = st.text_input(label="expected_output" ,value="A 2 paragraph letter.")
    agent = st.text_input(label="agent", value="approver")
    context = st.text_input(label="context", value="score_task")
    context = [task for task in context.split(",")]
    st.markdown(type(context))


    if st.form_submit_button("Add Task"):
        # add agent
        requests.post(f"http://localhost:8000/tasks/new/{name}",
                       json={"name": name,
                             "description": description,
                               "expected_output": expected_output,
                               "agent" : agent,
                               "context" : context
                               })
        #update config
        requests.post(f"http://localhost:8000/update_task_config")


st.divider()

if st.button(label="Compile crew.py"):
     requests.post("http://localhost:8000/compile")
st.markdown("crew.py")

with open("compiled_crew/test_compiled_crew.py" ,"r", encoding="utf-8") as f:
    python_file = f.read()
st.code(python_file)


if st.button(label="Run Agent"):
    with st.spinner():
        response = requests.post(url="http://localhost:8000/run")
        response = json.loads(response.content)
        st.markdown(response["agent_response"]["raw"])
