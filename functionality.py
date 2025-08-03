import subprocess
from datetime import datetime, timedelta
import os
import requests
from dotenv import load_dotenv

load_dotenv()


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






BANNED_FILES = [".env", ".secrets", ".DS_Store"]

def run_cmd(cmd, cwd):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return result.stdout.strip(), result.returncode

def remove_sensitive_files(local_path):
    for filename in BANNED_FILES:
        full_path = os.path.join(local_path, filename)
        if os.path.isfile(full_path):
            tracked, _ = run_cmd(["git", "ls-files", filename], cwd=local_path)
            if tracked:
                run_cmd(["git", "rm", "--cached", filename], cwd=local_path)

def ensure_gitignore(local_path):
    gitignore_path = os.path.join(local_path, ".gitignore")
    required_rules = [".env", "__pycache__/", "*.pyc"]

    if not os.path.exists(gitignore_path):
        with open(gitignore_path, "w") as f:
            for rule in required_rules:
                f.write(rule + "\n")
    else:
        with open(gitignore_path, "r+") as f:
            lines = f.read().splitlines()
            for rule in required_rules:
                if rule not in lines:
                    f.write(rule + "\n")

def upload_to_github():
    local_path = os.getcwd()
    repo_name = os.path.basename(local_path)
    description = "Synced by MCP GitHub uploader"
    private = True

    github_token = os.getenv("GITHUB_TOKEN")
    github_user = os.getenv("GITHUB_USERNAME")

    if not github_token or not github_user:
        return "❌ Missing GitHub credentials or username in .env."

    if not os.path.exists(local_path):
        return f"❌ Path does not exist: {local_path}"

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    check_url = f"https://api.github.com/repos/{github_user}/{repo_name}"
    check_response = requests.get(check_url, headers=headers)
    repo_exists = check_response.status_code == 200

    if not repo_exists:
        data = {
            "name": repo_name,
            "description": description,
            "private": private
        }
        create_response = requests.post("https://api.github.com/user/repos", headers=headers, json=data)
        if create_response.status_code != 201:
            return f"❌ Failed to create GitHub repo: {create_response.json().get('message')}"
        clone_url = create_response.json()["clone_url"]
    else:
        clone_url = f"https://github.com/{github_user}/{repo_name}.git"

    ensure_gitignore(local_path)
    remove_sensitive_files(local_path)

    if not any(os.scandir(local_path)):
        with open(os.path.join(local_path, "README.md"), "w") as f:
            f.write("# Auto-generated README\n")

    is_git_repo = os.path.isdir(os.path.join(local_path, ".git"))
    if not is_git_repo:
        run_cmd(["git", "init"], local_path)

    run_cmd(["git", "checkout", "-B", "main"], local_path)

    # Fix remote URL if needed
    expected_repo_url = f"https://github.com/{github_user}/{repo_name}.git"
    remotes_output, _ = run_cmd(["git", "remote", "-v"], local_path)
    origin_url = ""
    for line in remotes_output.splitlines():
        if line.startswith("origin") and "(push)" in line:
            origin_url = line.split()[1]
            break

    if origin_url != expected_repo_url:
        if origin_url:
            run_cmd(["git", "remote", "set-url", "origin", expected_repo_url], local_path)
        else:
            run_cmd(["git", "remote", "add", "origin", expected_repo_url], local_path)

    run_cmd(["git", "add", "."], local_path)
    _, code = run_cmd(["git", "commit", "-m", "Update project"], local_path)
    if code != 0:
        return "ℹ️ Nothing new to commit."

    run_cmd(["git", "branch", "-M", "main"], local_path)
    push_output, _ = run_cmd(["git", "push", "--force", "-u", "origin", "main"], local_path)

    return f"✅ Synced with GitHub: https://github.com/{github_user}/{repo_name}"
