#!/usr/bin/env python3
"""
Examples of different types of commands you can schedule
"""

import requests

BASE_URL = "http://localhost:8001"

# Different types of commands you can schedule:

COMMAND_EXAMPLES = [
    {
        "task_name": "Python Script",
        "command": "python my_script.py",
        "schedule": "0 9 * * *",
        "description": "Run a Python script daily"
    },
    {
        "task_name": "Windows Command",
        "command": "dir C:\\Users",
        "schedule": "*/30 * * * *",
        "description": "List directory contents every 30 minutes"
    },
    {
        "task_name": "PowerShell Script",
        "command": "powershell -File backup.ps1",
        "schedule": "0 2 * * *",
        "description": "Run PowerShell backup script"
    },
    {
        "task_name": "Batch File",
        "command": "cleanup.bat",
        "schedule": "0 0 * * 0",
        "description": "Run batch file weekly"
    },
    {
        "task_name": "System Command",
        "command": "echo Hello World > output.txt",
        "schedule": "*/5 * * * *",
        "description": "Write to file every 5 minutes"
    },
    {
        "task_name": "Multiple Commands",
        "command": "echo Starting backup && python backup.py && echo Backup complete",
        "schedule": "0 3 * * *",
        "description": "Chain multiple commands"
    },
    {
        "task_name": "File Copy",
        "command": "copy important.txt backup\\important_backup.txt",
        "schedule": "0 */4 * * *",
        "description": "Copy file every 4 hours"
    },
    {
        "task_name": "Network Check",
        "command": "ping google.com",
        "schedule": "*/15 * * * *",
        "description": "Check network connectivity"
    }
]

def show_command_examples():
    """Display different command examples"""
    print("💻 Command Examples for Task Scheduling\n")
    
    for i, example in enumerate(COMMAND_EXAMPLES, 1):
        print(f"{i}. {example['task_name']}")
        print(f"   Command: {example['command']}")
        print(f"   Schedule: {example['schedule']}")
        print(f"   Description: {example['description']}")
        print()

def create_sample_task():
    """Create one sample task"""
    sample_task = {
        "task_name": "Sample Echo Task",
        "command": "echo Current time: %date% %time%",
        "schedule": "*/2 * * * *",  # Every 2 minutes
        "description": "Print current date and time every 2 minutes"
    }
    
    print("🚀 Creating sample task...")
    try:
        response = requests.post(f"{BASE_URL}/tasks", json=sample_task)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Sample task created! ID: {result['id']}")
            print(f"   This task will run every 2 minutes")
            print(f"   Check the task history in a few minutes to see results")
        else:
            print(f"❌ Failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    show_command_examples()
    print("="*60)
    create_sample_task()