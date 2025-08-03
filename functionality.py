import subprocess
from datetime import datetime, timedelta
from os import name



# 📅 Add an event to the macOS Calendar
def create_event(title, date, start_time, duration_minutes):
    # Combine and parse start datetime - TODO: add validation
    start_datetime_str = f"{date} {start_time}"
    start_dt = datetime.strptime(start_datetime_str, "%d/%m/%Y %I:%M %p")
    end_dt = start_dt + timedelta(minutes=int(duration_minutes))

    # Format dates for AppleScript - TODO: add validation
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

# 📝 Create a note in macOS Notes


def create_note(title: str = None, body: str = None):
    """
    Creates a new note in the macOS Notes app under the 'Notes' folder.
    If title or body is not provided, prompts the user interactively.

    Args:
        title (str, optional): The note's title.
        body (str, optional): The note's body.
    """
    # Prompt user if title/body not provided
    if not title:
        print("📝 Let's create a new note in macOS Notes.")
        title = input("Title: ")

    if not body:
        print("Body (type your note, press Enter on an empty line to finish):")
        body_lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            body_lines.append(line)
        body = "\n".join(body_lines)

    # Escape title
    safe_title = title.replace('"', '\\"')

    # Prepare AppleScript lines
    body_lines = body.splitlines()
    applescript_body_lines = ""
    for line in body_lines:
        safe_line = line.replace('"', '\\"')
        applescript_body_lines += f'set paragraphText to "{safe_line}"\n'
        applescript_body_lines += 'set the body of newNote to (the body of newNote) & paragraphText & return\n'

    # Final AppleScript
    script = f'''
    tell application "Notes"
        activate
        set targetFolder to first folder whose name is "Notes"
        set newNote to make new note at targetFolder with properties {{name:"{safe_title}", body:""}}
        {applescript_body_lines}
    end tell
    '''

    subprocess.run(["osascript", "-e", script])
    print(f"✅ Note created in macOS Notes under 'Notes': {title}")

# 📝 Create a note with parameters (for agent use)
import subprocess

def create_note(title: str = None, body: str = None):
    """
    Creates a new note in the macOS Notes app under the 'Notes' folder.
    If title or body is not provided, prompts the user interactively.

    Args:
        title (str, optional): The note's title.
        body (str, optional): The note's body.
    """
    # Prompt user if title/body not provided
    if not title:
        print("📝 Let's create a new note in macOS Notes.")
        title = input("Title: ")

    if not body:
        print("Body (type your note, press Enter on an empty line to finish):")
        body_lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            body_lines.append(line)
        body = "\n".join(body_lines)

    # Escape title
    safe_title = title.replace('"', '\\"')

    # Prepare AppleScript lines
    body_lines = body.splitlines()
    applescript_body_lines = ""
    for line in body_lines:
        safe_line = line.replace('"', '\\"')
        applescript_body_lines += f'set paragraphText to "{safe_line}"\n'
        applescript_body_lines += 'set the body of newNote to (the body of newNote) & paragraphText & return\n'

    # Final AppleScript
    script = f'''
    tell application "Notes"
        activate
        set targetFolder to first folder whose name is "Notes"
        set newNote to make new note at targetFolder with properties {{name:"{safe_title}", body:""}}
        {applescript_body_lines}
    end tell
    '''

    subprocess.run(["osascript", "-e", script])
    print(f"✅ Note created in macOS Notes under 'Notes': {title}")

# 💬 Define a prompt template that generates a user message about a topic
def ask_user_task(name: str) -> str:
    """Generate a user message asking for an explanation of topic."""
    return f"Hello '{name}', How can I help you today?"

# TODO: connect to a client (e.g. a calendar app)
