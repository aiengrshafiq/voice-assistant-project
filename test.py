import requests
from datetime import datetime, timezone

# --- Configuration ---
headers = {
    "Authorization": f"Bearer {input['token']}"
}
project_id = input['project_id']
base_task_url = f"https://app.asana.com/api/1.0/projects/{project_id}/tasks"
params = {
    "opt_fields": "projects.name,completed,name,completed_at,assignee.name,memberships.section.name",
    "limit": 100  # max allowed by Asana
}

# --- Pagination: Fetch all tasks ---
tasks = []
next_page = None

while True:
    # Make request to the current page
    if next_page:
        response = requests.get(next_page, headers=headers)
    else:
        response = requests.get(base_task_url, headers=headers, params=params)

    if response.status_code != 200:
        print("Error fetching tasks:", response.status_code, response.text)
        break

    data = response.json()
    tasks.extend(data.get("data", []))

    # Check if next_page exists and update the URL for the next iteration
    next_page = data.get("next_page", None)

    # Ensure that next_page is actually a dictionary and extract the 'uri' if it exists
    if next_page and isinstance(next_page, dict):
        next_page = next_page.get('uri', None)
    if not next_page:  # Stop if no more pages
        break



# --- Get Project Name ---
project_url = f"https://app.asana.com/api/1.0/projects/{project_id}?opt_fields=name"
project_response = requests.get(project_url, headers=headers)
project_data = project_response.json().get("data", {})
project_name = project_data.get("name", "Unknown")

# --- Initialize counts ---
completed = 0
in_progress = 0
pending = 0
assignee_name = None
today = datetime.now(timezone.utc).date()

# --- Process each task ---
for task in tasks:
    name = task.get("name", "")
    assignee = task.get("assignee", {})
    if assignee and not assignee_name:
        assignee_name = assignee.get("name")

    # Get section
    section_name = ""
    memberships = task.get("memberships", [])
    if memberships:
        section = memberships[0].get("section", {})
        section_name = section.get("name", "").strip().lower()

    # Check if completed today
    completed_at = task.get("completed_at")
    completed_today = False
    if completed_at:
        try:
            completed_dt = datetime.fromisoformat(completed_at.replace("Z", "+00:00"))
            completed_today = completed_dt.date() == today
        except Exception as e:
            print(f"Error parsing date for task {name}: {e}")

    print(f"Task: {name}, section: {section_name}, completed_today: {completed_today}")

    # Count based on section and status
    if section_name == "completed" and completed_today:
        completed += 1
    elif section_name == "in progress":
        in_progress += 1
    elif section_name == "to do":
        pending += 1

# --- Final Report ---
total = completed + in_progress + pending
completion_ratio = round((completed / total) * 100, 2) if total > 0 else 0

if completion_ratio >= 80:
    status = "On Track"
elif completion_ratio >= 50:
    status = "At Risk"
else:
    status = "Behind"

return {
    "project_name": project_name or "Unknown",
    "assignee": assignee_name or "Unknown",
    "total_tasks": total,
    "completed": completed,
    "in_progress": in_progress,
    "pending": pending,
    "completion_ratio": completion_ratio,
    "project_status": status
}
