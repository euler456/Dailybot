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
    tasks = {
        "Monday": [
            {"task": " Work on Auto Triage", "completed": False},
            {"task": " Learn Python scripting (1hr)", "completed": False},
            {"task": " Write a script", "completed": False},
        ],
        "Tuesday": [
            {"task": " Work on Auto", "completed": False},
            {"task": " Learn Google Cloud Basics", "completed": False},
            {"task": " Watch GCP video (30 mins)", "completed": False},
        ],
        "Wednesday": [
            {"task": " Debug automation issues", "completed": False},
            {"task": " Learn CI/CD (Jenkins, GitHub Actions)", "completed": False},
            {"task": " Deploy script to cloud", "completed": False},
        ],
        "Thursday": [
            {"task": " Auto tasks", "completed": False},
            {"task": " Learn Python OOP", "completed": False},
            {"task": " Build a small automation tool", "completed": False},
        ],
        "Friday": [
            {"task": " Review Auto scripts", "completed": False},
            {"task": " Learn Google Cloud Networking", "completed": False},
            {"task": " Set up test VM", "completed": False},
        ],
        "Saturday": [
            {"task": " Solve 2 LeetCode problems (1 EZ, 1 MED)", "completed": False},
            {"task": " Improve coding skills", "completed": False},
        ],
        "Sunday": [
            {"task": " Weekly review", "completed": False},
            {"task": " Plan next week", "completed": False},
        ],
    }

    today = datetime.datetime.today().strftime('%A')
    return today, tasks.get(today, [])

def get_all_tasks():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
    }

    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()["results"]
    else:
        print(" Failed to fetch tasks:", response.text)
        return []

def clear_tasks_on_monday():
    if datetime.datetime.today().strftime('%A') == "Monday":
        print(" Clearing all tasks for a fresh start!")
        
        tasks = get_all_tasks()
        for task in tasks:
            task_id = task["id"]  
            archive_task(task_id)
def check_repeat():
    tasks = get_all_tasks()
    today_str = datetime.datetime.today().strftime('%Y-%m-%d')
    
    no_date_tasks = True  # Flag to track if we need to add new tasks
    
    for task in tasks:
        task_id = task["id"]
        task_date = task["properties"].get("Completion Date", {}).get("date", {}).get("start")

        if task_date:
            print(f" Task {task_id} has a completion date: {task_date}")
            if task_date != today_str:
                print(f" Updating task from {task_date} to today...")
                update_notion_task(task_date)
        else:
            print(f" Task {task_id} has no completion date. Needs to be added!")
            no_date_tasks = False  # Indicate that tasks need to be added

    # If no tasks have a valid completion date, add today's tasks
    if no_date_tasks:
        print(" No valid tasks found for today. Adding new tasks!")
        update_notion_task(None)


def archive_task(task_id):
    url = f"https://api.notion.com/v1/pages/{task_id}"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    data = {"archived": True}  

    response = requests.patch(url, json=data, headers=headers)

    if response.status_code == 200:
        print(f" Task {task_id} archived!")
    else:
        print(f" Failed to archive task {task_id}: {response.text}")

def update_notion_task(task_date):
    today_str = datetime.datetime.today().strftime('%Y-%m-%d')

    if task_date != today_str:
        date_long = datetime.datetime.today().strftime('%m-%d, %A')  
        day, task_list = get_weekday_tasks()

        clear_tasks_on_monday()  # Ensure Monday tasks are cleared

        url = "https://api.notion.com/v1/pages"
        headers = {
            "Authorization": f"Bearer {NOTION_API_KEY}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

        for task in task_list:
            data = {
                "parent": {"database_id": DATABASE_ID},
                "properties": {
                    "Name": {"title": [{"text": {"content": date_long}}]},
                    "Task": {"rich_text": [{"text": {"content": task["task"]}}]},
                    "Completed": {"checkbox": task["completed"]},
                    "Completion Date": {"date": {"start": today_str}}
                }
            }

            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                print(f"Task '{task['task']}' added for {date_long}!")
            else:
                print(f" Failed to add task '{task['task']}' for {date_long}:", response.text)

    
check_repeat()
