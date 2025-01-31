import random
from typing import Annotated, TypedDict

from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# Define the state structure
class State(TypedDict):
    messages: Annotated[list, add_messages]
    score: int
    needs_scoring: bool
    needs_approval: bool

# Initialize the LLM model (point this to your Ollama instance or other model endpoint)
model = ChatOllama(model='mistral:latest')

# Create the LangGraph workflow
graph_builder = StateGraph(State)

# ---------------------------
#  Agent: Insurance Specialist
# ---------------------------
def insurance_agent(state: State):
    user_message = state["messages"][-1].content

    decision_prompt = f"""
    You are an AI car insurance specialist. Determine if an insurability score needs to be calculated.
    - If yes, respond ONLY with "call scorer".
    - If no, respond ONLY with "no scoring needed".

    User Input: "{user_message}"
    Decision:
    """
    decision_response = model.invoke([HumanMessage(content=decision_prompt)])
    decision = decision_response.content.strip().lower()

    if "call scorer" in decision:
        return {
            "messages": [AIMessage(content="The Scorer will now determine your insurability score.")],
            "needs_scoring": True,
            "needs_approval": False
        }

    return {
        "messages": [AIMessage(content="No scoring needed. Your request is processed manually.")],
        "needs_scoring": False,
        "needs_approval": False
    }

# ---------------------------
#  Tool/Task: Scorer
# ---------------------------
def scorer(state: State):
    if not state["needs_scoring"]:
        return state  # Skip if not needed

    score = random.randint(1, 100)
    state["score"] = score

    response = AIMessage(content=f"Generated insurability score: {score}. Sending to Approver...")
    return {"messages": [response], "score": score, "needs_approval": True}

# ---------------------------
#  Tool/Task: Approver
# ---------------------------
def approver(state: State):
    if not state["needs_approval"]:
        return state  # Skip if not needed

    score = state["score"]

    approval_prompt = f"""
    You are an AI insurance approver. You receive an insurability score and must determine if the user is approved.
    - If the score is above 50, return ONLY "approved".
    - If the score is 50 or below, return ONLY "denied".
    - DO NOT return any other text.

    Insurability Score: {score}
    Decision:
    """

    decision_response = model.invoke([HumanMessage(content=approval_prompt)])
    decision = decision_response.content.strip().lower()

    if "approved" in decision:
        final_message = f"✅ Approved! Your insurability score of {score} qualifies you for insurance."
    elif "denied" in decision:
        final_message = f"❌ Denied. Unfortunately, your insurability score of {score} falls below our required threshold."
    else:
        final_message = f"⚠️ Unexpected LLM response: {decision}. Defaulting to denied."

    return {"messages": [AIMessage(content=final_message)]}

# Build the Graph
graph_builder.add_node("insurance_agent", insurance_agent)
graph_builder.add_node("scorer", scorer)
graph_builder.add_node("approver", approver)

graph_builder.add_edge(START, "insurance_agent")

graph_builder.add_conditional_edges(
    "insurance_agent",
    lambda state: "scorer" if state["needs_scoring"] else END
)
graph_builder.add_conditional_edges(
    "scorer",
    lambda state: "approver" if state["needs_approval"] else END
)

# The flow can end after "insurance_agent" or "approver"
graph_builder.add_edge("approver", END)
graph_builder.set_finish_point("insurance_agent")
graph_builder.set_finish_point("approver")

# Compile it
graph = graph_builder.compile()

def run_insurance_workflow(user_input: str) -> list[str]:
    """
    Runs the insurance workflow with user_input. Returns list of
    messages from the AI to the user.
    """
    initial_state = {
        "messages": [HumanMessage(content=user_input)],
        "score": 0,
        "needs_scoring": False,
        "needs_approval": False
    }

    output_messages = []

    # Stream the graph execution
    for event in graph.stream(initial_state):
        for value in event.values():
            # Each step adds an AIMessage to state["messages"]
            ai_msg = value["messages"][-1].content
            output_messages.append(ai_msg)

    return output_messages
