from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    task_name: str = Field(..., description="Name of the task")
    command: str = Field(..., description="Command to execute")
    schedule: str = Field(..., description="Cron expression (e.g., '0 9 * * 1')")
    description: Optional[str] = Field(None, description="Task description")

class TaskUpdate(BaseModel):
    task_name: Optional[str] = None
    command: Optional[str] = None
    schedule: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    task_name: str
    command: str
    schedule: str
    description: Optional[str]
    status: str
    created_at: Optional[datetime] = None
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None

class TaskExecution(BaseModel):
    id: int
    task_id: int
    execution_time: datetime
    status: str  # 'success', 'failed'
    output: Optional[str] = None
    error: Optional[str] = None