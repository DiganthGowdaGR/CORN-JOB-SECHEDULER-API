# Jira Setup - EPICs and User Stories

## Project: Scheduled Task Execution Service (Cron Job Manager)

---

## EPIC 1: System Monitoring & Health Dashboard

**Epic Description:**
As a system administrator, I need a comprehensive system monitoring solution that provides real-time insights into system health, resource utilization, and performance metrics, so that I can proactively manage system resources and prevent issues.

**Business Value:**
- Proactive system management
- Early detection of resource issues
- Better capacity planning
- Reduced downtime

**Acceptance Criteria:**
- Real-time system metrics displayed
- Historical data tracking
- Visual dashboards with charts
- Automated health status determination

---

### User Stories for EPIC 1:

#### ✅ US-001: View Real-Time System Metrics
**Status:** DONE (Completed)

**Story:**
As a system administrator,
I want to view real-time CPU, memory, and disk usage metrics,
So that I can monitor current system performance.

**Acceptance Criteria:**
- ✅ Display CPU usage percentage
- ✅ Display CPU core count and frequency
- ✅ Display total, used, and available memory
- ✅ Display memory usage percentage
- ✅ Display total, used, and free disk space
- ✅ Display disk usage percentage
- ✅ Metrics update automatically every 5 seconds

**Story Points:** 5
**Priority:** High
**Assignee:** [Your Name]

**Implementation Details:**
- File: `system_monitor.py`
- Collects system data using psutil library
- Generates JSON report with all metrics
- Includes timestamp for each check

**Test Cases:**
- Unit test: Verify psutil data collection
- Integration test: Verify JSON report generation
- System test: Verify metrics accuracy

---

#### ✅ US-002: System Health Status Determination
**Status:** DONE (Completed)

**Story:**
As a system administrator,
I want the system to automatically determine health status based on resource thresholds,
So that I can quickly identify if the system needs attention.

**Acceptance Criteria:**
- ✅ Health status shows "Healthy" when all resources normal
- ✅ Health status shows "Warning" when CPU > 80% OR Memory > 85%
- ✅ Health status shows "Critical" when Disk > 90%
- ✅ Display list of issues detected
- ✅ Color-coded status indicators (Green/Yellow/Red)

**Story Points:** 3
**Priority:** High
**Assignee:** [Your Name]

**Implementation Details:**
- File: `system_monitor.py` (get_system_info function)
- Logic for health determination implemented
- Issues list generated based on thresholds

**Test Cases:**
- Unit test: Test health logic with mock data
- Integration test: Verify correct status for different scenarios

---

#### ✅ US-003: System Monitoring Web Dashboard
**Status:** DONE (Completed)

**Story:**
As a system administrator,
I want a web-based dashboard to visualize system metrics,
So that I can easily monitor system health from any browser.

**Acceptance Criteria:**
- ✅ Web page accessible at /system-monitor
- ✅ Display system owner and hostname
- ✅ Show circular progress indicators for CPU, Memory, Disk
- ✅ Show horizontal progress bars for overview
- ✅ Color-coded based on usage levels
- ✅ Auto-refresh every 5 seconds
- ✅ Manual refresh button available
- ✅ Responsive design (works on mobile)

**Story Points:** 8
**Priority:** High
**Assignee:** [Your Name]

**Implementation Details:**
- File: `templates/system_monitor.html`
- Uses Bootstrap 5 for responsive design
- SVG circular progress indicators
- JavaScript for auto-refresh
- API endpoint: `/api/system-monitor`

**Test Cases:**
- Integration test: API endpoint returns correct data
- System test: Dashboard loads and displays data
- UI test: Auto-refresh works correctly

---

#### ✅ US-004: System Information Display
**Status:** DONE (Completed)

**Story:**
As a system administrator,
I want to see detailed system information including owner, hostname, and OS,
So that I can identify which system I'm monitoring.

**Acceptance Criteria:**
- ✅ Display system owner (username)
- ✅ Display hostname
- ✅ Display operating system and version
- ✅ Display timestamp of last check
- ✅ Information prominently displayed at top of dashboard

**Story Points:** 2
**Priority:** Medium
**Assignee:** [Your Name]

**Implementation Details:**
- File: `system_monitor.py`
- Uses platform and os modules
- Data included in JSON report

**Test Cases:**
- Unit test: Verify system info collection
- Integration test: Verify data in API response

---

#### ✅ US-005: System Monitor API Endpoint
**Status:** DONE (Completed)

**Story:**
As a developer,
I want a REST API endpoint to retrieve system monitoring data,
So that I can integrate system metrics into other applications.

**Acceptance Criteria:**
- ✅ GET endpoint at /api/system-monitor
- ✅ Returns JSON with all system metrics
- ✅ Executes system_monitor.py script
- ✅ Returns 200 status on success
- ✅ Returns error status on failure
- ✅ Response time < 2 seconds

**Story Points:** 3
**Priority:** Medium
**Assignee:** [Your Name]

**Implementation Details:**
- File: `main.py` (get_system_monitor_data function)
- Runs system_monitor.py subprocess
- Reads generated JSON file
- Returns as API response

**Test Cases:**
- Integration test: API returns valid JSON
- Integration test: API handles errors gracefully
- Performance test: Response time < 2s

---

## EPIC 1 Summary:

**Total User Stories:** 5
**Completed:** 5 ✅
**Story Points:** 21
**Sprint:** Sprint 1
**Status:** COMPLETED

**Features Delivered:**
- Real-time system monitoring
- Health status determination
- Web dashboard with visualizations
- Auto-refresh functionality
- REST API for system metrics

**Files Created:**
- `system_monitor.py` - Core monitoring logic
- `templates/system_monitor.html` - Web UI
- `system_report.json` - Generated data file
- API endpoints in `main.py`

---

## EPIC 2: Email Notification & Scheduling System

**Epic Description:**
As a system administrator, I need an automated email notification system that can send scheduled health reports and custom alerts, so that I can stay informed about system status without manually checking the dashboard.

**Business Value:**
- Proactive notifications
- Automated reporting
- Reduced manual monitoring effort
- Timely alerts for issues

**Acceptance Criteria:**
- Email configuration via web UI
- Scheduled email sending
- System health reports via email
- Custom email messages
- Email history tracking

---

### User Stories for EPIC 2:

#### ✅ US-006: Email Configuration Management
**Status:** DONE (Completed)

**Story:**
As a system administrator,
I want to configure email settings through a web interface,
So that I can set up email notifications without editing config files.

**Acceptance Criteria:**
- ✅ Web form to enter email address
- ✅ Web form to enter app password
- ✅ SMTP server configuration (default: Gmail)
- ✅ SMTP port configuration (default: 587)
- ✅ Save configuration securely
- ✅ Load existing configuration
- ✅ Test email functionality
- ✅ Configuration status indicator

**Story Points:** 5
**Priority:** High
**Assignee:** [Your Name]

**Implementation Details:**
- File: `email_config.py` - Configuration manager
- File: `templates/email_manager.html` - Web UI
- Configuration saved in `email_config.json`
- API endpoints in `main.py`

**Test Cases:**
- Unit test: Save and load configuration
- Integration test: API endpoints work correctly
- System test: Configuration persists across restarts

---

#### ✅ US-007: Send System Health Check Email
**Status:** DONE (Completed)

**Story:**
As a system administrator,
I want to receive system health reports via email,
So that I can monitor system status remotely.

**Acceptance Criteria:**
- ✅ Email includes current system metrics
- ✅ Email includes CPU, Memory, Disk usage
- ✅ Email includes health status
- ✅ Email includes timestamp of check
- ✅ Email has both plain text and HTML versions
- ✅ HTML email has color-coded status
- ✅ HTML email has progress bars
- ✅ Email subject includes health status

**Story Points:** 8
**Priority:** High
**Assignee:** [Your Name]

**Implementation Details:**
- File: `email_system.py` (send_system_health_email function)
- Runs system_monitor.py to get current data
- Generates HTML email with styling
- Uses SMTP to send email

**Test Cases:**
- Unit test: Email content generation
- Integration test: Email sending with mock SMTP
- System test: Actual email delivery

---

#### ✅ US-008: Send Custom Email Messages
**Status:** DONE (Completed)

**Story:**
As a system administrator,
I want to send custom email messages through the system,
So that I can use it for various notification purposes.

**Acceptance Criteria:**
- ✅ Web form to enter recipient email
- ✅ Web form to enter subject
- ✅ Web form to enter message body
- ✅ Send email immediately option
- ✅ Email includes timestamp
- ✅ Both plain text and HTML versions
- ✅ Confirmation of successful send

**Story Points:** 5
**Priority:** Medium
**Assignee:** [Your Name]

**Implementation Details:**
- File: `email_system.py` (send_custom_email function)
- File: `templates/email_manager.html` - Form UI
- API endpoint: `/api/email/send-custom`

**Test Cases:**
- Integration test: Custom email API
- System test: Email delivery with custom content

---

#### ✅ US-009: Schedule Email Tasks
**Status:** DONE (Completed)

**Story:**
As a system administrator,
I want to schedule emails to be sent at specific intervals,
So that I receive regular updates without manual intervention.

**Acceptance Criteria:**
- ✅ Schedule options: 1 min, 5 min, 10 min, 30 min, 1 hr, 3 hrs, 6 hrs
- ✅ Schedule options: Daily, Weekly
- ✅ Create scheduled task for health check emails
- ✅ Create scheduled task for custom emails
- ✅ View all scheduled email tasks
- ✅ Tasks show next run time
- ✅ Tasks can be paused/resumed
- ✅ Tasks can be deleted

**Story Points:** 8
**Priority:** High
**Assignee:** [Your Name]

**Implementation Details:**
- Uses existing task scheduler system
- Creates tasks with email commands
- Integration with Jira task system
- UI in `templates/email_manager.html`

**Test Cases:**
- Integration test: Task creation via API
- System test: Scheduled email executes correctly
- System test: Task shows in email manager

---

#### ✅ US-010: Email Manager Dashboard
**Status:** DONE (Completed)

**Story:**
As a system administrator,
I want a centralized dashboard to manage all email-related features,
So that I can easily configure and monitor email notifications.

**Acceptance Criteria:**
- ✅ Web page accessible at /email-manager
- ✅ Email configuration section
- ✅ Quick action cards for health check and custom emails
- ✅ List of scheduled email tasks
- ✅ Navigation link in main menu
- ✅ Responsive design
- ✅ Real-time task list updates

**Story Points:** 5
**Priority:** High
**Assignee:** [Your Name]

**Implementation Details:**
- File: `templates/email_manager.html`
- Bootstrap 5 cards and forms
- JavaScript for dynamic updates
- API integration

**Test Cases:**
- System test: Dashboard loads correctly
- UI test: All forms work
- Integration test: Task list displays correctly

---

#### ✅ US-011: Email Configuration API
**Status:** DONE (Completed)

**Story:**
As a developer,
I want REST API endpoints for email configuration,
So that I can integrate email features programmatically.

**Acceptance Criteria:**
- ✅ GET /api/email/config - Get configuration status
- ✅ POST /api/email/config - Save configuration
- ✅ POST /api/email/test - Send test email
- ✅ POST /api/email/send-health - Send health check immediately
- ✅ POST /api/email/send-custom - Send custom email immediately
- ✅ All endpoints return JSON responses
- ✅ Proper error handling

**Story Points:** 5
**Priority:** Medium
**Assignee:** [Your Name]

**Implementation Details:**
- File: `main.py` - API endpoints
- Uses email_config.py and email_system.py
- JSON request/response format

**Test Cases:**
- Integration test: All API endpoints
- Integration test: Error handling
- Integration test: Authentication (if added)

---

## EPIC 2 Summary:

**Total User Stories:** 6
**Completed:** 6 ✅
**Story Points:** 36
**Sprint:** Sprint 1 & Sprint 2
**Status:** COMPLETED

**Features Delivered:**
- Email configuration web UI
- System health check emails
- Custom email messages
- Email scheduling (multiple intervals)
- Email manager dashboard
- Complete REST API

**Files Created:**
- `email_config.py` - Configuration manager
- `email_system.py` - Email sending logic
- `templates/email_manager.html` - Web UI
- `email_config.json` - Stored configuration
- API endpoints in `main.py`

---

## Additional User Stories (Testing & Infrastructure):

#### 🔄 US-012: Unit Tests for System Monitor
**Status:** TO DO (Sprint 2)

**Story:**
As a developer,
I want comprehensive unit tests for the system monitoring module,
So that I can ensure reliability and catch bugs early.

**Acceptance Criteria:**
- [ ] Test get_system_info() function
- [ ] Test health status logic
- [ ] Test with mock psutil data
- [ ] Test edge cases (0% usage, 100% usage)
- [ ] Test error handling
- [ ] Minimum 80% code coverage for system_monitor.py

**Story Points:** 5
**Priority:** High
**Sprint:** Sprint 2

---

#### 🔄 US-013: Integration Tests for Email System
**Status:** TO DO (Sprint 2)

**Story:**
As a developer,
I want integration tests for the email system,
So that I can verify email sending works correctly.

**Acceptance Criteria:**
- [ ] Test email configuration save/load
- [ ] Test email sending with mock SMTP
- [ ] Test health check email generation
- [ ] Test custom email generation
- [ ] Test API endpoints
- [ ] Minimum 75% code coverage for email modules

**Story Points:** 5
**Priority:** High
**Sprint:** Sprint 2

---

#### 🔄 US-014: System Tests for Complete Workflows
**Status:** TO DO (Sprint 2)

**Story:**
As a QA engineer,
I want end-to-end system tests,
So that I can verify complete user workflows work correctly.

**Acceptance Criteria:**
- [ ] Test: Configure email → Send test email → Verify delivery
- [ ] Test: Schedule health check → Wait for execution → Verify email sent
- [ ] Test: View system monitor → Verify data accuracy
- [ ] Test: Create task → Execute → View history
- [ ] All critical user journeys covered

**Story Points:** 8
**Priority:** High
**Sprint:** Sprint 2

---

#### 🔄 US-015: CI/CD Pipeline Setup
**Status:** TO DO (Sprint 2)

**Story:**
As a DevOps engineer,
I want a complete CI/CD pipeline,
So that code quality is automatically verified.

**Acceptance Criteria:**
- [ ] Build stage: Install dependencies
- [ ] Test stage: Run all tests
- [ ] Coverage stage: Generate coverage report (≥75%)
- [ ] Lint stage: Run pylint (score ≥7.5)
- [ ] Security stage: Run bandit security scan
- [ ] Deploy stage: Create deployment artifact
- [ ] Pipeline runs on every push and PR
- [ ] README documents pipeline

**Story Points:** 13
**Priority:** Critical
**Sprint:** Sprint 2

---

## Project Summary:

### Completed Work:
- **EPIC 1:** System Monitoring ✅ (5 stories, 21 points)
- **EPIC 2:** Email System ✅ (6 stories, 36 points)
- **Total Completed:** 11 stories, 57 points

### Remaining Work:
- **US-012:** Unit Tests (5 points)
- **US-013:** Integration Tests (5 points)
- **US-014:** System Tests (8 points)
- **US-015:** CI/CD Pipeline (13 points)
- **Total Remaining:** 4 stories, 31 points

### Sprint Allocation:
- **Sprint 1 (Weeks 1-2):** US-001 to US-011 ✅ COMPLETED
- **Sprint 2 (Weeks 3-4):** US-012 to US-015 🔄 IN PROGRESS

### Overall Progress:
- **Total Stories:** 15
- **Completed:** 11 (73%)
- **Remaining:** 4 (27%)
- **Total Story Points:** 88
- **Completed Points:** 57 (65%)

---

## Next Steps:

1. **Create Jira Workspace** and add these EPICs and User Stories
2. **Mark US-001 to US-011 as DONE** (already implemented)
3. **Start Sprint 2** with US-012 to US-015
4. **Write Tests** (US-012, US-013, US-014)
5. **Setup CI/CD** (US-015)
6. **Conduct Sprint Retrospectives** for both sprints
7. **Prepare Final Demo**

---

## Files Reference:

### Completed Features:
```
project/
├── system_monitor.py          # US-001, US-002, US-004, US-005
├── email_config.py            # US-006, US-011
├── email_system.py            # US-007, US-008, US-011
├── main.py                    # US-005, US-010, US-011
├── templates/
│   ├── system_monitor.html    # US-003
│   ├── email_manager.html     # US-009, US-010
│   └── base.html              # Navigation
├── system_report.json         # Generated data
└── email_config.json          # Saved configuration
```

### To Be Created (Sprint 2):
```
project/
├── tests/
│   ├── unit/
│   │   ├── test_system_monitor.py    # US-012
│   │   ├── test_email_config.py      # US-012
│   │   └── test_email_system.py      # US-012
│   ├── integration/
│   │   ├── test_api_endpoints.py     # US-013
│   │   └── test_email_sending.py     # US-013
│   └── system/
│       └── test_workflows.py         # US-014
├── .github/
│   └── workflows/
│       └── ci-cd.yml                 # US-015
└── requirements.txt                  # Updated with test dependencies
```
