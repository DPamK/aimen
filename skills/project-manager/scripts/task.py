#!/usr/bin/env python3
"""Task management script."""

import sqlite3
import json
import sys
import argparse
from pathlib import Path

DB_PATH = Path(__file__).parent / "project.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_task(feature_id, task_id, description, phase=None, file_path=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """INSERT INTO tasks (feature_id, task_id, phase, description, file_path) 
           VALUES (?, ?, ?, ?, ?)""",
        (feature_id, task_id, phase, description, file_path)
    )
    db_task_id = cursor.lastrowid
    
    # Log history
    cursor.execute(
        "INSERT INTO history (entity_type, entity_id, action, new_value) VALUES (?, ?, ?, ?)",
        ("task", db_task_id, "created", f"{task_id}: {description}")
    )
    
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "data": {"id": db_task_id, "task_id": task_id, "description": description},
        "message": f"Task {task_id} created"
    }

def list_tasks(feature_id=None, status=None, phase=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT t.id, t.feature_id, f.name as feature_name, t.task_id, t.phase,
               t.description, t.file_path, t.status, t.created_at
        FROM tasks t
        JOIN features f ON t.feature_id = f.id
        WHERE 1=1
    """
    params = []
    
    if feature_id:
        query += " AND t.feature_id = ?"
        params.append(feature_id)
    if status:
        query += " AND t.status = ?"
        params.append(status)
    if phase:
        query += " AND t.phase = ?"
        params.append(phase)
    
    query += " ORDER BY t.task_id"
    cursor.execute(query, params)
    
    tasks = [
        {
            "id": row[0],
            "feature_id": row[1],
            "feature_name": row[2],
            "task_id": row[3],
            "phase": row[4],
            "description": row[5],
            "file_path": row[6],
            "status": row[7],
            "created_at": row[8]
        }
        for row in cursor.fetchall()
    ]
    
    conn.close()
    
    return {
        "success": True,
        "data": tasks,
        "message": f"Found {len(tasks)} task(s)"
    }

def update_task(task_id, status=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    if not status:
        return {"success": False, "error": "Status is required"}
    
    cursor.execute(
        "UPDATE tasks SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (status, task_id)
    )
    
    # Log history
    cursor.execute(
        "INSERT INTO history (entity_type, entity_id, action, new_value) VALUES (?, ?, ?, ?)",
        ("task", task_id, "status_changed", status)
    )
    
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "message": f"Task {task_id} updated to {status}"
    }

def main():
    parser = argparse.ArgumentParser(description="Task management")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new task")
    create_parser.add_argument("--feature-id", type=int, required=True, help="Feature ID")
    create_parser.add_argument("--task-id", required=True, help="Task ID (e.g., T001)")
    create_parser.add_argument("--description", required=True, help="Task description")
    create_parser.add_argument("--phase", help="Phase (e.g., Setup, Foundation)")
    create_parser.add_argument("--file", help="File path")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--feature-id", type=int, help="Filter by feature ID")
    list_parser.add_argument("--status", help="Filter by status")
    list_parser.add_argument("--phase", help="Filter by phase")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("--id", type=int, required=True, help="Task database ID")
    update_parser.add_argument("--status", help="New status (todo/doing/done)")
    
    args = parser.parse_args()
    
    try:
        if args.command == "create":
            result = create_task(
                args.feature_id, args.task_id, args.description, 
                args.phase, args.file
            )
        elif args.command == "list":
            result = list_tasks(args.feature_id, args.status, args.phase)
        elif args.command == "update":
            result = update_task(args.id, args.status)
        
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))
        sys.exit(1)

if __name__ == "__main__":
    main()
