# code from https://modelcontextprotocol.io/quickstart/client
import asyncio
from typing import Optional
from contextlib import AsyncExitStack
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


class MCPClient:
    def __init__(self):
        self.session : Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.openai = OpenAI(
            api_key=os.getenv("API_KEY"),
            base_url= os.getenv("BASE_URL"),
            ) 
    
    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server
        
        Args:
            server_script_path: Path to the server script (.py or .js file) 
        """
        is_python = server_script_path.endswith(".py")
        is_js = server_script_path.endswith(".js")

        if not (is_js or is_python):
            raise ValueError("Server script must be .py or .js")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        #list available tools
        response = await self.session.list_tools()
        tools = response.tools
        response = await self.session.read_resource("greeting://Agent_User")
        print(response.contents[0].text)
        print("\nYou are connected to a server with tools:", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        """Process a query using custom client and available tools"""
        conversation = [
            {
                "role": "user",
                "content": query
            }
        ]

        response = await self.session.list_tools()
        
        available_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for tool in response.tools]

        #Initial LLM API Call
        response = self.openai.chat.completions.create(
            model=os.getenv("MODEL_NAME"),
            max_tokens=100,
            messages=conversation,
            tools=available_tools,
            tool_choice="auto"
        )

        # Process response and handle tool calls
        tool_results = []
        final_text = []

        for content in response.choices:
            if content.message.content:
                print("TEXT")
                final_text.append(content.message.content)
            elif content.message.tool_calls:
                print("TOOL")
                print(content.message.tool_calls)
                tool_name = content.message.tool_calls[0].function.name
                tool_args = content.message.tool_calls[0].function.arguments
                print(tool_name)
                print(tool_args)
                tool_args = json.loads(tool_args)
                print(type(tool_args))
                #execute tool call
                result = await self.session.call_tool(tool_name, arguments=tool_args)
                print(result)
                tool_results.append({"call": tool_name, "result": result})
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

                # # Continue conversation with tool results
                if content.message.tool_calls:
                    conversation.append({
                        "role":"assistant",
                        "content": str(content.message.tool_calls)
                    }) 
                
                conversation.append({
                    "role":"user",
                    "content": str(result.content)
                })


                #Get next response from claude
                response = self.openai.chat.completions.create(
                    model = os.getenv("MODEL_NAME"),
                    max_tokens = 100,
                    messages = conversation,
                )

                final_text.append(response.choices[0].message.content)
            
            return "\n".join(final_text)
        
    async def chat_loop(self):
        """Run interactive chat loop"""
        print("\nMCP client started!")
        print("What's on your mind? Type 'quite' to exit")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)
                print("\n" + response)
            
            except Exception as e:
                print(f"\n Error: {str(e)}")
        
    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()

    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup

if __name__ == "__main__":
    import sys
    asyncio.run(main())
