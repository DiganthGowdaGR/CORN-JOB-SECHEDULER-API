#!/usr/bin/env python3
"""
Simple command-line client to manage scheduled tasks
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8001"

def print_header(title):
    print("\n" + "="*50)
    print(f"  {title}")
    print("="*50)

def create_task():
    """Interactive task creation"""
    print_header("CREATE NEW TASK")
    
    print("Enter task details:")
    task_name = input("Task Name: ")
    command = input("Command to execute: ")
    
    print("\nSchedule examples:")
    print("  */5 * * * *  - Every 5 minutes")
    print("  0 9 * * *    - Daily at 9 AM")
    print("  0 9 * * 1    - Every Monday at 9 AM")
    print("  0 0 1 * *    - First day of month")
    
    schedule = input("Schedule (cron format): ")
    description = input("Description (optional): ")
    
    task_data = {
        "task_name": task_name,
        "command": command,
        "schedule": schedule,
        "description": description if description else None
    }
    
    try:
        response = requests.post(f"{BASE_URL}/tasks", json=task_data)
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Task created successfully!")
            print(f"   Task ID: {result['id']}")
            print(f"   Name: {result['task_name']}")
            print(f"   Schedule: {result['schedule']}")
        else:
            print(f"\n❌ Failed to create task: {response.text}")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def list_tasks():
    """List all tasks"""
    print_header("ALL SCHEDULED TASKS")
    
    try:
        response = requests.get(f"{BASE_URL}/tasks")
        if response.status_code == 200:
            tasks = response.json()
            if not tasks:
                print("No tasks found.")
                return
            
            for task in tasks:
                print(f"\n📋 Task ID: {task['id']}")
                print(f"   Name: {task['task_name']}")
                print(f"   Command: {task['command']}")
                print(f"   Schedule: {task['schedule']}")
                print(f"   Status: {task['status']}")
                if task.get('description'):
                    print(f"   Description: {task['description']}")
                if task.get('last_run'):
                    print(f"   Last Run: {task['last_run']}")
        else:
            print(f"❌ Failed to get tasks: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def view_task_history():
    """View execution history for a task"""
    print_header("TASK EXECUTION HISTORY")
    
    task_id = input("Enter Task ID: ")
    
    try:
        response = requests.get(f"{BASE_URL}/tasks/{task_id}/history")
        if response.status_code == 200:
            history = response.json()
            if not history:
                print("No execution history found.")
                return
            
            print(f"\n📊 Execution History for Task {task_id}:")
            for execution in history[:10]:  # Show last 10 executions
                status_icon = "✅" if execution['status'] == 'success' else "❌"
                print(f"\n{status_icon} {execution['execution_time']} - {execution['status']}")
                if execution.get('output'):
                    print(f"   Output: {execution['output'][:100]}...")
                if execution.get('error'):
                    print(f"   Error: {execution['error'][:100]}...")
        else:
            print(f"❌ Failed to get history: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def delete_task():
    """Delete a task"""
    print_header("DELETE TASK")
    
    # First show current tasks
    list_tasks()
    
    task_id = input("\nEnter Task ID to delete: ")
    confirm = input(f"Are you sure you want to delete task {task_id}? (y/N): ")
    
    if confirm.lower() == 'y':
        try:
            response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
            if response.status_code == 200:
                print(f"\n✅ Task {task_id} deleted successfully!")
            else:
                print(f"\n❌ Failed to delete task: {response.text}")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    else:
        print("Delete cancelled.")

def main_menu():
    """Main menu"""
    while True:
        print_header("SCHEDULED TASK MANAGER")
        print("1. Create New Task")
        print("2. List All Tasks") 
        print("3. View Task History")
        print("4. Delete Task")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ")
        
        if choice == '1':
            create_task()
        elif choice == '2':
            list_tasks()
        elif choice == '3':
            view_task_history()
        elif choice == '4':
            delete_task()
        elif choice == '5':
            print("\nGoodbye! 👋")
            break
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nExiting... 👋")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the task scheduler service.")
        print("   Make sure the server is running: python main.py")