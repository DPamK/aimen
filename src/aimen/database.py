"""SQLite database management for AIMEN."""

import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any


def get_db_path() -> Path:
    """Get the path to programs.db in .aimen directory."""
    aimen_dir = Path.cwd() / ".aimen"
    if not aimen_dir.exists():
        raise FileNotFoundError(".aimen directory not found. Run 'aimen init' first.")
    return aimen_dir / "programs.db"


def get_connection() -> sqlite3.Connection:
    """Get database connection."""
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database with required tables."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create program table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS program (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT '未开发',
            orchestration TEXT,
            notes TEXT
        )
    """)

    # Create task table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task (
            id TEXT PRIMARY KEY,
            program_id TEXT NOT NULL,
            status TEXT DEFAULT '⚪',
            name TEXT NOT NULL,
            description TEXT,
            acceptance_criteria TEXT,
            acceptance_script TEXT,
            notes TEXT,
            FOREIGN KEY (program_id) REFERENCES program(id)
        )
    """)

    conn.commit()
    conn.close()


def generate_id(name: str, prefix: str = "") -> str:
    """Generate 6-character hash ID from name with optional prefix."""
    hash_id = hashlib.md5(name.encode()).hexdigest()[:6].upper()
    return f"{prefix}{hash_id}" if prefix else hash_id


def create_program(name: str, description: str) -> str:
    """Create a new program."""
    conn = get_connection()
    cursor = conn.cursor()

    program_id = generate_id(name, "P-")
    created_at = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO program (id, name, created_at, description, status)
        VALUES (?, ?, ?, ?, '未开发')
    """, (program_id, name, created_at, description))

    conn.commit()
    conn.close()
    return program_id


def get_program(program_id: str) -> Optional[Dict[str, Any]]:
    """Get a program by ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM program WHERE id = ?", (program_id,))
    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


def get_all_programs() -> List[Dict[str, Any]]:
    """Get all programs."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM program ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def update_program(program_id: str, **kwargs):
    """Update program fields."""
    conn = get_connection()
    cursor = conn.cursor()

    fields = ", ".join(f"{k} = ?" for k in kwargs.keys())
    values = list(kwargs.values()) + [program_id]

    cursor.execute(f"UPDATE program SET {fields} WHERE id = ?", values)
    conn.commit()
    conn.close()


def delete_program(program_id: str):
    """Delete a program and its tasks."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM task WHERE program_id = ?", (program_id,))
    cursor.execute("DELETE FROM program WHERE id = ?", (program_id,))
    conn.commit()
    conn.close()


def create_task(program_id: str, name: str, description: str, acceptance_criteria: str) -> str:
    """Create a new task."""
    conn = get_connection()
    cursor = conn.cursor()

    task_id = generate_id(name, "T-")

    cursor.execute("""
        INSERT INTO task (id, program_id, name, description, acceptance_criteria, status)
        VALUES (?, ?, ?, ?, ?, '⚪')
    """, (task_id, program_id, name, description, acceptance_criteria))

    conn.commit()
    conn.close()
    return task_id


def get_task(task_id: str) -> Optional[Dict[str, Any]]:
    """Get a task by ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM task WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


def get_tasks_by_program(program_id: str) -> List[Dict[str, Any]]:
    """Get all tasks for a program."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM task WHERE program_id = ? ORDER BY id", (program_id,))
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def update_task(task_id: str, **kwargs):
    """Update task fields."""
    conn = get_connection()
    cursor = conn.cursor()

    fields = ", ".join(f"{k} = ?" for k in kwargs.keys())
    values = list(kwargs.values()) + [task_id]

    cursor.execute(f"UPDATE task SET {fields} WHERE id = ?", values)
    conn.commit()
    conn.close()


def delete_task(task_id: str):
    """Delete a task."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM task WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
