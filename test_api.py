#!/usr/bin/env python3
"""
Test script to demonstrate the Scheduled Task Execution Service API
"""

import requests
import json
import time

BASE_URL = "http://localhost:8001"

def test_api():
    print("🚀 Testing Scheduled Task Execution Service API\n")
    
    # Test 1: Create a task
    print("1. Creating a new task...")
    task_data = {
        "task_name": "Health Check",
        "command": "python example_tasks.py health_check",
        "schedule": "*/2 * * * *",  # Every 2 minutes
        "description": "Run system health check every 2 minutes"
    }
    
    response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    if response.status_code == 200:
        task = response.json()
        task_id = task['id']
        print(f"✅ Task created successfully! ID: {task_id}")
        print(f"   Name: {task['task_name']}")
        print(f"   Schedule: {task['schedule']}")
    else:
        print(f"❌ Failed to create task: {response.text}")
        return
    
    # Test 2: List all tasks
    print("\n2. Listing all tasks...")
    response = requests.get(f"{BASE_URL}/tasks")
    if response.status_code == 200:
        tasks = response.json()
        print(f"✅ Found {len(tasks)} task(s)")
        for task in tasks:
            print(f"   - {task['task_name']} (ID: {task['id']}, Status: {task['status']})")
    else:
        print(f"❌ Failed to list tasks: {response.text}")
    
    # Test 3: Get specific task
    print(f"\n3. Getting task details for ID {task_id}...")
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    if response.status_code == 200:
        task = response.json()
        print(f"✅ Task details retrieved:")
        print(f"   Name: {task['task_name']}")
        print(f"   Command: {task['command']}")
        print(f"   Schedule: {task['schedule']}")
        print(f"   Status: {task['status']}")
    else:
        print(f"❌ Failed to get task: {response.text}")
    
    # Test 4: Create another task
    print("\n4. Creating a backup task...")
    backup_task = {
        "task_name": "Daily Backup",
        "command": "python example_tasks.py backup_database",
        "schedule": "0 2 * * *",  # Daily at 2 AM
        "description": "Run daily database backup"
    }
    
    response = requests.post(f"{BASE_URL}/tasks", json=backup_task)
    if response.status_code == 200:
        backup_task_id = response.json()['id']
        print(f"✅ Backup task created! ID: {backup_task_id}")
    else:
        print(f"❌ Failed to create backup task: {response.text}")
    
    # Test 5: Update task
    print(f"\n5. Updating task {task_id}...")
    update_data = {
        "description": "Updated: Run system health check every 2 minutes"
    }
    
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=update_data)
    if response.status_code == 200:
        print("✅ Task updated successfully!")
    else:
        print(f"❌ Failed to update task: {response.text}")
    
    # Test 6: Wait and check execution history
    print(f"\n6. Waiting 3 minutes for task execution...")
    print("   (The health check task should execute at least once)")
    time.sleep(180)  # Wait 3 minutes
    
    response = requests.get(f"{BASE_URL}/tasks/{task_id}/history")
    if response.status_code == 200:
        history = response.json()
        print(f"✅ Task execution history ({len(history)} executions):")
        for execution in history[:3]:  # Show last 3 executions
            print(f"   - {execution['execution_time']}: {execution['status']}")
            if execution['output']:
                print(f"     Output: {execution['output'][:100]}...")
    else:
        print(f"❌ Failed to get task history: {response.text}")
    
    # Test 7: Delete task
    print(f"\n7. Deleting task {task_id}...")
    response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    if response.status_code == 200:
        print("✅ Task deleted successfully!")
    else:
        print(f"❌ Failed to delete task: {response.text}")
    
    print("\n🎉 API testing completed!")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API server.")
        print("   Make sure the server is running: python main.py")
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")