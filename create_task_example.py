#!/usr/bin/env python3
"""
Example: How to create tasks using the API
"""

import requests
import json

# API endpoint
BASE_URL = "http://localhost:8001"

def create_task_example():
    """Example of creating different types of tasks"""
    
    # Example 1: Simple Python script task
    task1 = {
        "task_name": "Health Check",
        "command": "python example_tasks.py health_check",
        "schedule": "*/5 * * * *",  # Every 5 minutes
        "description": "Run system health check every 5 minutes"
    }
    
    # Example 2: File backup task
    task2 = {
        "task_name": "Daily Backup", 
        "command": "python example_tasks.py backup_database",
        "schedule": "0 2 * * *",  # Daily at 2 AM
        "description": "Backup database daily at 2 AM"
    }
    
    # Example 3: Log cleanup task
    task3 = {
        "task_name": "Weekly Cleanup",
        "command": "python example_tasks.py cleanup_logs", 
        "schedule": "0 0 * * 0",  # Every Sunday at midnight
        "description": "Clean up old log files weekly"
    }
    
    # Example 4: Custom Windows command
    task4 = {
        "task_name": "Directory Listing",
        "command": "dir C:\\temp",  # Windows command
        "schedule": "0 9 * * 1-5",  # Weekdays at 9 AM
        "description": "List temp directory contents on weekdays"
    }
    
    tasks = [task1, task2, task3, task4]
    
    print("🚀 Creating example tasks...\n")
    
    for i, task in enumerate(tasks, 1):
        print(f"{i}. Creating task: {task['task_name']}")
        
        try:
            response = requests.post(f"{BASE_URL}/tasks", json=task)
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success! Task ID: {result['id']}")
                print(f"   📅 Schedule: {task['schedule']}")
                print(f"   💻 Command: {task['command']}")
            else:
                print(f"   ❌ Failed: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()

def list_all_tasks():
    """List all created tasks"""
    print("📋 Current tasks:")
    try:
        response = requests.get(f"{BASE_URL}/tasks")
        if response.status_code == 200:
            tasks = response.json()
            for task in tasks:
                print(f"   • {task['task_name']} (ID: {task['id']}) - {task['status']}")
        else:
            print(f"   ❌ Failed to get tasks: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    create_task_example()
    print("\n" + "="*50)
    list_all_tasks()