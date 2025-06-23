from google.adk import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
relative_path = os.path.join(script_dir, "mcp_server", "minimal.py")
print(f"Using script: {relative_path}")

print(f"Current working directory: {os.getcwd()}")

root_agent = Agent(
    model="gemini-2.0-flash",
    name="mcp_agent",
    instruction="Help the user explore and read files and query user emails.",
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command="uv",
                args=["run", "--with", "mcp", "mcp", "run", relative_path]
            )
        )
    ],
)
