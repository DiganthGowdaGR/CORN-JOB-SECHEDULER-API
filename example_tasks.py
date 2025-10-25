#!/usr/bin/env python3
"""
Example scripts that can be scheduled as tasks
"""

import datetime
import os

def send_report():
    """Example: Send weekly report"""
    print(f"[{datetime.datetime.now()}] Sending weekly report...")
    # Simulate report generation
    print("Report generated successfully!")
    return "Weekly report sent"

def cleanup_logs():
    """Example: Cleanup old log files"""
    print(f"[{datetime.datetime.now()}] Cleaning up old log files...")
    # Simulate cleanup
    print("Cleaned up 5 old log files")
    return "Cleanup completed"

def backup_database():
    """Example: Database backup"""
    print(f"[{datetime.datetime.now()}] Starting database backup...")
    # Simulate backup
    print("Database backup completed successfully!")
    return "Backup completed"

def health_check():
    """Example: System health check"""
    print(f"[{datetime.datetime.now()}] Running system health check...")
    print("CPU: OK")
    print("Memory: OK") 
    print("Disk: OK")
    return "Health check passed"

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python example_tasks.py <function_name>")
        print("Available functions: send_report, cleanup_logs, backup_database, health_check")
        sys.exit(1)
    
    function_name = sys.argv[1]
    
    functions = {
        'send_report': send_report,
        'cleanup_logs': cleanup_logs,
        'backup_database': backup_database,
        'health_check': health_check
    }
    
    if function_name in functions:
        result = functions[function_name]()
        print(f"Result: {result}")
    else:
        print(f"Unknown function: {function_name}")
        sys.exit(1)