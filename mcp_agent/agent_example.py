import os
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

from google.adk import Agent
folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "example"))
  # Replace with a real path
root_agent = Agent(
    model="gemini-2.0-flash",
    name="mcp_agent",
    instruction="Help the user explore and read files.",
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command="npx",
                args=[
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    folder_path,
                ],
                
            )
        )
    ],
)
