from mcp.server.fastmcp import FastMCP
from functionality import create_event, create_note

mcp = FastMCP(
    name='PIPI',
    description='Enables Scheduling, Booking, and Management of appointments for a business, and everything else that can be done by a personal assistant'
)
 

# 📅 Add an event to the macOS Calendar
@mcp.tool()
def create_event_tool(title, date, start_time, duration_minutes):
    """Create a calendar event in macOS Calendar"""
    return create_event(title, date, start_time, duration_minutes)

# 📝 Create a note in macOS Notes app
@mcp.tool()
def create_note_tool(title: str, body: str):
    """Create a new note in the macOS Notes app with the provided title and body"""
    return create_note(title, body)

if __name__ == '__main__':
    mcp.run(transport='stdio')