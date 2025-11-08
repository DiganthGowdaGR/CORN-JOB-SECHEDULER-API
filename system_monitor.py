#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
System Monitoring Script
Displays system owner, CPU usage, memory usage, disk space, and system health
"""

import psutil
import platform
import os
from datetime import datetime
import json

def get_system_info():
    """Gather comprehensive system information"""
    
    # Get system owner/username
    username = os.getenv('USERNAME') or os.getenv('USER') or 'Unknown'
    
    # Get CPU information
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()
    
    # Get memory information
    memory = psutil.virtual_memory()
    memory_total_gb = memory.total / (1024**3)
    memory_available_gb = memory.available / (1024**3)
    memory_used_gb = memory.used / (1024**3)
    memory_percent = memory.percent
    
    # Get disk information
    disk = psutil.disk_usage('/')
    disk_total_gb = disk.total / (1024**3)
    disk_free_gb = disk.free / (1024**3)
    disk_used_gb = disk.used / (1024**3)
    disk_percent = disk.percent
    
    # System health status
    health_status = "Healthy"
    health_issues = []
    
    if cpu_percent > 80:
        health_status = "Warning"
        health_issues.append("High CPU usage")
    
    if memory_percent > 85:
        health_status = "Warning"
        health_issues.append("High memory usage")
    
    if disk_percent > 90:
        health_status = "Critical"
        health_issues.append("Low disk space")
    
    if not health_issues:
        health_issues.append("All systems operational")
    
    # Compile report
    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "system_owner": username,
        "hostname": platform.node(),
        "os": f"{platform.system()} {platform.release()}",
        "cpu": {
            "usage_percent": round(cpu_percent, 2),
            "cores": cpu_count,
            "frequency_mhz": round(cpu_freq.current, 2) if cpu_freq else "N/A"
        },
        "memory": {
            "total_gb": round(memory_total_gb, 2),
            "used_gb": round(memory_used_gb, 2),
            "available_gb": round(memory_available_gb, 2),
            "usage_percent": round(memory_percent, 2)
        },
        "disk": {
            "total_gb": round(disk_total_gb, 2),
            "used_gb": round(disk_used_gb, 2),
            "free_gb": round(disk_free_gb, 2),
            "usage_percent": round(disk_percent, 2)
        },
        "health": {
            "status": health_status,
            "issues": health_issues
        }
    }
    
    return report

def print_report(report):
    """Print formatted system report"""
    print("\n" + "="*60)
    print("           SYSTEM MONITORING REPORT")
    print("="*60)
    print(f"Timestamp: {report['timestamp']}")
    print(f"System Owner: {report['system_owner']}")
    print(f"Hostname: {report['hostname']}")
    print(f"Operating System: {report['os']}")
    print("-"*60)
    
    print("\nCPU INFORMATION:")
    print(f"  Usage: {report['cpu']['usage_percent']}%")
    print(f"  Cores: {report['cpu']['cores']}")
    print(f"  Frequency: {report['cpu']['frequency_mhz']} MHz")
    
    print("\nMEMORY INFORMATION:")
    print(f"  Total: {report['memory']['total_gb']} GB")
    print(f"  Used: {report['memory']['used_gb']} GB")
    print(f"  Available: {report['memory']['available_gb']} GB")
    print(f"  Usage: {report['memory']['usage_percent']}%")
    
    print("\nDISK INFORMATION:")
    print(f"  Total: {report['disk']['total_gb']} GB")
    print(f"  Used: {report['disk']['used_gb']} GB")
    print(f"  Free: {report['disk']['free_gb']} GB")
    print(f"  Usage: {report['disk']['usage_percent']}%")
    
    print("\nSYSTEM HEALTH:")
    print(f"  Status: {report['health']['status']}")
    for issue in report['health']['issues']:
        print(f"  - {issue}")
    
    print("="*60 + "\n")

def main():
    """Main function"""
    report = get_system_info()
    print_report(report)
    
    # Save current report to JSON file for web display
    with open('system_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Also save to history file (append mode)
    history_file = 'system_health_history.json'
    history = []
    
    # Load existing history
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r') as f:
                history = json.load(f)
        except:
            history = []
    
    # Add current report to history
    history.append(report)
    
    # Keep only last 50 reports
    if len(history) > 50:
        history = history[-50:]
    
    # Save updated history
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)
    
    print("✅ Report saved to system_report.json")
    print(f"✅ History updated ({len(history)} records)")

if __name__ == "__main__":
    main()
