from mcp.server.fastmcp import FastMCP
from functionality import create_event, create_note
from datetime import datetime

mcp = FastMCP(
    name='PIPI',
    description='Enables Scheduling, Booking, and Management of appointments for a business, and everything else that can be done by a personal assistant'
)
 

# 📅 Add an event to the macOS Calendar
def try_parse_date(date_str):
    known_formats = [
        "%d/%m/%Y",
        "%Y-%m-%d",
        "%B %d %Y",       # "May 8 2025"
        "%b %d %Y",        # "May 8 2025" with short month
        "%d %B %Y",        # "8 May 2025"
        "%d %b %Y",        # "8 May 2025" with short month
    ]
    for fmt in known_formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return None

@mcp.tool()
def create_event_tool(title, date, start_time, duration_minutes):
    """
    Create a macOS Calendar event.
    
    Args:
        title: Event title like "UC Purely"
        date: Date like "5/8/2025", "May 8 2025", "8 May 2025"
        start_time: Time like "08:00 AM", "8 AM"
        duration_minutes: Duration in minutes, e.g., 40
    """
    date_obj = try_parse_date(date)
    if not date_obj:
        return f"❌ Failed to parse date: '{date}'. Please use a clearer format like '5/8/2025' or 'May 8 2025'."

    # Normalize date to DD/MM/YYYY
    formatted_date = date_obj.strftime("%d/%m/%Y")
    
    try:
        # Just to validate the format works before sending
        datetime.strptime(f"{formatted_date} {start_time}", "%d/%m/%Y %I:%M %p")
    except ValueError:
        return f"❌ Couldn't parse time: '{start_time}'. Use format like '8:00 AM'"

    return create_event(title, formatted_date, start_time, int(duration_minutes))
# 📝 Create a note in macOS Notes app
@mcp.tool()
def create_note_tool(title: str, body: str):
    """Create a new note in the macOS Notes app with the provided title and body"""
    return create_note(title, body)

if __name__ == '__main__':
    mcp.run(transport='stdio')