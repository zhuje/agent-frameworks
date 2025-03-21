import anyio
import click
import httpx
import json
import yaml
from typing import Any, Dict, List, Optional, Union
import mcp.types as types
from mcp.server.lowlevel import Server
from pydantic import BaseModel, Field

class OpenAPISpec:
    """Class for parsing and working with OpenAPI specifications."""
    
    def __init__(self, spec_path: str):
        """Initialize with path to an OpenAPI spec file or URL."""
        self.spec = self._load_spec(spec_path)
        self.base_url = self._get_base_url()
        
    async def _fetch_spec(self, url: str) -> Dict[str, Any]:
        """Fetch an OpenAPI spec from a URL."""
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            content = response.text
            
            if url.endswith('.yaml') or url.endswith('.yml'):
                return yaml.safe_load(content)
            else:
                return json.loads(content)
    
    def _load_spec(self, spec_path: str) -> Dict[str, Any]:
        """Load and parse the OpenAPI spec file or URL."""
        if spec_path.startswith('http://') or spec_path.startswith('https://'):
            # For URLs, we need to run this in an event loop
            import asyncio
            try:
                return asyncio.run(self._fetch_spec(spec_path))
            except Exception as e:
                raise ValueError(f"Failed to fetch OpenAPI spec from URL: {e}")
        else:
            # For local files
            with open(spec_path, 'r') as f:
                if spec_path.endswith('.yaml') or spec_path.endswith('.yml'):
                    return yaml.safe_load(f)
                else:
                    return json.load(f)
    
    def _get_base_url(self) -> str:
        """Extract the base URL from the OpenAPI spec."""
        if 'servers' in self.spec and self.spec['servers']:
            return self.spec['servers'][0]['url']
        return ""
    
    def get_endpoints(self) -> List[Dict[str, Any]]:
        """Extract endpoints from the OpenAPI spec."""
        endpoints = []
        
        for path, path_item in self.spec.get('paths', {}).items():
            for method, operation in path_item.items():
                if method in ['get', 'post', 'put', 'delete', 'patch']:
                    endpoint = {
                        'path': path,
                        'method': method,
                        'operation_id': operation.get('operationId', f"{method}_{path}".replace('/', '_')),
                        'summary': operation.get('summary', ''),
                        'description': operation.get('description', ''),
                        'parameters': operation.get('parameters', []),
                        'request_body': operation.get('requestBody', {}),
                        'responses': operation.get('responses', {})
                    }
                    endpoints.append(endpoint)
        
        return endpoints
    
    def generate_input_schema(self, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """Generate JSON Schema for the endpoint parameters."""
        properties = {}
        required = []
        
        # Path and query parameters
        for param in endpoint['parameters']:
            param_name = param['name']
            param_schema = param.get('schema', {})
            
            properties[param_name] = {
                'type': param_schema.get('type', 'string'),
                'description': param.get('description', '')
            }
            
            if param.get('required', False):
                required.append(param_name)
        
        # Request body if it exists
        if 'requestBody' in endpoint and endpoint['requestBody']:
            content = endpoint['requestBody'].get('content', {})
            if 'application/json' in content:
                body_schema = content['application/json'].get('schema', {})
                
                if 'properties' in body_schema:
                    for prop_name, prop_schema in body_schema['properties'].items():
                        properties[prop_name] = {
                            'type': prop_schema.get('type', 'string'),
                            'description': prop_schema.get('description', '')
                        }
                
                if 'required' in body_schema:
                    required.extend(body_schema['required'])
        
        return {
            'type': 'object',
            'properties': properties,
            'required': required
        }

class MCPOpenAPITools:
    """Class for creating MCP tools from OpenAPI specifications."""
    
    def __init__(self, spec_path: str):
        """Initialize with path to an OpenAPI spec file."""
        self.api_spec = OpenAPISpec(spec_path)
        self.client = None
    
    async def initialize_client(self) -> None:
        """Initialize the HTTP client."""
        self.client = httpx.AsyncClient(
            base_url=self.api_spec.base_url,
            follow_redirects=True,
            headers={
                "User-Agent": "MCP OpenAPI Tool (github.com/modelcontextprotocol/python-sdk)",
                "Accept": "application/json"
            }
        )
    
    async def close_client(self) -> None:
        """Close the HTTP client."""
        if self.client:
            await self.client.aclose()
    
    def get_mcp_tools(self) -> List[types.Tool]:
        """Generate MCP tools from the OpenAPI spec."""
        tools = []
        
        for endpoint in self.api_spec.get_endpoints():
            tool = types.Tool(
                name=endpoint['operation_id'],
                description=endpoint.get('summary', '') or endpoint.get('description', '') or f"Call {endpoint['method'].upper()} {endpoint['path']}",
                inputSchema=self.api_spec.generate_input_schema(endpoint)
            )
            tools.append(tool)
        
        return tools
    
    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
        """Execute a tool by making the appropriate API call."""
        # Find the endpoint that corresponds to this tool name
        matching_endpoints = [
            e for e in self.api_spec.get_endpoints() 
            if e['operation_id'] == name
        ]
        
        if not matching_endpoints:
            raise ValueError(f"Unknown tool: {name}")
        
        endpoint = matching_endpoints[0]
        path = endpoint['path']
        method = endpoint['method']
        
        # Process path parameters
        path_params = {}
        query_params = {}
        body_params = {}
        
        for param in endpoint['parameters']:
            param_name = param['name']
            if param_name in arguments:
                if param['in'] == 'path':
                    path_params[param_name] = arguments[param_name]
                    path = path.replace(f"{{{param_name}}}", str(arguments[param_name]))
                elif param['in'] == 'query':
                    query_params[param_name] = arguments[param_name]
        
        # Check if there's a request body
        if 'requestBody' in endpoint and endpoint['requestBody']:
            content_type = list(endpoint['requestBody'].get('content', {}).keys())
            if 'application/json' in content_type:
                # Filter arguments that aren't path or query params
                body_params = {
                    k: v for k, v in arguments.items()
                    if k not in path_params and k not in query_params
                }
        
        # Make the request
        response = None
        if method == 'get':
            response = await self.client.get(path, params=query_params)
        elif method == 'post':
            response = await self.client.post(path, params=query_params, json=body_params if body_params else None)
        elif method == 'put':
            response = await self.client.put(path, params=query_params, json=body_params if body_params else None)
        elif method == 'delete':
            response = await self.client.delete(path, params=query_params)
        elif method == 'patch':
            response = await self.client.patch(path, params=query_params, json=body_params if body_params else None)
        
        response.raise_for_status()
        
        # Determine content type
        content_type = response.headers.get('content-type', '')
        
        if 'application/json' in content_type:
            return [types.TextContent(type="text", text=json.dumps(response.json(), indent=2))]
        elif 'image/' in content_type:
            return [types.ImageContent(type="image", data=response.content)]
        else:
            return [types.TextContent(type="text", text=response.text)]

@click.command()
@click.argument('spec_path')
@click.option("--port", default=8000, help="Port to listen on for SSE")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type",
)
def main(spec_path: str, port: int, transport: str) -> int:
    """Create MCP tools from an OpenAPI specification."""
    app = Server("mcp-openapi-tools")
    tools_manager = MCPOpenAPITools(spec_path)
    
    # Initialize the HTTP client before running
    async def initialize_client():
        await tools_manager.initialize_client()
        
    # Clean up the HTTP client after running
    async def cleanup_client():
        await tools_manager.close_client()
    
    @app.call_tool()
    async def call_tool(
        name: str, arguments: dict
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        return await tools_manager.execute_tool(name, arguments)
    
    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        return tools_manager.get_mcp_tools()
    
    if transport == "sse":
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Mount, Route
        
        sse = SseServerTransport("/messages/")
        
        async def handle_sse(request):
            await initialize_client()
            try:
                async with sse.connect_sse(
                    request.scope, request.receive, request._send
                ) as streams:
                    await app.run(
                        streams[0], streams[1], app.create_initialization_options()
                    )
            finally:
                await cleanup_client()
        
        starlette_app = Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
            ],
        )
        
        import uvicorn
        uvicorn.run(starlette_app, host="0.0.0.0", port=port)
    else:
        from mcp.server.stdio import stdio_server
        
        async def arun():
            await initialize_client()
            try:
                async with stdio_server() as streams:
                    await app.run(
                        streams[0], streams[1], app.create_initialization_options()
                    )
            finally:
                await cleanup_client()
        
        anyio.run(arun)
    
    return 0

if __name__ == "__main__":
    main()