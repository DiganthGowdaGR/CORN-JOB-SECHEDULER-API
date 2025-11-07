from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.memory import MemoryJobStore
import subprocess
import logging
from datetime import datetime
from database import create_task, get_task, get_all_tasks, update_task, delete_task, log_task_execution, get_task_history

logger = logging.getLogger(__name__)

class TaskScheduler:
    def __init__(self):
        jobstores = {
            'default': MemoryJobStore()
        }
        
        self.scheduler = BackgroundScheduler(
            jobstores=jobstores,
            timezone='UTC'
        )
        
    def start(self):
        """Start the scheduler"""
        self.scheduler.start()
        logger.info("Scheduler started")
        
        # Load existing tasks from database
        self._load_existing_tasks()
    
    def shutdown(self):
        """Shutdown the scheduler"""
        self.scheduler.shutdown()
        logger.info("Scheduler shutdown")
    
    def _load_existing_tasks(self):
        """Load existing active tasks from database into scheduler"""
        tasks = get_all_tasks()
        for task in tasks:
            if task['status'] == 'active':
                try:
                    self._schedule_task(task)
                    logger.info(f"Loaded task: {task['task_name']}")
                except Exception as e:
                    logger.error(f"Failed to load task {task['id']}: {e}")
    
    def _schedule_task(self, task):
        """Schedule a task with APScheduler"""
        try:
            # Parse cron expression
            cron_parts = task['schedule'].split()
            if len(cron_parts) != 5:
                raise ValueError("Invalid cron expression. Expected 5 parts: minute hour day month day_of_week")
            
            minute, hour, day, month, day_of_week = cron_parts
            
            # Create cron trigger
            trigger = CronTrigger(
                minute=minute,
                hour=hour,
                day=day,
                month=month,
                day_of_week=day_of_week
            )
            
            # Add job to scheduler
            self.scheduler.add_job(
                func=self._execute_task,
                trigger=trigger,
                args=[task['id']],
                id=str(task['id']),
                name=task['task_name'],
                replace_existing=True
            )
            
            # Update next run time in database
            job = self.scheduler.get_job(str(task['id']))
            if job and job.next_run_time:
                update_task(task['id'], {'next_run': job.next_run_time})
                
        except Exception as e:
            logger.error(f"Failed to schedule task {task['id']}: {e}")
            raise
    
    def _execute_task(self, task_id: int):
        """Execute a scheduled task"""
        task = get_task(task_id)
        if not task:
            logger.error(f"Task {task_id} not found")
            return
        
        logger.info(f"Executing task: {task['task_name']}")
        
        try:
            # Execute the command
            result = subprocess.run(
                task['command'],
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                # Success
                log_task_execution(task_id, 'success', result.stdout)
                logger.info(f"Task {task['task_name']} completed successfully")
            else:
                # Failed
                log_task_execution(task_id, 'failed', result.stdout, result.stderr)
                logger.error(f"Task {task['task_name']} failed with return code {result.returncode}")
            
            # Update last run time
            update_task(task_id, {'last_run': datetime.utcnow()})
            
        except subprocess.TimeoutExpired:
            log_task_execution(task_id, 'failed', None, 'Task execution timed out')
            logger.error(f"Task {task['task_name']} timed out")
        except Exception as e:
            log_task_execution(task_id, 'failed', None, str(e))
            logger.error(f"Task {task['task_name']} failed with exception: {e}")
    
    def add_task(self, name: str, command: str, schedule: str, description: str = None) -> int:
        """Add a new scheduled task"""
        # Validate cron expression
        try:
            cron_parts = schedule.split()
            if len(cron_parts) != 5:
                raise ValueError("Invalid cron expression. Expected 5 parts: minute hour day month day_of_week")
        except Exception as e:
            raise ValueError(f"Invalid cron expression: {e}")
        
        # Create task in database
        task_id = create_task(name, command, schedule, description)
        
        # Schedule the task
        task = get_task(task_id)
        self._schedule_task(task)
        
        logger.info(f"Added new task: {name}")
        return task_id
    
    def remove_task(self, task_id: int) -> bool:
        """Remove a scheduled task"""
        # Remove from scheduler
        try:
            self.scheduler.remove_job(str(task_id))
        except:
            pass  # Job might not exist in scheduler
        
        # Remove from database
        success = delete_task(task_id)
        if success:
            logger.info(f"Removed task: {task_id}")
        
        return success
    
    def update_task(self, task_id: int, updates: dict):
        """Update an existing task"""
        # Update in database
        success = update_task(task_id, updates)
        if not success:
            return None
        
        # Get updated task
        task = get_task(task_id)
        
        # If schedule, command or status changed, reschedule the job
        if 'schedule' in updates or 'status' in updates or 'command' in updates:
            try:
                self.scheduler.remove_job(str(task_id))
            except:
                pass
            
            if task['status'] == 'active':
                self._schedule_task(task)
        
        logger.info(f"Updated task: {task_id}")
        return task
    
    def get_task(self, task_id: int):
        """Get task details"""
        return get_task(task_id)
    
    def get_task_history(self, task_id: int):
        """Get task execution history"""
        task = get_task(task_id)
        if not task:
            return None
        return get_task_history(task_id)