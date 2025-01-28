## Open-WebUI as an AI Agent framework and interface

Tim Baek, the founder of Open WebUI, explains in [this short video](https://youtu.be/-yyMSBARfgM?si=xriJzGZsZvDVI3Hz)
why his project has over 3M downloads and 50K GitHub stars.

Also, refer to the [open-webui documentation](https://docs.openwebui.com/).

## AI interface with agentic features

If you've checked out [open-webui](https://docs.openwebui.com/) chances are you got up and running quickly with `ollama`.
`open-webui` has a ton of cool features like enabling web-search and RAG with chats. There is also a community maintained
[`Tools` and `Functions`collection](https://docs.openwebui.com/features/plugin/) with which to craft AI powered agentic
applications.

In this exploration, we'll utilize an OpenAI API model endpoint serving
[mistralai/Mistral-7B-v0.1](https://huggingface.co/mistralai/Mistral-7B-v0.1) via vLLM and KServe in OpenShift.
We will not utilize ollama or explore multiple models. Our main purpose is to create a few agents.

### [Deploy on OpenShift](./openshift-deploy/README.md)

### [Deploy locally](./local/README.md)

## Create some agents with the Scorer and Approver example

Follow [tools](./tools/README.md) documentation.
