# MCP - Model Context Protocol

Add the correct `API_KEY`, `BASE_URL` and `MODEL_NAME` to your `.env` file. 

Then run the following to start the simple mcp client and associated tool server. 

```bash
uv run mcp_client.py tool_server.py
```
You should see the following in your terminal.

```bash
Hello, Agent_User

You are connected to a server with tools: ['generate_random_number', 'approve_score']

MCP client started!
What's on your mind? Type 'quite' to exit

Query: 
```
