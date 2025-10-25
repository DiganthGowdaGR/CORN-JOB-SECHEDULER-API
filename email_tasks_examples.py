#!/usr/bin/env python3
"""
Example email tasks that can be scheduled
"""

import requests
import json

BASE_URL = "http://localhost:8001"

def create_email_tasks():
    """Create example email tasks"""
    
    print("📧 Creating Email Task Examples")
    print("=" * 40)
    
    # Email tasks to create
    email_tasks = [
        {
            "task_name": "Daily Report Email",
            "command": "python email_sender.py daily_report",
            "schedule": "0 9 * * *",  # Daily at 9 AM
            "description": "Send daily system report via email every morning"
        },
        {
            "task_name": "Weekly Summary Email",
            "command": "python email_sender.py weekly_summary",
            "schedule": "0 9 * * 1",  # Every Monday at 9 AM
            "description": "Send weekly summary report every Monday morning"
        },
        {
            "task_name": "System Health Alert",
            "command": "python email_sender.py alert 'System Check' 'Automated system health check completed successfully'",
            "schedule": "0 */6 * * *",  # Every 6 hours
            "description": "Send system health status email every 6 hours"
        },
        {
            "task_name": "Monthly Backup Notification",
            "command": "python email_sender.py send_custom admin@company.com 'Monthly Backup Complete' 'The monthly backup has been completed successfully.'",
            "schedule": "0 2 1 * *",  # First day of month at 2 AM
            "description": "Send monthly backup completion notification"
        },
        {
            "task_name": "Weekend Reminder",
            "command": "python email_sender.py send_custom team@company.com 'Weekend Reminder' 'Don\\'t forget to review the weekly reports before Monday!'",
            "schedule": "0 17 * * 5",  # Every Friday at 5 PM
            "description": "Send weekend reminder email to team every Friday"
        }
    ]
    
    created_tasks = []
    
    for task in email_tasks:
        print(f"\n📝 Creating: {task['task_name']}")
        
        try:
            response = requests.post(f"{BASE_URL}/tasks", json=task)
            if response.status_code == 200:
                result = response.json()
                created_tasks.append(result)
                print(f"   ✅ Created! Task ID: {result['id']}")
                print(f"   📅 Schedule: {task['schedule']}")
                print(f"   📧 Command: {task['command']}")
            else:
                print(f"   ❌ Failed: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n🎉 Created {len(created_tasks)} email tasks!")
    
    if created_tasks:
        print("\n📋 Summary of Created Email Tasks:")
        for task in created_tasks:
            print(f"   • {task['task_name']} (ID: {task['id']})")
    
    return created_tasks

def show_email_examples():
    """Show examples of email commands"""
    
    print("\n📧 Email Command Examples")
    print("=" * 40)
    
    examples = [
        {
            "name": "Daily Report",
            "command": "python email_sender.py daily_report",
            "description": "Sends a formatted daily system report"
        },
        {
            "name": "Weekly Summary", 
            "command": "python email_sender.py weekly_summary",
            "description": "Sends a weekly summary with statistics"
        },
        {
            "name": "Custom Alert",
            "command": "python email_sender.py alert 'Server Down' 'The main server is not responding'",
            "description": "Sends an alert email with custom message"
        },
        {
            "name": "Custom Email",
            "command": "python email_sender.py send_custom user@example.com 'Hello' 'This is a test message'",
            "description": "Sends a custom email to specific recipient"
        },
        {
            "name": "Backup Notification",
            "command": "python email_sender.py send_custom admin@company.com 'Backup Complete' 'Daily backup finished successfully at %date% %time%'",
            "description": "Sends backup completion notification"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['name']}")
        print(f"   Command: {example['command']}")
        print(f"   Description: {example['description']}")

def main():
    """Main function"""
    print("📧 Email Tasks for Task Scheduler")
    print("=" * 40)
    print("1. Create example email tasks")
    print("2. Show email command examples")
    print("3. Both")
    
    choice = input("\nEnter your choice (1-3): ")
    
    if choice == "1":
        create_email_tasks()
    elif choice == "2":
        show_email_examples()
    elif choice == "3":
        show_email_examples()
        create_email_tasks()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()