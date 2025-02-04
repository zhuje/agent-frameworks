import random
from typing import Optional
from typing_extensions import Annotated, TypedDict

from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from constant import MODEL_NAME, MODEL_TEMPERATURE, BASE_URL, BASE_PROMPT, THREAD_ID, CHECKPOINT_NS, CHECKPOINT_ID


class State(TypedDict, total=False):
    messages: Annotated[list, add_messages]
    score: Optional[int]

class InsuranceAgent:
    def __init__(self):
        self.model = ChatOllama(
            model=MODEL_NAME,
            base_url=BASE_URL,
            temperature=MODEL_TEMPERATURE)
       
        self.tools = [self.scorer, self.approver]
        self.llm_with_tools = self.model.bind_tools(self.tools)
        self.memory = MemorySaver()
        self.graph = self.build_graph()

        self.initial_state: State = {
            "messages": [HumanMessage(content=BASE_PROMPT)],
            "score": None
        }

    def print_separator(self, text=""):
        """Prints a formatted separator for better readability."""
        print("\n" + "=" * 50)
        if text:
            print(f"  {text}")
            print("=" * 50 + "\n")

    def scorer(self, state: State) -> State:
        """Generates a random insurability score and updates the state."""
        score = random.randint(0, 100)
        self.initial_state["score"] = score
        state.setdefault("messages", []).append(
            AIMessage(content=f"Generated insurability score: {score}.")
        )
        self.print_separator("🏆 SCORE GENERATED")
        print(f"🔹 Insurability Score: {score}\n")
        return state

    def approver(self, state: State) -> State:
        """Decides whether the insurance application is approved or denied based on the score."""
        score = self.initial_state.get("score", 0)
        decision = "✅ Approved!" if score > 50 else "❌ Denied."
        state.setdefault("messages", []).append(
            AIMessage(content=f"{decision} Your insurability score: {score}.")
        )
        self.print_separator("📋 APPROVAL DECISION")
        print(f"🔹 Score: {score}")
        print(f"🔹 Decision: {decision}\n")
        return state

    def chatbot(self, state: State) -> State:
        """Processes messages and executes tools if necessary."""
        messages = state.setdefault("messages", [])
        response = self.llm_with_tools.invoke(messages)

        if isinstance(response, dict):
            state.update(response)
        elif isinstance(response, (str, AIMessage)):
            state["messages"].append(
                AIMessage(content=response) if isinstance(response, str) else response
            )
        else:
            state["messages"].append(AIMessage(content=str(response)))

        return state

    def build_graph(self) -> StateGraph:
        """Constructs the LangGraph workflow."""
        graph_builder = StateGraph(State)
        graph_builder.add_node("chatbot", self.chatbot)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_conditional_edges("chatbot", tools_condition)
        graph_builder.add_edge("tools", "chatbot")
        graph_builder.set_entry_point("chatbot")
        return graph_builder.compile(checkpointer=self.memory)

    def process_turn(self, state: State, user_input: Optional[str] = None) -> State:
        """
        Process one conversation turn:
         - Optionally append a user message to the state.
         - Invoke the graph to process the updated state.
        """
        if user_input:
            state.setdefault("messages", []).append(HumanMessage(content=user_input))
        config = {
            "configurable": {
                "thread_id": THREAD_ID,
                "checkpoint_ns": CHECKPOINT_NS,
                "checkpoint_id": CHECKPOINT_ID,
            }
        }
        new_state = self.graph.invoke(state, config=config)
        return new_state
