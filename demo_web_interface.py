#!/usr/bin/env python3
"""
Demo script to show the web interface functionality
"""

import webbrowser
import time
import requests

def demo_web_interface():
    """Demonstrate the web interface"""
    
    print("🌐 Task Scheduler Web Interface Demo")
    print("="*50)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8001/api")
        print("✅ Server is running!")
    except:
        print("❌ Server is not running. Please start it with: python main.py")
        return
    
    print("\n📋 Available Web Pages:")
    print("1. Dashboard: http://localhost:8001/")
    print("2. Create Task: http://localhost:8001/create")
    print("3. API Documentation: http://localhost:8001/docs")
    
    print("\n🚀 Opening web interface in your browser...")
    
    # Open the dashboard in browser
    webbrowser.open("http://localhost:8001/")
    
    print("\n✨ Web Interface Features:")
    print("• 📊 Dashboard - View all your scheduled tasks")
    print("• ➕ Create Task - User-friendly form to create new tasks")
    print("• 👁️ View Task - See task details and execution history")
    print("• ⏸️ Pause/Resume - Toggle task status")
    print("• 🗑️ Delete - Remove tasks with confirmation")
    print("• 📈 Statistics - Success rates and execution counts")
    
    print("\n🎯 How to Use:")
    print("1. Go to http://localhost:8001/ in your browser")
    print("2. Click 'Create New Task' to add a scheduled task")
    print("3. Fill in the form with:")
    print("   - Task name (e.g., 'Daily Backup')")
    print("   - Command (e.g., 'echo Hello World')")
    print("   - Schedule (e.g., '*/2 * * * *' for every 2 minutes)")
    print("   - Description (optional)")
    print("4. Click 'Create Task' to save")
    print("5. View your tasks on the dashboard")
    print("6. Click 'View' to see execution history")
    
    print("\n💡 Quick Schedule Examples:")
    print("• */2 * * * * - Every 2 minutes (good for testing)")
    print("• 0 9 * * * - Daily at 9 AM")
    print("• 0 9 * * 1 - Every Monday at 9 AM")
    print("• 0 0 1 * * - First day of each month")
    
    print("\n🔧 Sample Commands to Try:")
    print("• echo Current time: %date% %time%")
    print("• python example_tasks.py health_check")
    print("• dir C:\\temp")
    print("• ping google.com")

if __name__ == "__main__":
    demo_web_interface()