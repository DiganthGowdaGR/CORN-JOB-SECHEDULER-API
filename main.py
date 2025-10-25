from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from scheduler import TaskScheduler
from models import TaskCreate, TaskResponse, TaskUpdate
from database import init_db, get_all_tasks
import logging
import os

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)