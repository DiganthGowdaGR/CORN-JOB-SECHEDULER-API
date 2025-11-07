#!/usr/bin/env python3
"""
Test script to verify the bug fix in the scheduler's update_task method.
"""

import requests
import time
import os

BASE_URL = "http://localhost:8001"
OUTPUT_FILE = "test_output.txt"

def cleanup():
    """Remove the output file if it exists."""
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

def test_command_update_fix():
    """
    Tests if updating a task's command is correctly handled by the scheduler.
    """
    print("🚀 Testing command update bug fix\n")
    cleanup()

    # 1. Create a task with an initial command
    print("1. Creating a new task...")
    initial_command = f"echo 'initial command' > {OUTPUT_FILE}"
    task_data = {
        "task_name": "Bug Fix Test Task",
        "command": initial_command,
        "schedule": "* * * * *",  # Every minute
        "description": "A task to test the command update bug fix."
    }

    response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    if response.status_code != 200:
        print(f"❌ Failed to create task: {response.text}")
        return

    task = response.json()
    task_id = task['id']
    print(f"✅ Task created successfully! ID: {task_id}")

    # 2. Update the task's command
    print("\n2. Updating the task's command...")
    updated_command = f"echo 'updated command' > {OUTPUT_FILE}"
    update_data = {
        "command": updated_command
    }

    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=update_data)
    if response.status_code != 200:
        print(f"❌ Failed to update task: {response.text}")
        requests.delete(f"{BASE_URL}/tasks/{task_id}") # cleanup
        return

    print("✅ Task command updated successfully!")

    # 3. Wait for the task to execute
    print("\n3. Waiting 70 seconds for the task to execute...")
    time.sleep(70)

    # 4. Verify the output
    print("\n4. Verifying the output...")
    if not os.path.exists(OUTPUT_FILE):
        print("❌ Output file was not created.")
        requests.delete(f"{BASE_URL}/tasks/{task_id}") # cleanup
        return

    with open(OUTPUT_FILE, "r") as f:
        content = f.read().strip()

    if content == "updated command":
        print("✅ Test Passed: The updated command was executed.")
    else:
        print(f"❌ Test Failed: Expected 'updated command', but got '{content}'.")

    # 5. Cleanup
    print("\n5. Cleaning up...")
    requests.delete(f"{BASE_URL}/tasks/{task_id}")
    cleanup()
    print("✅ Cleanup complete.")
    print("\n🎉 Bug fix test completed!")


if __name__ == "__main__":
    try:
        test_command_update_fix()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API server.")
        print("   Make sure the server is running: python main.py")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cleanup()
