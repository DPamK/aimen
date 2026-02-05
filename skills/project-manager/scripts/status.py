#!/usr/bin/env python3
"""Status query script."""

import sqlite3
import json
import sys
import argparse
from pathlib import Path

DB_PATH = Path(__file__).parent / "project.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_current_work():
    """Get all in-progress items."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get active products
    cursor.execute(
        "SELECT id, name, status FROM products WHERE status = 'active'"
    )
    products = [{"id": row[0], "name": row[1], "status": row[2]} for row in cursor.fetchall()]
    
    # Get in-progress features
    cursor.execute("""
        SELECT f.id, f.product_id, p.name as product_name, f.name, f.branch,
               f.status, f.workflow_stage
        FROM features f
        JOIN products p ON f.product_id = p.id
        WHERE f.status IN ('planning', 'implementing', 'testing')
        ORDER BY f.updated_at DESC
    """)
    features = [
        {
            "id": row[0],
            "product_id": row[1],
            "product_name": row[2],
            "name": row[3],
            "branch": row[4],
            "status": row[5],
            "workflow_stage": row[6]
        }
        for row in cursor.fetchall()
    ]
    
    # Get in-progress tasks
    cursor.execute("""
        SELECT t.id, t.feature_id, f.name as feature_name, t.task_id, 
               t.description, t.status
        FROM tasks t
        JOIN features f ON t.feature_id = f.id
        WHERE t.status = 'doing'
        ORDER BY t.updated_at DESC
    """)
    tasks = [
        {
            "id": row[0],
            "feature_id": row[1],
            "feature_name": row[2],
            "task_id": row[3],
            "description": row[4],
            "status": row[5]
        }
        for row in cursor.fetchall()
    ]
    
    conn.close()
    
    return {
        "success": True,
        "data": {
            "products": products,
            "features": features,
            "tasks": tasks
        },
        "message": f"Found {len(features)} active feature(s) and {len(tasks)} in-progress task(s)"
    }

def get_stats(product_id=None):
    """Get project statistics."""
    conn = get_connection()
    cursor = conn.cursor()
    
    where_clause = f"WHERE f.product_id = {product_id}" if product_id else ""
    
    # Feature stats
    cursor.execute(f"""
        SELECT f.status, COUNT(*) 
        FROM features f
        {where_clause}
        GROUP BY f.status
    """)
    feature_stats = dict(cursor.fetchall())
    
    # Task stats
    cursor.execute(f"""
        SELECT t.status, COUNT(*) 
        FROM tasks t
        JOIN features f ON t.feature_id = f.id
        {where_clause}
        GROUP BY t.status
    """)
    task_stats = dict(cursor.fetchall())
    
    # Workflow stage stats
    cursor.execute(f"""
        SELECT f.workflow_stage, COUNT(*) 
        FROM features f
        {where_clause}
        GROUP BY f.workflow_stage
    """)
    workflow_stats = dict(cursor.fetchall())
    
    conn.close()
    
    return {
        "success": True,
        "data": {
            "features": feature_stats,
            "tasks": task_stats,
            "workflow_stages": workflow_stats
        },
        "message": "Statistics generated"
    }

def get_workflow_status(feature_id):
    """Get workflow stage for a feature."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT f.name, f.workflow_stage, f.status,
               COUNT(CASE WHEN t.status = 'done' THEN 1 END) as done_tasks,
               COUNT(*) as total_tasks
        FROM features f
        LEFT JOIN tasks t ON t.feature_id = f.id
        WHERE f.id = ?
        GROUP BY f.id
    """, (feature_id,))
    
    row = cursor.fetchone()
    if not row:
        conn.close()
        return {"success": False, "error": f"Feature {feature_id} not found"}
    
    workflow_stages = ["specify", "clarify", "plan", "tasks", "analyze", "implement"]
    current_stage = row[1]
    current_index = workflow_stages.index(current_stage) if current_stage in workflow_stages else 0
    
    result = {
        "success": True,
        "data": {
            "feature_name": row[0],
            "current_stage": current_stage,
            "status": row[2],
            "progress": f"{row[3]}/{row[4]} tasks completed",
            "next_stage": workflow_stages[current_index + 1] if current_index < len(workflow_stages) - 1 else "completed",
            "completed_stages": workflow_stages[:current_index + 1]
        },
        "message": f"Feature is at {current_stage} stage"
    }
    
    conn.close()
    return result

def main():
    parser = argparse.ArgumentParser(description="Status query")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Current command
    subparsers.add_parser("current", help="Get current work status")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Get project statistics")
    stats_parser.add_argument("--product-id", type=int, help="Filter by product ID")
    
    # Workflow command
    workflow_parser = subparsers.add_parser("workflow", help="Get workflow status")
    workflow_parser.add_argument("--feature-id", type=int, required=True, help="Feature ID")
    
    args = parser.parse_args()
    
    try:
        if args.command == "current":
            result = get_current_work()
        elif args.command == "stats":
            result = get_stats(args.product_id)
        elif args.command == "workflow":
            result = get_workflow_status(args.feature_id)
        
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))
        sys.exit(1)

if __name__ == "__main__":
    main()
