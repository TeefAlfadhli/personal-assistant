from os import name
from mcp.server.fastmcp import FastMCP
import subprocess

mcp = FastMCP(
    name="My Server",
    description="Provides tools, resources, and prompts"
)

# Define a tool that adds two integers and returns the result
# TODO: Add PA tools
'''
The date format must match what AppleScript expects (e.g., "Monday, June 10, 2024 at 10:00:00 AM").
'''
@mcp.tool()
@mcp.tool()
def create_event(title, date, start_time, duration_minutes):
    # Combine and parse start datetime
    start_datetime_str = f"{date} {start_time}"
    start_dt = datetime.strptime(start_datetime_str, "%d/%m/%Y %I:%M %p")
    end_dt = start_dt + timedelta(minutes=int(duration_minutes))

    # Format dates for AppleScript
    start_str = start_dt.strftime("%-d/%-m/%Y %I:%M %p")
    end_str = end_dt.strftime("%-d/%-m/%Y %I:%M %p")

    # AppleScript to add event
    script = f'''
    tell application "Calendar"
        activate
        tell calendar "Calendar"
            set startDate to date "{start_str}"
            set endDate to date "{end_str}"
            make new event at end with properties {{summary:"{title}", start date:startDate, end date:endDate}}
        end tell
    end tell
    '''
    subprocess.run(["osascript", "-e", script])

# 🌟 Get input from the user
def prompt_user_for_event():
    print("📅 Let's schedule a new event in your macOS Calendar.\n")
    title = input("Event title: ")
    date = input("Date (D/M/YYYY): ")
    start_time = input("Start time (e.g., 10:00 AM): ")
    duration = input("Duration (minutes): ")

    create_event(title, date, start_time, duration)


# add_event_to_calendar()


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
