from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import autogen
import os
import logging
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Define the input model
class AgentInput(BaseModel):
    name: str
    system_message: str


# Helper function to check for termination message
def is_termination_message(message: dict) -> bool:
    return "TERMINATE" in message.get("content", "").upper()

# Initialize the UserProxyAgent
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    is_termination_msg=is_termination_message,
    code_execution_config={
        "work_dir": "working_dir",
        "use_docker": False
    }
)

config_list = [
    {
        'model': os.getenv('MODEL_NAME'),
        "base_url": os.getenv('BASE_URL')
    }
]

@app.get("/", response_class=HTMLResponse)
def index():
    logger.info("Serving the index page")
    return """
    <html>
        <head>
            <title>Autogen Agent Factory</title>
        </head>
        <body>
            <h1>Autogen Agent Factory</h1>
            <form action="/chat_report/" method="post">
                <h2>Scorer</h2>
                <label for="scorer_name">Name:</label><br>
                <input type="text" id="scorer_name" name="scorer_name" style="width: 100%;"><br>
                <label for="scorer_message">System Message:</label><br>
                <input type="text" id="scorer_message" name="scorer_message" style="width: 100%;"><br>
                <h2>Approver</h2>
                <label for="approver_name">Name:</label><br>
                <input type="text" id="approver_name" name="approver_name" style="width: 100%;"><br>
                <label for="approver_message">System Message:</label><br>
                <input type="text" id="approver_message" name="approver_message" style="width: 100%;"><br>
                <h2>User Proxy</h2>
                <label for="user_message">Message:</label><br>
                <input type="text" id="user_message" name="user_message" style="width: 100%;"><br>
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """


@app.post("/chat_report/")
def chat_report(scorer_name: str = Form(...), scorer_message: str = Form(...), approver_name: str = Form(...), approver_message: str = Form(...), user_message: str = Form(...)):
    logger.info("Chat report initiated")
    scorer = autogen.AssistantAgent(
        name=scorer_name,
        llm_config={
            "seed": 42,
            "config_list": config_list,
            "temperature": 0,
        },
        system_message=scorer_message,
        is_termination_msg=is_termination_message,
    )
    approver = autogen.AssistantAgent(
        name=approver_name,
        llm_config={
            "seed": 42,
            "config_list": config_list,
            "temperature": 0,
        },
        system_message=approver_message,
        is_termination_msg=is_termination_message,
    )
    groupchat = autogen.GroupChat(
        agents=[scorer, approver, user_proxy],
        messages=[],
        max_round=10,
        speaker_selection_method="auto",
        allow_repeat_speaker=False,
    )
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={
        "seed": 42,
        "config_list": config_list,
        "temperature": 0,
    })
    logger.info("Initiating chat with user message: %s \n", user_message + "\n")
    response = user_proxy.initiate_chat(
        manager,
        message=user_message
    )
    logger.info("Chat initiated successfully \n")
    
    def iter_response():
        for message in response.chat_history:
            yield f"{message['name']}:\n{message['content']}\n\n"
    
    return StreamingResponse(iter_response(), media_type="text/plain")
