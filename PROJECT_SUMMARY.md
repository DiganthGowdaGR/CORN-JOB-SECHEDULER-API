# Scheduled Task Execution Service - Project Summary

## 📋 Project Overview

A comprehensive backend service for scheduling and executing recurring tasks with a user-friendly web interface, built with FastAPI and APScheduler.

**Team:** Ica-Sonic  
**Course:** UE23CS341A - Software Engineering  
**Institution:** PES University

---

## ✨ Implemented Features

### 1. System Monitoring & Health Dashboard
- Real-time system metrics (CPU, Memory, Disk)
- Automated health status determination (Healthy/Warning/Critical)
- Web dashboard with circular progress indicators
- Color-coded status (Green/Yellow/Red)
- System information display (owner, hostname, OS)
- REST API for system metrics

### 2. Email Notification System
- Email configuration via web interface
- System health check emails (HTML + plain text)
- Custom email messages
- Email scheduling (multiple intervals)
- Email task management (pause/resume/delete)

### 3. Scheduled Health Checks
- Schedule system health checks at custom intervals
- 13 preset intervals (1 min to weekly)
- View scheduled checks with status
- Start/Stop controls for each check
- Execution history tracking

### 4. Task Management
- Create, view, update, delete tasks
- Cron-based scheduling
- Task execution history
- Pause/resume functionality
- Task status tracking

---

## 🏗️ Architecture

### Technology Stack
- **Backend:** FastAPI (Python)
- **Scheduler:** APScheduler
- **Database:** SQLite
- **Frontend:** Bootstrap 5, JavaScript
- **Email:** SMTP (Gmail)
- **Monitoring:** psutil

### Project Structure
```
project/
├── main.py                      # FastAPI application
├── scheduler.py                 # APScheduler integration
├── database.py                  # SQLite operations
├── models.py                    # Pydantic models
├── system_monitor.py            # System monitoring
├── email_system.py              # Email functionality
├── email_config.py              # Email configuration
├── example_tasks.py             # Example task scripts
├── simple_client.py             # CLI client
├── templates/
│   ├── base.html               # Base template
│   ├── dashboard.html          # Main dashboard
│   ├── create_task.html        # Task creation
│   ├── view_task.html          # Task details
│   ├── system_monitor.html     # System monitoring
│   └── email_manager.html      # Email management
├── tasks.db                    # SQLite database
├── system_report.json          # Current system data
├── system_health_history.json  # Health check history
├── email_config.json           # Email credentials
└── requirements.txt            # Dependencies
```

---

## 🎯 Key Features Explained

### System Monitoring
**What it does:**
- Monitors CPU, Memory, and Disk usage
- Determines health status based on thresholds
- Displays data from most recent scheduled check
- Shows timestamp of when check was performed

**How to use:**
1. Go to http://localhost:8001/system-monitor
2. Click "Schedule Health Check"
3. Select interval (e.g., "Every 5 minutes")
4. View results after check executes
5. Click "Refresh" to see latest check data

**Health Thresholds:**
- CPU > 80% = Warning
- Memory > 85% = Warning
- Disk > 90% = Critical

### Email System
**What it does:**
- Sends system health reports via email
- Sends custom email messages
- Schedules emails at custom intervals
- Uses data from recent scheduled checks

**How to use:**
1. Go to http://localhost:8001/email-manager
2. Configure email (Gmail + App Password)
3. Send test email to verify
4. Schedule health check emails
5. Manage scheduled email tasks

**Email Features:**
- HTML emails with progress bars
- Color-coded health status
- Plain text fallback
- Timestamp of check included

### Task Scheduling
**What it does:**
- Creates scheduled tasks using cron expressions
- Executes commands at specified intervals
- Tracks execution history
- Allows pause/resume/delete

**Cron Format:**
```
* * * * *
│ │ │ │ │
│ │ │ │ └─ Day of week (0-7)
│ │ │ └─── Month (1-12)
│ │ └───── Day of month (1-31)
│ └─────── Hour (0-23)
└───────── Minute (0-59)
```

**Common Schedules:**
- `* * * * *` - Every minute
- `*/5 * * * *` - Every 5 minutes
- `0 * * * *` - Every hour
- `0 9 * * *` - Daily at 9 AM
- `0 9 * * 1` - Weekly (Monday 9 AM)

---

## 🚀 Getting Started

### Installation
```bash
# Install dependencies
pip install -r requirements.txt
```

### Start Server
```bash
python main.py
```

### Access Points
- **Dashboard:** http://localhost:8001/
- **System Monitor:** http://localhost:8001/system-monitor
- **Email Manager:** http://localhost:8001/email-manager
- **API Docs:** http://localhost:8001/docs

---

## 📊 API Endpoints

### Task Management
- `GET /tasks` - List all tasks
- `POST /tasks` - Create task
- `GET /tasks/{id}` - Get task details
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task
- `POST /tasks/{id}/toggle` - Pause/Resume task
- `GET /tasks/{id}/history` - Get execution history

### System Monitoring
- `GET /api/system-monitor` - Get latest scheduled check data
- `GET /api/system-monitor/current` - Get real-time data
- `GET /api/system-monitor/history` - Get all history

### Email Management
- `GET /api/email/config` - Get email configuration
- `POST /api/email/config` - Save email configuration
- `POST /api/email/test` - Send test email
- `POST /api/email/send-health` - Send health check email
- `POST /api/email/send-custom` - Send custom email

---

## 🎨 User Interface

### Dashboard
- View all scheduled tasks
- Task statistics (total, active, inactive)
- Quick actions (view, pause, delete)
- Task status indicators

### System Monitor
- Real-time system metrics display
- Circular progress indicators
- Health status with color coding
- Schedule health checks
- View scheduled checks list
- Start/Stop controls

### Email Manager
- Email configuration form
- Test email functionality
- Quick action cards (health check, custom email)
- Schedule email tasks
- View scheduled email tasks
- Start/Stop/Delete controls

---

## 🔧 Configuration

### Email Setup (Gmail)
1. Go to Email Manager
2. Enter Gmail address
3. Generate App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification
   - App Passwords → Generate
4. Enter App Password
5. Click "Save Configuration"
6. Send test email to verify

### Database
- SQLite database: `tasks.db`
- Auto-created on first run
- Tables: `tasks`, `task_executions`

### System Monitoring
- Data file: `system_report.json`
- History file: `system_health_history.json`
- Keeps last 50 checks

---

## 📝 Usage Examples

### Example 1: Schedule Daily Health Check Email
```
1. Go to Email Manager
2. Configure email settings
3. In "System Health Check Email" section:
   - Enter recipient email
   - Select "Daily at 9 AM"
   - Click "Send/Schedule Health Check"
4. Email will be sent daily at 9 AM
```

### Example 2: Monitor System Every 5 Minutes
```
1. Go to System Monitor
2. Click "Schedule Health Check"
3. Select "Every 5 minutes"
4. Enter name: "Production Monitor"
5. Click "Schedule Check"
6. Check runs every 5 minutes
7. Click "Refresh" to see latest data
```

### Example 3: Pause Email Notifications
```
1. Go to Email Manager
2. Scroll to "Scheduled Email Tasks"
3. Find the email task
4. Click Pause button (⏸️)
5. Emails stop sending
6. Click Resume (▶️) to restart
```

---

## 🐛 Troubleshooting

### Issue: Emails keep sending after pause
**Solution:**
- Ensure you clicked the Pause button
- Check task status shows "Inactive"
- Restart server if needed
- Verify in Dashboard that task is paused

### Issue: System Monitor shows old data
**Solution:**
- Scheduled check might be paused
- Check "Scheduled Health Checks" section
- Verify check is "Running" (not "Paused")
- Check "Next Run" time
- Click "Refresh" after check executes

### Issue: Email configuration not saving
**Solution:**
- Check email format is valid
- Verify App Password (not regular password)
- Check SMTP settings (smtp.gmail.com:587)
- Try test email to verify

### Issue: Task not executing
**Solution:**
- Check task status is "Active"
- Verify cron expression is valid
- Check execution history for errors
- Ensure command is correct

---

## 🔒 Security Notes

- Email credentials stored in `email_config.json`
- Use Gmail App Passwords (not regular password)
- SMTP connection uses TLS encryption
- Main branch should be protected in production
- Validate all user inputs
- Sanitize commands before execution

---

## 📦 Dependencies

```
fastapi - Web framework
uvicorn - ASGI server
apscheduler - Task scheduling
pydantic - Data validation
python-multipart - Form handling
jinja2 - Template engine
psutil - System monitoring
```

---

## 🎓 Learning Outcomes

### Technical Skills
- REST API development with FastAPI
- Task scheduling with APScheduler
- Database operations with SQLite
- Email integration with SMTP
- System monitoring with psutil
- Frontend development with Bootstrap
- Asynchronous programming

### Software Engineering Practices
- Clean code architecture
- Modular design
- Error handling
- User experience design
- API documentation
- Testing strategies

---

## 🚀 Future Enhancements

### Potential Features
- User authentication and authorization
- Multi-user support with role-based access
- Dashboard with charts and graphs
- Export reports to PDF
- Webhook notifications
- Slack/Discord integration
- Mobile app
- Docker containerization
- Cloud deployment (AWS/Azure/GCP)

### Testing & Quality
- Unit tests (pytest)
- Integration tests
- System tests
- Code coverage (≥75%)
- CI/CD pipeline (GitHub Actions)
- Linting (pylint ≥7.5)
- Security scanning (bandit)

---

## 📞 Support

For questions or issues:
1. Check this documentation
2. Review API documentation at /docs
3. Check execution logs
4. Test individual components

---

## 👥 Team

**Team Ica-Sonic**
- Project developed for UE23CS341A
- PES University
- Software Engineering Course

---

## 📄 License

Educational project for PES University coursework.

---

**Last Updated:** November 2025  
**Version:** 1.0.0  
**Status:** Active Development

---

Built with ❤️ by Team Ica-Sonic
