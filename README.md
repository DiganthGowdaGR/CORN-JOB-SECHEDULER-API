# 📅 Scheduled Task Execution Service (Cron Job Manager)

A comprehensive backend service for scheduling and executing recurring tasks with a user-friendly web interface, built with FastAPI and APScheduler.

## Architecture
![Architecture](https://github.com/DiganthGowdaGR/CRON-JOB-SECHEDULER-API/blob/70cf4d2c26df573ba14da2324dbf22c24a89d911/Screenshot%202025-11-07%20084750.png)

## ✨ Features

- 🌐 **Web Interface** - User-friendly dashboard for task management
- 📡 **REST API** - Complete API for programmatic access
- ⏰ **Cron-based Scheduling** - Standard cron expressions for flexible timing
- 💾 **Persistent Storage** - SQLite database (no setup required)
- 📊 **Execution History** - Track success/failure with detailed logs
- 📧 **Email Integration** - Send automated emails and reports
- 🔄 **Real-time Scheduling** - Automatic task loading and execution
- 📈 **Statistics Dashboard** - Visual task performance metrics

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Start the Service

```bash
# Run the server
python main.py
```

The service will be available at:
- **Web Interface:** `http://localhost:8001/`
- **API Documentation:** `http://localhost:8001/docs`

### 3. Create Your First Task

**Option A: Web Interface (Recommended)**
1. Open `http://localhost:8001/` in your browser
2. Click "Create New Task"
3. Fill in the form and click "Create Task"

**Option B: Command Line**
```bash
python simple_client.py
```

**Option C: API**
```bash
curl -X POST "http://localhost:8001/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "task_name": "Test Task",
    "command": "echo Hello World",
    "schedule": "*/2 * * * *",
    "description": "Test task every 2 minutes"
  }'
```

## 🌐 Web Interface Guide

### Dashboard (`http://localhost:8001/`)
- 📊 View all scheduled tasks
- 📈 Task statistics and performance metrics
- ⏸️ Pause/Resume tasks with one click
- 🗑️ Delete tasks with confirmation
- 👁️ View detailed task information

### Create Task (`http://localhost:8001/create`)
- 📝 User-friendly form with validation
- 🔘 Quick schedule buttons (Every 5 min, Hourly, Daily, etc.)
- 📧 Email task templates
- 💡 Built-in examples and help
- ⚡ Real-time form validation

### Task Details (`/tasks/{id}/view`)
- 📋 Complete task information
- 📊 Execution history with success/failure status
- 📈 Performance statistics and success rates
- 🔧 Task management actions

## 📧 Email Functionality

### Setup Email (One-time)
```bash
python setup_email.py
```

Choose your email provider:
1. **Gmail** (Recommended - requires App Password)
2. **Outlook/Hotmail**
3. **Custom SMTP**

### Email Task Examples

**Daily Report Email:**
```bash
# Command: python email_sender.py daily_report
# Schedule: 0 9 * * * (Daily at 9 AM)
```

**Custom Email:**
```bash
# Command: python email_sender.py send_custom recipient@example.com "Subject" "Message"
# Example: python email_sender.py send_custom admin@company.com "Backup Complete" "Daily backup finished"
```

**Alert Email:**
```bash
# Command: python email_sender.py alert "System Check" "All systems operational"
# Schedule: 0 */6 * * * (Every 6 hours)
```

### Web Interface Email Templates
Use the blue email template buttons in the web interface:
- **Daily Report** - Automated system reports
- **Weekly Summary** - Weekly statistics
- **Custom Email** - Send custom messages
- **Alert Email** - System alerts and notifications

## 📅 Cron Expression Guide

Format: `minute hour day month day_of_week`

### Common Schedules:
| Expression | Description | Use Case |
|------------|-------------|----------|
| `*/5 * * * *` | Every 5 minutes | Testing, monitoring |
| `0 * * * *` | Every hour | Hourly reports |
| `0 9 * * *` | Daily at 9 AM | Daily reports |
| `0 9 * * 1` | Every Monday 9 AM | Weekly reports |
| `0 0 1 * *` | First day of month | Monthly tasks |
| `0 17 * * 1-5` | Weekdays at 5 PM | End-of-day tasks |
| `*/15 9-17 * * 1-5` | Every 15 min, business hours | Frequent monitoring |

### Special Characters:
- `*` = Any value
- `*/n` = Every n units
- `n-m` = Range from n to m
- `n,m` = Specific values

## 🛠️ Project Structure

```
📁 Scheduled Task Execution Service/
├── 🌐 Web Interface
│   ├── main.py                    # FastAPI app with web routes
│   ├── templates/                 # HTML templates
│   │   ├── base.html             # Base template
│   │   ├── dashboard.html        # Main dashboard
│   │   ├── create_task.html      # Task creation form
│   │   └── view_task.html        # Task details view
│   └── static/                   # Static files (auto-created)
│
├── 🔧 Core System
│   ├── scheduler.py              # APScheduler integration
│   ├── database.py               # SQLite operations
│   ├── models.py                 # Pydantic models
│   └── tasks.db                  # SQLite database (auto-created)
│
├── 📧 Email System
│   ├── email_sender.py           # Email functionality
│   ├── setup_email.py            # Email configuration
│   └── email_tasks_examples.py   # Email task examples
│
├── 🎯 Examples & Tools
│   ├── example_tasks.py          # Sample task scripts
│   ├── simple_client.py          # CLI interface
│   ├── demo_web_interface.py     # Web demo
│   ├── create_task_example.py    # API examples
│   └── command_examples.py       # Command examples
│
├── 📚 Documentation
│   ├── README.md                 # This file
│   ├── EMAIL_SETUP_GUIDE.md      # Email setup guide
│   └── cron_examples.md          # Cron expression examples
│
└── 📦 Configuration
    └── requirements.txt          # Python dependencies
```

## 🎯 Usage Examples

### 1. System Administration Tasks

**Daily Backup:**
```bash
# Task Name: Daily Database Backup
# Command: python backup_script.py
# Schedule: 0 2 * * *
# Description: Backup database daily at 2 AM
```

**Log Cleanup:**
```bash
# Task Name: Weekly Log Cleanup
# Command: python cleanup_logs.py
# Schedule: 0 0 * * 0
# Description: Clean old logs every Sunday
```

### 2. Business Tasks

**Weekly Reports:**
```bash
# Task Name: Weekly Sales Report
# Command: python email_sender.py send_custom manager@company.com "Weekly Sales Report" "Please find attached this week's sales summary"
# Schedule: 0 9 * * 1
# Description: Send weekly sales report every Monday
```

**Daily Health Check:**
```bash
# Task Name: System Health Check
# Command: python email_sender.py daily_report
# Schedule: 0 8 * * 1-5
# Description: Send daily system status on weekdays
```

### 3. Development Tasks

**Automated Testing:**
```bash
# Task Name: Nightly Tests
# Command: python run_tests.py
# Schedule: 0 1 * * *
# Description: Run automated tests every night
```

**Code Deployment:**
```bash
# Task Name: Deploy to Staging
# Command: python deploy_staging.py
# Schedule: 0 18 * * 5
# Description: Deploy to staging every Friday at 6 PM
```

## 🔧 API Reference

### Core Endpoints

**Create Task:**
```http
POST /tasks
Content-Type: application/json

{
  "task_name": "My Task",
  "command": "python script.py",
  "schedule": "0 9 * * *",
  "description": "Optional description"
}
```

**List Tasks:**
```http
GET /tasks
```

**Get Task Details:**
```http
GET /tasks/{task_id}
```

**Update Task:**
```http
PUT /tasks/{task_id}
Content-Type: application/json

{
  "task_name": "Updated Name",
  "status": "inactive"
}
```

**Delete Task:**
```http
DELETE /tasks/{task_id}
```

**Get Execution History:**
```http
GET /tasks/{task_id}/history
```

### Web Interface Endpoints

- `GET /` - Dashboard
- `GET /create` - Create task form
- `POST /create` - Handle task creation
- `GET /tasks/{id}/view` - Task details page
- `POST /tasks/{id}/delete` - Delete task
- `POST /tasks/{id}/toggle` - Toggle task status

## 🧪 Testing & Development

### Run Tests
```bash
# Test API functionality
python test_api.py

# Test email functionality (after setup)
python setup_email.py  # Choose option 4

# Create example tasks
python create_task_example.py
```

### Development Mode
```bash
# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Demo Mode
```bash
# Open web interface demo
python demo_web_interface.py
```

## 🛡️ Security & Best Practices

### Email Security
- Use App Passwords for Gmail (more secure than regular passwords)
- Never commit email credentials to version control
- Consider using environment variables for production
- Regularly rotate email passwords

### Task Security
- Validate all user inputs
- Sanitize commands before execution
- Use least privilege principles
- Monitor task execution logs

### Database Security
- SQLite file is created with appropriate permissions
- Regular backups recommended for production
- Consider encryption for sensitive data

## 🚨 Troubleshooting

### Common Issues

**1. Server Won't Start**
```bash
# Check if port is in use
netstat -an | findstr :8001

# Try different port
python main.py  # Edit main.py to change port
```

**2. Tasks Not Executing**
- Check task status (should be "active")
- Verify cron expression syntax
- Check execution history for errors
- Ensure commands are valid

**3. Email Issues**
```bash
# Test email configuration
python setup_email.py  # Choose option 4

# Common fixes:
# - Use App Password for Gmail
# - Check spam folder
# - Verify SMTP settings
```

**4. Web Interface Issues**
- Clear browser cache
- Check browser console for errors
- Ensure JavaScript is enabled
- Try different browser

### Getting Help

1. **Check the logs** - Server logs show detailed error information
2. **Test components individually** - Use test scripts to isolate issues
3. **Verify configuration** - Double-check email and database settings
4. **Check permissions** - Ensure files have proper read/write permissions

## 🎓 Course Context

This project is developed for **UE23CS341A** at PES University, demonstrating:

### Technical Skills
- **Backend Development** - FastAPI, REST APIs
- **Database Management** - SQLite, data persistence
- **Task Scheduling** - APScheduler, cron expressions
- **Web Development** - HTML templates, responsive design
- **Email Integration** - SMTP, automated notifications

### Software Engineering Practices
- **Clean Code** - Modular design, clear documentation
- **User Experience** - Intuitive web interface
- **Error Handling** - Comprehensive error management
- **Testing** - Automated testing scripts
- **Security** - Input validation, secure practices

### Real-world Applications
- **System Administration** - Automated backups, monitoring
- **Business Automation** - Reports, notifications
- **DevOps** - Deployment, testing automation
- **Data Management** - Scheduled data processing

## 🚀 Getting Started Checklist

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Start server: `python main.py`
- [ ] Open web interface: `http://localhost:8001/`
- [ ] Create first task using web interface
- [ ] Set up email (optional): `python setup_email.py`
- [ ] Create email task using templates
- [ ] Test with short schedule (every 2 minutes)
- [ ] Check execution history
- [ ] Explore API documentation: `http://localhost:8001/docs`

## 📞 Support

For questions or issues:
1. Check this README and documentation files
2. Review the troubleshooting section
3. Test individual components
4. Check server logs for detailed error information

---

**Happy Scheduling! 🎉**

*Built with ❤️ Team Ica-Sonic*
