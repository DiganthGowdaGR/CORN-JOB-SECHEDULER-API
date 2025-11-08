#!/usr/bin/env python3
"""
Email System with System Health Check Integration
"""

import smtplib
import sys
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json
import subprocess
from email_config import load_email_config

def send_email(to_email, subject, body, html_body=None):
    """Send an email using configured credentials"""
    config = load_email_config()
    
    if not config:
        print("❌ Email not configured. Please configure email first.")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = config['email']
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add plain text body
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)
        
        # Add HTML body if provided
        if html_body:
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
        
        # Connect to server and send email
        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        server.starttls()
        server.login(config['email'], config['password'])
        
        text = msg.as_string()
        server.sendmail(config['email'], to_email, text)
        server.quit()
        
        print(f"✅ Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False

def send_system_health_email(to_email):
    """Send system health check email with most recent scheduled check data"""
    
    # Get data from most recent scheduled health check (not run new check)
    try:
        # Try to read from history first (scheduled checks)
        history_file = 'system_health_history.json'
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
            if history:
                data = history[-1]  # Most recent check
        else:
            # Fallback to current report if no history
            with open('system_report.json', 'r') as f:
                data = json.load(f)
    except Exception as e:
        print(f"❌ Failed to get system data: {e}")
        return False
    
    # Create email subject
    subject = f"🏥 System Health Check - {data['health']['status']} - {data['timestamp']}"
    
    # Create plain text body
    body = f"""
System Health Check Report
==========================

Checked At: {data['timestamp']}
System Owner: {data['system_owner']}
Hostname: {data['hostname']}
Operating System: {data['os']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 CPU INFORMATION:
  Usage: {data['cpu']['usage_percent']}%
  Cores: {data['cpu']['cores']}
  Frequency: {data['cpu']['frequency_mhz']} MHz

💾 MEMORY INFORMATION:
  Total: {data['memory']['total_gb']} GB
  Used: {data['memory']['used_gb']} GB
  Available: {data['memory']['available_gb']} GB
  Usage: {data['memory']['usage_percent']}%

💿 DISK INFORMATION:
  Total: {data['disk']['total_gb']} GB
  Used: {data['disk']['used_gb']} GB
  Free: {data['disk']['free_gb']} GB
  Usage: {data['disk']['usage_percent']}%

🏥 SYSTEM HEALTH STATUS: {data['health']['status']}
"""
    
    for issue in data['health']['issues']:
        body += f"  • {issue}\n"
    
    body += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    body += "\nThis is an automated system health check email.\n"
    
    # Create HTML body
    health_color = {
        'Healthy': '#28a745',
        'Warning': '#ffc107',
        'Critical': '#dc3545'
    }.get(data['health']['status'], '#6c757d')
    
    cpu_color = '#dc3545' if data['cpu']['usage_percent'] > 80 else '#ffc107' if data['cpu']['usage_percent'] > 60 else '#28a745'
    mem_color = '#dc3545' if data['memory']['usage_percent'] > 85 else '#ffc107' if data['memory']['usage_percent'] > 70 else '#28a745'
    disk_color = '#dc3545' if data['disk']['usage_percent'] > 90 else '#ffc107' if data['disk']['usage_percent'] > 75 else '#28a745'
    
    html_body = f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background-color: {health_color}; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .info-box {{ background-color: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #007bff; }}
        .metric {{ margin: 15px 0; }}
        .metric-name {{ font-weight: bold; color: #555; }}
        .metric-value {{ font-size: 1.2em; color: #000; }}
        .progress-bar {{ background-color: #e9ecef; height: 25px; border-radius: 5px; overflow: hidden; margin: 5px 0; }}
        .progress-fill {{ height: 100%; text-align: center; line-height: 25px; color: white; font-weight: bold; }}
        .health-status {{ padding: 15px; margin: 20px 0; border-radius: 5px; background-color: {health_color}; color: white; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #007bff; color: white; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏥 System Health Check Report</h1>
        <p>Status: {data['health']['status']}</p>
    </div>
    
    <div class="content">
        <div class="info-box">
            <p><strong>Checked At:</strong> {data['timestamp']}</p>
            <p><strong>System Owner:</strong> {data['system_owner']}</p>
            <p><strong>Hostname:</strong> {data['hostname']}</p>
            <p><strong>Operating System:</strong> {data['os']}</p>
        </div>
        
        <h2>📊 System Resources</h2>
        
        <table>
            <tr>
                <th>Resource</th>
                <th>Usage</th>
                <th>Details</th>
                <th>Status</th>
            </tr>
            <tr>
                <td><strong>CPU</strong></td>
                <td>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {data['cpu']['usage_percent']}%; background-color: {cpu_color};">
                            {data['cpu']['usage_percent']}%
                        </div>
                    </div>
                </td>
                <td>{data['cpu']['cores']} cores @ {data['cpu']['frequency_mhz']} MHz</td>
                <td style="color: {cpu_color};">●</td>
            </tr>
            <tr>
                <td><strong>Memory</strong></td>
                <td>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {data['memory']['usage_percent']}%; background-color: {mem_color};">
                            {data['memory']['usage_percent']}%
                        </div>
                    </div>
                </td>
                <td>{data['memory']['used_gb']} GB / {data['memory']['total_gb']} GB</td>
                <td style="color: {mem_color};">●</td>
            </tr>
            <tr>
                <td><strong>Disk</strong></td>
                <td>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {data['disk']['usage_percent']}%; background-color: {disk_color};">
                            {data['disk']['usage_percent']}%
                        </div>
                    </div>
                </td>
                <td>{data['disk']['used_gb']} GB / {data['disk']['total_gb']} GB</td>
                <td style="color: {disk_color};">●</td>
            </tr>
        </table>
        
        <div class="health-status">
            <h3>Health Status: {data['health']['status']}</h3>
            <ul>
"""
    
    for issue in data['health']['issues']:
        html_body += f"                <li>{issue}</li>\n"
    
    html_body += """
            </ul>
        </div>
    </div>
    
    <div class="footer">
        <p>This is an automated system health check email from Task Scheduler.</p>
        <p>Generated at """ + data['timestamp'] + """</p>
    </div>
</body>
</html>
"""
    
    return send_email(to_email, subject, body, html_body)

def send_custom_email(to_email, subject, message):
    """Send a custom email"""
    body = f"""
{message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
From: Task Scheduler System
"""
    
    html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; padding: 20px;">
    <div style="background-color: #007bff; color: white; padding: 20px; border-radius: 5px;">
        <h2>{subject}</h2>
    </div>
    <div style="padding: 20px; background-color: #f8f9fa; margin-top: 20px; border-radius: 5px;">
        <p style="font-size: 1.1em; line-height: 1.6;">{message}</p>
    </div>
    <div style="text-align: center; padding: 20px; color: #666; font-size: 0.9em;">
        <p>Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>From: Task Scheduler System</p>
    </div>
</body>
</html>
"""
    
    return send_email(to_email, subject, body, html_body)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python email_system.py health <recipient_email>")
        print("  python email_system.py custom <recipient_email> <subject> <message>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "health":
        if len(sys.argv) < 3:
            print("Usage: python email_system.py health <recipient_email>")
            sys.exit(1)
        send_system_health_email(sys.argv[2])
    
    elif command == "custom":
        if len(sys.argv) < 5:
            print("Usage: python email_system.py custom <recipient_email> <subject> <message>")
            sys.exit(1)
        send_custom_email(sys.argv[2], sys.argv[3], sys.argv[4])
    
    else:
        print(f"Unknown command: {command}")
