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
    return aimen_dir / "projects.db"


def get_connection() -> sqlite3.Connection:
    """Get database connection."""
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database with required tables."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Create project table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS project (
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
                project_id TEXT NOT NULL,
                status TEXT DEFAULT '⚪',
                name TEXT NOT NULL,
                description TEXT,
                acceptance_criteria TEXT,
                acceptance_script TEXT,
                notes TEXT,
                FOREIGN KEY (project_id) REFERENCES project(id)
            )
        """)

        conn.commit()


def generate_id(name: str, prefix: str = "") -> str:
    """Generate 6-character hash ID from name with optional prefix."""
    hash_id = hashlib.md5(name.encode()).hexdigest()[:6].upper()
    return f"{prefix}{hash_id}" if prefix else hash_id


def _make_unique_id(cursor, name: str, prefix: str) -> str:
    """Generate an ID that does not collide with existing records."""
    table = "project" if prefix == "P-" else "task"
    base = generate_id(name, prefix)
    candidate = base
    suffix = 0
    while cursor.execute(f"SELECT 1 FROM {table} WHERE id = ?", (candidate,)).fetchone():
        suffix += 1
        candidate = f"{base}{suffix}"
    return candidate


def create_program(name: str, description: str) -> str:
    """Create a new program."""
    with get_connection() as conn:
        cursor = conn.cursor()
        program_id = _make_unique_id(cursor, name, "P-")
        created_at = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO project (id, name, created_at, description, status)
            VALUES (?, ?, ?, ?, '未开发')
        """, (program_id, name, created_at, description))
        conn.commit()
    return program_id


def get_program(program_id: str) -> Optional[Dict[str, Any]]:
    """Get a program by ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM project WHERE id = ?", (program_id,))
        row = cursor.fetchone()
    return dict(row) if row else None


def get_all_programs() -> List[Dict[str, Any]]:
    """Get all programs."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM project ORDER BY created_at DESC")
        rows = cursor.fetchall()
    return [dict(row) for row in rows]


def update_program(program_id: str, **kwargs):
    """Update program fields."""
    with get_connection() as conn:
        cursor = conn.cursor()
        fields = ", ".join(f"{k} = ?" for k in kwargs.keys())
        values = list(kwargs.values()) + [program_id]
        cursor.execute(f"UPDATE project SET {fields} WHERE id = ?", values)
        conn.commit()


def delete_program(program_id: str):
    """Delete a program and its tasks."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM task WHERE project_id = ?", (program_id,))
        cursor.execute("DELETE FROM project WHERE id = ?", (program_id,))
        conn.commit()


def create_task(program_id: str, name: str, description: str, acceptance_criteria: str) -> str:
    """Create a new task."""
    with get_connection() as conn:
        cursor = conn.cursor()
        task_id = _make_unique_id(cursor, name, "T-")
        cursor.execute("""
            INSERT INTO task (id, project_id, name, description, acceptance_criteria, status)
            VALUES (?, ?, ?, ?, ?, '⚪')
        """, (task_id, program_id, name, description, acceptance_criteria))
        conn.commit()
    return task_id


def get_task(task_id: str) -> Optional[Dict[str, Any]]:
    """Get a task by ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM task WHERE id = ?", (task_id,))
        row = cursor.fetchone()
    return dict(row) if row else None


def get_tasks_by_program(program_id: str) -> List[Dict[str, Any]]:
    """Get all tasks for a program."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM task WHERE project_id = ? ORDER BY id", (program_id,))
        rows = cursor.fetchall()
    return [dict(row) for row in rows]


def update_task(task_id: str, **kwargs):
    """Update task fields."""
    with get_connection() as conn:
        cursor = conn.cursor()
        fields = ", ".join(f"{k} = ?" for k in kwargs.keys())
        values = list(kwargs.values()) + [task_id]
        cursor.execute(f"UPDATE task SET {fields} WHERE id = ?", values)
        conn.commit()


def delete_task(task_id: str):
    """Delete a task."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM task WHERE id = ?", (task_id,))
        conn.commit()
