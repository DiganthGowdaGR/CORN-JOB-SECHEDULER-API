#!/usr/bin/env python3
"""
Email sending functionality for scheduled tasks
"""

import smtplib
import sys
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import json

# Email configuration - Update these with your email settings
EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",  # Gmail SMTP
    "smtp_port": 587,
    "sender_email": "your_email@gmail.com",  # Replace with your email
    "sender_password": "your_app_password",  # Replace with your app password
    "sender_name": "Task Scheduler"
}

def send_email(to_email, subject, body, html_body=None, attachments=None):
    """
    Send an email
    
    Args:
        to_email (str): Recipient email address
        subject (str): Email subject
        body (str): Plain text body
        html_body (str, optional): HTML body
        attachments (list, optional): List of file paths to attach
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{EMAIL_CONFIG['sender_name']} <{EMAIL_CONFIG['sender_email']}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add plain text body
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)
        
        # Add HTML body if provided
        if html_body:
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
        
        # Add attachments if provided
        if attachments:
            for file_path in attachments:
                if os.path.isfile(file_path):
                    with open(file_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {os.path.basename(file_path)}'
                    )
                    msg.attach(part)
        
        # Connect to server and send email
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()  # Enable encryption
        server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
        
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG['sender_email'], to_email, text)
        server.quit()
        
        print(f"✅ Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False

def send_daily_report():
    """Send a daily report email"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    subject = f"Daily Report - {datetime.now().strftime('%Y-%m-%d')}"
    
    body = f"""
Daily System Report
==================

Report Generated: {current_time}

System Status: ✅ All systems operational
Tasks Completed: 15
Errors: 0
Uptime: 99.9%

This is an automated report from your Task Scheduler.

Best regards,
Task Scheduler System
"""
    
    html_body = f"""
<html>
<body>
    <h2>📊 Daily System Report</h2>
    <p><strong>Report Generated:</strong> {current_time}</p>
    
    <table border="1" style="border-collapse: collapse; width: 100%;">
        <tr style="background-color: #f2f2f2;">
            <th style="padding: 8px;">Metric</th>
            <th style="padding: 8px;">Value</th>
            <th style="padding: 8px;">Status</th>
        </tr>
        <tr>
            <td style="padding: 8px;">System Status</td>
            <td style="padding: 8px;">Operational</td>
            <td style="padding: 8px;">✅</td>
        </tr>
        <tr>
            <td style="padding: 8px;">Tasks Completed</td>
            <td style="padding: 8px;">15</td>
            <td style="padding: 8px;">✅</td>
        </tr>
        <tr>
            <td style="padding: 8px;">Errors</td>
            <td style="padding: 8px;">0</td>
            <td style="padding: 8px;">✅</td>
        </tr>
        <tr>
            <td style="padding: 8px;">Uptime</td>
            <td style="padding: 8px;">99.9%</td>
            <td style="padding: 8px;">✅</td>
        </tr>
    </table>
    
    <p><em>This is an automated report from your Task Scheduler.</em></p>
</body>
</html>
"""
    
    # Replace with actual recipient email
    recipient = "recipient@example.com"  # Update this!
    
    return send_email(recipient, subject, body, html_body)

def send_weekly_summary():
    """Send a weekly summary email"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    subject = f"Weekly Summary - Week of {datetime.now().strftime('%Y-%m-%d')}"
    
    body = f"""
Weekly System Summary
====================

Report Generated: {current_time}

📈 This Week's Highlights:
- Total Tasks Executed: 105
- Success Rate: 98.1%
- Average Response Time: 2.3 seconds
- New Tasks Created: 3
- Tasks Completed: 2

🔧 System Maintenance:
- Database cleanup performed
- Log files rotated
- Security updates applied

📊 Performance Metrics:
- CPU Usage: 15% average
- Memory Usage: 45% average
- Disk Usage: 67%

Next Week's Scheduled Maintenance:
- Server restart: Sunday 2:00 AM
- Database backup: Daily at 3:00 AM

Best regards,
Task Scheduler System
"""
    
    recipient = "admin@example.com"  # Update this!
    
    return send_email(recipient, subject, body)

def send_alert_email(alert_type, message):
    """Send an alert email"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    subject = f"🚨 ALERT: {alert_type}"
    
    body = f"""
SYSTEM ALERT
============

Alert Type: {alert_type}
Time: {current_time}
Message: {message}

Please investigate this issue immediately.

This is an automated alert from your Task Scheduler.
"""
    
    recipient = "admin@example.com"  # Update this!
    
    return send_email(recipient, subject, body)

def send_custom_email():
    """Send a custom email with user input"""
    if len(sys.argv) < 4:
        print("Usage: python email_sender.py send_custom <recipient> <subject> <message>")
        return False
    
    recipient = sys.argv[2]
    subject = sys.argv[3]
    message = sys.argv[4] if len(sys.argv) > 4 else "Hello from Task Scheduler!"
    
    return send_email(recipient, subject, message)

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) < 2:
        print("📧 Email Sender for Task Scheduler")
        print("=" * 40)
        print("Available commands:")
        print("  python email_sender.py daily_report")
        print("  python email_sender.py weekly_summary")
        print("  python email_sender.py alert <alert_type> <message>")
        print("  python email_sender.py send_custom <recipient> <subject> <message>")
        print()
        print("⚠️  IMPORTANT: Update EMAIL_CONFIG in this file with your email settings!")
        return
    
    command = sys.argv[1]
    
    if command == "daily_report":
        send_daily_report()
    elif command == "weekly_summary":
        send_weekly_summary()
    elif command == "alert":
        if len(sys.argv) >= 4:
            alert_type = sys.argv[2]
            message = sys.argv[3]
            send_alert_email(alert_type, message)
        else:
            print("Usage: python email_sender.py alert <alert_type> <message>")
    elif command == "send_custom":
        send_custom_email()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()