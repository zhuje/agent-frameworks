# Agentic frameworks evaluation

User Story:
- As an Insurance Specialist at Parisol Insurance I want to be able to, via a simple UI, create an agent named “Scorer” that will use a tool to generate a random number between 1 and 100, simulating calculating an “insurability score” for a user. This score will be passed to the next agent named “Approver” that will use a tool to look up whether or not the score is sufficient for insurance approval, and output an acceptance or denial letter with an explanation as to why to the user. This “looking-up” can be as simple as `if score > 50: return “approved”` for now. Once the agents, tools, tasks and workflow are defined, I need to be able to deploy my agent to OpenShift. (This is obviously a very simple toy example but I’d like us to all be very solid on the absolute basics before we try to add complexity :)
- As an Insurance Specialist at Parisol Insurance I want a simple (ideally no-code) way to define Agents, Tasks, Tools and Workflows and deploy them onto our OpenShift Cluster to help me automate away many of the tedious tasks I normally do. When I define an Agent, Task, Tool, or Workflow I want them added to some persistent location so that I can re-use or modify them later.
- I do not want to worry about LLM deployment. I only want to provide my agent with an Endpoint to access any arbitrary model server.

Notes:
- One of our goals here is to identify any limitations or dead-ends we might run into with a particular framework before we get too far down the road with one.
- The demo should be built as a client-server web app (I used FastAPI for the server and Streamlit for
the client, but who should use whatever is easiest for you at this point)
