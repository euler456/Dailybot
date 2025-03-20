import requests
import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Securely get API key and database ID
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("DATABASE_ID")

def get_weekday_tasks():
    # Define your tasks with toggles
    tasks = {
        "Monday": [
            {"task": "✅ Work on Auto Triage", "completed": False},
            {"task": "📌 Learn Python scripting (1hr)", "completed": False},
            {"task": "🎯 Write a script", "completed": False},
            {"task": "🏋️‍♂️ Gym/Rest", "completed": False},
        ],
        "Tuesday": [
            {"task": "✅ Work on Auto", "completed": False},
            {"task": "📌 Learn Google Cloud Basics", "completed": False},
            {"task": "🎯 Watch GCP video (30 mins)", "completed": False},
        ],
        "Wednesday": [
            {"task": "✅ Debug automation issues", "completed": False},
            {"task": "📌 Learn CI/CD (Jenkins, GitHub Actions)", "completed": False},
            {"task": "🎯 Deploy script to cloud", "completed": False},
        ],
        "Thursday": [
            {"task": "✅ Auto tasks", "completed": False},
            {"task": "📌 Learn Python OOP", "completed": False},
            {"task": "🎯 Build a small automation tool", "completed": False},
        ],
        "Friday": [
            {"task": "✅ Review Auto scripts", "completed": False},
            {"task": "📌 Learn Google Cloud Networking", "completed": False},
            {"task": "🎯 Set up test VM", "completed": False},
        ],
        "Saturday": [
            {"task": "📌 Solve 2 LeetCode problems (1 EZ, 1 MED)", "completed": False},
            {"task": "🎯 Improve coding skills", "completed": False},
        ],
        "Sunday": [
            {"task": "📌 Weekly review", "completed": False},
            {"task": "🎯 Plan next week", "completed": False},
        ],
    }

    return tasks.get(datetime.datetime.today().strftime('%A'), "No tasks for today")

def clear_tasks_on_monday():
    # Only clear tasks on Monday
    if datetime.datetime.today().strftime('%A') == "Monday":
        print("Clearing weekly tasks for a fresh start!")
        return True  # Clear tasks for the week
    return False

def update_notion_task():
    task_content = get_weekday_tasks()
    clear_this_week = clear_tasks_on_monday()  # Check if it's Monday and clear tasks if necessary

    # URL and headers
    url = f"https://api.notion.com/v1/pages"  # Correct API endpoint to create pages
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    # Data for the tasks
    for task in task_content:
        task_title = task["task"]
        task_completed = task["completed"]

        data = {
            "parent": {"database_id": DATABASE_ID},
            "properties": {
                "Name": {"title": [{"text": {"content": task_title}}]},
                "Completed": {"checkbox": task_completed}
            }
        }

        # Create a new task entry in the Notion database
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            print("✅ Task updated in Notion!")
        else:
            print("❌ Failed to update Notion:", response.text)

update_notion_task()
