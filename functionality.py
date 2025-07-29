from os import name
from mcp.server.fastmcp import FastMCP
import subprocess

mcp = FastMCP(
    name="My Server",
    description="Provides tools, resources, and prompts"
)

# Define a tool that adds two integers and returns the result
# TODO: Add PA tools
@mcp.tool()
def add(a: int, b: int) -> int:
    """Return the sum of a and b."""
    return a + b



'''
The date format must match what AppleScript expects (e.g., "Monday, June 10, 2024 at 10:00:00 AM").
'''
@mcp.tool()
def add_calendar_event(date: str, description: str) -> str:
    # AppleScript to add an event
    applescript = f'''
    tell application "Calendar"
        tell calendar "Home"
            make new event at end with properties {{summary:"{description}", start date:date "{date}"}}
        end tell
    end tell
    '''
    subprocess.run(['osascript', '-e', applescript])
    return f"Event '{description}' scheduled for {date} in your Mac Calendar."



# Define a resource that returns a static greeting string
# TODO: Add PA resources
@mcp.resource("resource://user_info", description="Data about the user")
def user_info() -> str:
    """Data about the user"""
    name = "Teef"
    return name


# Define a prompt template that generates a user message about a topic
# TODO: Add PA prompts
@mcp.prompt()
def ask_user_task(name: str) -> str:
    """Generate a user message asking for an explanation of topic."""
    return f"Hello '{name}', How can I help you today?"


# TODO: connect to a client (e.g. a calendar app)
