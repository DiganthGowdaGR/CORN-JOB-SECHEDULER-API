import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import json

DATABASE_FILE = "tasks.db"

def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create tasks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            command TEXT NOT NULL,
            schedule TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_run TIMESTAMP,
            next_run TIMESTAMP
        )
    ''')
    
    # Create task_executions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task_executions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            execution_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL,
            output TEXT,
            error TEXT,
            FOREIGN KEY (task_id) REFERENCES tasks (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def create_task(task_name: str, command: str, schedule: str, description: str = None) -> int:
    """Create a new task in the database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO tasks (task_name, command, schedule, description)
        VALUES (?, ?, ?, ?)
    ''', (task_name, command, schedule, description))
    
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return task_id

def get_task(task_id: int) -> Optional[Dict]:
    """Get a task by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None

def get_all_tasks() -> List[Dict]:
    """Get all tasks"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def update_task(task_id: int, updates: Dict) -> bool:
    """Update a task"""
    if not updates:
        return False
        
    conn = get_connection()
    cursor = conn.cursor()
    
    # Build dynamic update query
    set_clauses = []
    values = []
    
    for key, value in updates.items():
        if key in ['task_name', 'command', 'schedule', 'description', 'status', 'last_run', 'next_run']:
            set_clauses.append(f"{key} = ?")
            values.append(value)
    
    if not set_clauses:
        conn.close()
        return False
    
    query = f"UPDATE tasks SET {', '.join(set_clauses)} WHERE id = ?"
    values.append(task_id)
    
    cursor.execute(query, values)
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    return success

def delete_task(task_id: int) -> bool:
    """Delete a task"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    return success

def log_task_execution(task_id: int, status: str, output: str = None, error: str = None):
    """Log task execution result"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO task_executions (task_id, status, output, error)
        VALUES (?, ?, ?, ?)
    ''', (task_id, status, output, error))
    
    conn.commit()
    conn.close()

def get_task_history(task_id: int) -> List[Dict]:
    """Get execution history for a task"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM task_executions 
        WHERE task_id = ? 
        ORDER BY execution_time DESC 
        LIMIT 50
    ''', (task_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]