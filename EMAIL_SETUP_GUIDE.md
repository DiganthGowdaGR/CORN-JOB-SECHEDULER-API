# 📧 Email Setup Guide for Task Scheduler

This guide will help you set up email functionality for your scheduled tasks.

## 🚀 Quick Setup

### Step 1: Configure Email Settings
```bash
python setup_email.py
```

### Step 2: Create Email Tasks
```bash
python email_tasks_examples.py
```

### Step 3: Test Your Setup
Go to `http://localhost:8001/create` and use the email task templates!

## 📋 Detailed Setup Instructions

### For Gmail Users

1. **Enable 2-Factor Authentication**
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Enable 2-Step Verification

2. **Generate App Password**
   - In Security settings, click "App passwords"
   - Select "Mail" and "Windows Computer"
   - Copy the 16-character password (no spaces)

3. **Run Setup**
   ```bash
   python setup_email.py
   ```
   - Choose option 1 (Gmail)
   - Enter your Gmail address
   - Enter the App Password (not your regular password)

### For Outlook/Hotmail Users

1. **Run Setup**
   ```bash
   python setup_email.py
   ```
   - Choose option 2 (Outlook)
   - Enter your email and password

### For Other Email Providers

1. **Get SMTP Settings**
   - Contact your email provider for SMTP settings
   - Common settings:
     - **Yahoo**: smtp.mail.yahoo.com, port 587
     - **Custom**: Ask your IT department

2. **Run Setup**
   ```bash
   python setup_email.py
   ```
   - Choose option 3 (Custom)
   - Enter your SMTP settings

## 📧 Email Task Examples

### 1. Daily Report Email
```bash
# Command to use in task scheduler:
python email_sender.py daily_report

# Schedule: 0 9 * * * (Daily at 9 AM)
```

### 2. Weekly Summary Email
```bash
# Command:
python email_sender.py weekly_summary

# Schedule: 0 9 * * 1 (Every Monday at 9 AM)
```

### 3. Custom Email
```bash
# Command:
python email_sender.py send_custom recipient@example.com "Subject" "Message"

# Example:
python email_sender.py send_custom admin@company.com "Backup Complete" "Daily backup finished successfully"
```

### 4. Alert Email
```bash
# Command:
python email_sender.py alert "Alert Type" "Alert Message"

# Example:
python email_sender.py alert "System Check" "All systems operational"
```

## 🌐 Using the Web Interface

1. **Go to Create Task Page**
   - Visit: `http://localhost:8001/create`

2. **Use Email Templates**
   - Click the blue email template buttons
   - Templates will auto-fill the form
   - Customize as needed

3. **Email Template Buttons:**
   - **Daily Report** - Sends formatted daily reports
   - **Weekly Summary** - Sends weekly statistics
   - **Custom Email** - Send custom messages
   - **Alert Email** - Send system alerts

## 🔧 Customizing Email Content

### Edit Email Templates
Open `email_sender.py` and modify these functions:
- `send_daily_report()` - Daily report content
- `send_weekly_summary()` - Weekly summary content
- `send_alert_email()` - Alert email format

### Example Customization:
```python
def send_daily_report():
    subject = f"My Custom Report - {datetime.now().strftime('%Y-%m-%d')}"
    
    body = f"""
    Custom Daily Report
    ==================
    
    Date: {datetime.now().strftime('%Y-%m-%d')}
    
    Your custom content here...
    """
    
    recipient = "your-email@example.com"  # Update this!
    return send_email(recipient, subject, body)
```

## 📅 Common Email Schedules

| Schedule | Cron Expression | Description |
|----------|----------------|-------------|
| Every hour | `0 * * * *` | Hourly reports |
| Daily 9 AM | `0 9 * * *` | Morning reports |
| Weekly Monday | `0 9 * * 1` | Weekly summaries |
| Monthly 1st | `0 9 1 * *` | Monthly reports |
| Weekdays 5 PM | `0 17 * * 1-5` | End of day reports |
| Every 6 hours | `0 */6 * * *` | System checks |

## 🛠️ Troubleshooting

### Common Issues:

1. **"Authentication failed"**
   - For Gmail: Use App Password, not regular password
   - For Outlook: Check if account has 2FA enabled
   - Verify email and password are correct

2. **"Connection refused"**
   - Check internet connection
   - Verify SMTP server and port
   - Some networks block SMTP ports

3. **"Email not received"**
   - Check spam/junk folder
   - Verify recipient email address
   - Check email provider limits

### Test Your Setup:
```bash
python setup_email.py
# Choose option 4 to test current configuration
```

## 🔐 Security Notes

- **Never commit passwords to version control**
- **Use App Passwords for Gmail (more secure)**
- **Consider using environment variables for sensitive data**
- **Regularly rotate email passwords**

## 📝 Example Task Creation

### Via Web Interface:
1. Go to `http://localhost:8001/create`
2. Click "Daily Report" email template button
3. Update recipient email in the command
4. Click "Create Task"

### Via API:
```bash
curl -X POST "http://localhost:8001/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "task_name": "Daily Email Report",
    "command": "python email_sender.py daily_report",
    "schedule": "0 9 * * *",
    "description": "Send daily report every morning"
  }'
```

## 🎯 Next Steps

1. **Setup your email configuration**
2. **Create your first email task**
3. **Test with a short schedule (every 2 minutes)**
4. **Customize email content for your needs**
5. **Set up production schedules**

Happy scheduling! 📧✨