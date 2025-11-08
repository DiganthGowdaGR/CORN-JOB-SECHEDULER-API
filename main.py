from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from scheduler import TaskScheduler
from models import TaskCreate, TaskResponse, TaskUpdate
from database import init_db, get_all_tasks
import logging
import os
import subprocess
import json
from email_config import save_email_config, load_email_config, is_email_configured
from email_system import send_system_health_email, send_custom_email

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global scheduler
    init_db()
    scheduler = TaskScheduler()
    scheduler.start()
    logger.info("Task scheduler started")
    yield
    # Shutdown
    if scheduler:
        scheduler.shutdown()
        logger.info("Task scheduler stopped")

app = FastAPI(
    title="Scheduled Task Execution Service",
    description="A cron job manager API for scheduling and executing recurring tasks",
    version="1.0.0",
    lifespan=lifespan
)

# Create templates directory if it doesn't exist
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard page"""
    tasks = get_all_tasks()
    return templates.TemplateResponse("dashboard.html", {"request": request, "tasks": tasks})

@app.get("/api")
async def api_root():
    return {"message": "Scheduled Task Execution Service API is running"}

@app.get("/create", response_class=HTMLResponse)
async def create_task_page(request: Request):
    """Create task page"""
    return templates.TemplateResponse("create_task.html", {"request": request})

@app.post("/create", response_class=HTMLResponse)
async def create_task_form(
    request: Request,
    task_name: str = Form(...),
    command: str = Form(...),
    schedule: str = Form(...),
    description: str = Form("")
):
    """Handle task creation from form"""
    try:
        task_id = scheduler.add_task(
            name=task_name,
            command=command,
            schedule=schedule,
            description=description if description else None
        )
        return RedirectResponse(url="/?success=Task created successfully", status_code=303)
    except Exception as e:
        return templates.TemplateResponse("create_task.html", {
            "request": request,
            "error": str(e),
            "task_name": task_name,
            "command": command,
            "schedule": schedule,
            "description": description
        })

@app.get("/tasks/{task_id}/view", response_class=HTMLResponse)
async def view_task_page(request: Request, task_id: int):
    """View task details and history"""
    task = scheduler.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    history = scheduler.get_task_history(task_id)
    return templates.TemplateResponse("view_task.html", {
        "request": request,
        "task": task,
        "history": history
    })

@app.post("/tasks/{task_id}/delete")
async def delete_task_form(task_id: int):
    """Delete task from form"""
    success = scheduler.remove_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return RedirectResponse(url="/?success=Task deleted successfully", status_code=303)

@app.post("/tasks/{task_id}/toggle")
async def toggle_task_status(task_id: int):
    """Toggle task active/inactive status"""
    task = scheduler.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    new_status = "inactive" if task['status'] == 'active' else "active"
    scheduler.update_task(task_id, {"status": new_status})
    return RedirectResponse(url="/?success=Task status updated", status_code=303)

@app.post("/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate):
    """Create a new scheduled task"""
    try:
        task_id = scheduler.add_task(
            name=task.task_name,
            command=task.command,
            schedule=task.schedule,
            description=task.description
        )
        return TaskResponse(
            id=task_id,
            task_name=task.task_name,
            command=task.command,
            schedule=task.schedule,
            description=task.description,
            status="active"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/tasks")
async def list_tasks():
    """List all scheduled tasks"""
    return get_all_tasks()

@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    """Get a specific task by ID"""
    task = scheduler.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task_update: TaskUpdate):
    """Update an existing task"""
    try:
        updated_task = scheduler.update_task(task_id, task_update.dict(exclude_unset=True))
        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found")
        return updated_task
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    """Delete a scheduled task"""
    success = scheduler.remove_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": f"Task {task_id} deleted successfully"}

@app.get("/tasks/{task_id}/history")
async def get_task_history(task_id: int):
    """Get execution history for a specific task"""
    history = scheduler.get_task_history(task_id)
    if history is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return history

@app.get("/system-monitor", response_class=HTMLResponse)
async def system_monitor_page(request: Request):
    """System monitoring page"""
    return templates.TemplateResponse("system_monitor.html", {"request": request})

@app.get("/api/system-monitor")
async def get_system_monitor_data():
    """Get system monitoring data - returns latest scheduled check data"""
    try:
        # Read the latest report from history (from scheduled checks)
        history_file = 'system_health_history.json'
        
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
            
            if history:
                # Return the most recent report
                latest_report = history[-1]
                return JSONResponse(content=latest_report)
        
        # If no history exists, read the current report file
        if os.path.exists('system_report.json'):
            with open('system_report.json', 'r') as f:
                data = json.load(f)
            return JSONResponse(content=data)
        
        # If no data at all, run the script once
        result = subprocess.run(
            ["python", "system_monitor.py"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if os.path.exists('system_report.json'):
            with open('system_report.json', 'r') as f:
                data = json.load(f)
            return JSONResponse(content=data)
        else:
            raise HTTPException(status_code=500, detail="Failed to generate system report")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/system-monitor/current")
async def get_current_system_monitor_data():
    """Get current real-time system monitoring data (runs check immediately)"""
    try:
        # Run the system monitor script
        result = subprocess.run(
            ["python", "system_monitor.py"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Read the generated JSON file
        if os.path.exists('system_report.json'):
            with open('system_report.json', 'r') as f:
                data = json.load(f)
            return JSONResponse(content=data)
        else:
            raise HTTPException(status_code=500, detail="Failed to generate system report")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/system-monitor/history")
async def get_system_monitor_history():
    """Get system monitoring history"""
    try:
        history_file = 'system_health_history.json'
        
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
            return JSONResponse(content=history)
        
        return JSONResponse(content=[])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/email-manager", response_class=HTMLResponse)
async def email_manager_page(request: Request):
    """Email management page"""
    return templates.TemplateResponse("email_manager.html", {"request": request})

@app.get("/api/email/config")
async def get_email_config():
    """Get email configuration status"""
    config = load_email_config()
    if config:
        return {
            "configured": True,
            "email": config.get('email', ''),
            "smtp_server": config.get('smtp_server', 'smtp.gmail.com'),
            "smtp_port": config.get('smtp_port', 587)
        }
    return {"configured": False}

@app.post("/api/email/config")
async def save_email_config_endpoint(request: Request):
    """Save email configuration"""
    try:
        data = await request.json()
        save_email_config(
            email=data['email'],
            password=data['password'],
            smtp_server=data.get('smtp_server', 'smtp.gmail.com'),
            smtp_port=data.get('smtp_port', 587)
        )
        return {"success": True, "message": "Email configuration saved"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/email/test")
async def test_email_endpoint(request: Request):
    """Send test email"""
    try:
        data = await request.json()
        recipient = data['recipient']
        
        success = send_custom_email(
            recipient,
            "Test Email from Task Scheduler",
            "This is a test email to verify your email configuration is working correctly."
        )
        
        return {"success": success, "message": "Test email sent" if success else "Failed to send test email"}
    except Exception as e:
        return {"success": False, "message": str(e)}

@app.post("/api/email/send-health")
async def send_health_email_endpoint(request: Request):
    """Send system health check email immediately"""
    try:
        data = await request.json()
        recipient = data['recipient']
        
        success = send_system_health_email(recipient)
        
        return {"success": success, "message": "Health check email sent" if success else "Failed to send email"}
    except Exception as e:
        return {"success": False, "message": str(e)}

@app.post("/api/email/send-custom")
async def send_custom_email_endpoint(request: Request):
    """Send custom email immediately"""
    try:
        data = await request.json()
        recipient = data['recipient']
        subject = data['subject']
        message = data['message']
        
        success = send_custom_email(recipient, subject, message)
        
        return {"success": success, "message": "Custom email sent" if success else "Failed to send email"}
    except Exception as e:
        return {"success": False, "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)