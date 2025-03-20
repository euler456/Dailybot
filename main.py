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
        "Monday": "✅ Work on Auto Triage\n📌 Learn Python scripting (1hr)\n🎯 Write a script\n🏋️‍♂️ Gym/Rest",
        "Tuesday": "✅ Work on Auto\n📌 Learn Google Cloud Basics\n🎯 Watch GCP video (30 mins)",
        "Wednesday": "✅ Debug automation issues\n📌 Learn CI/CD (Jenkins, GitHub Actions)\n🎯 Deploy script to cloud",
        "Thursday": "✅ Auto tasks\n📌 Learn Python OOP\n🎯 Build a small automation tool",
        "Friday": "✅ Review Auto scripts\n📌 Learn Google Cloud Networking\n🎯 Set up test VM",
        "Saturday": "📌 Solve 2 LeetCode problems (1 EZ, 1 MED)\n🎯 Improve coding skills",
        "Sunday": "📌 Weekly review\n🎯 Plan next week"
    }
    return tasks.get(datetime.datetime.today().strftime('%A'), "No tasks for today")

def update_notion_task():
    task_content = get_weekday_tasks()
    
    url = "https://api.notion.com/v1/pages"  # ✅ Correct API endpoint
    
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": datetime.datetime.today().strftime('%A')}}]},
            "Tasks": {"rich_text": [{"text": {"content": task_content}}]}
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("✅ Task updated in Notion!")
    else:
        print("❌ Failed to update Notion:", response.text)

update_notion_task()
