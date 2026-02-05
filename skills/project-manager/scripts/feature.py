#!/usr/bin/env python3
"""Feature management script."""

import sqlite3
import json
import sys
import argparse
from pathlib import Path

DB_PATH = Path(__file__).parent / "project.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_feature(product_id, name, branch=None, priority="medium"):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """INSERT INTO features (product_id, name, branch, priority) 
           VALUES (?, ?, ?, ?)""",
        (product_id, name, branch, priority)
    )
    feature_id = cursor.lastrowid
    
    # Log history
    cursor.execute(
        "INSERT INTO history (entity_type, entity_id, action, new_value) VALUES (?, ?, ?, ?)",
        ("feature", feature_id, "created", f"{name} (branch: {branch})")
    )
    
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "data": {"id": feature_id, "product_id": product_id, "name": name, "branch": branch},
        "message": f"Feature created with ID {feature_id}"
    }

def list_features(product_id=None, status=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT f.id, f.product_id, p.name as product_name, f.name, f.branch, 
               f.status, f.priority, f.workflow_stage, f.created_at
        FROM features f
        JOIN products p ON f.product_id = p.id
        WHERE 1=1
    """
    params = []
    
    if product_id:
        query += " AND f.product_id = ?"
        params.append(product_id)
    if status:
        query += " AND f.status = ?"
        params.append(status)
    
    cursor.execute(query, params)
    
    features = [
        {
            "id": row[0],
            "product_id": row[1],
            "product_name": row[2],
            "name": row[3],
            "branch": row[4],
            "status": row[5],
            "priority": row[6],
            "workflow_stage": row[7],
            "created_at": row[8]
        }
        for row in cursor.fetchall()
    ]
    
    conn.close()
    
    return {
        "success": True,
        "data": features,
        "message": f"Found {len(features)} feature(s)"
    }

def update_feature(feature_id, status=None, workflow_stage=None, priority=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    if status:
        updates.append("status = ?")
        params.append(status)
    if workflow_stage:
        updates.append("workflow_stage = ?")
        params.append(workflow_stage)
    if priority:
        updates.append("priority = ?")
        params.append(priority)
    
    if not updates:
        return {"success": False, "error": "No updates specified"}
    
    updates.append("updated_at = CURRENT_TIMESTAMP")
    params.append(feature_id)
    
    cursor.execute(
        f"UPDATE features SET {', '.join(updates)} WHERE id = ?",
        params
    )
    
    # Log history
    if status:
        cursor.execute(
            "INSERT INTO history (entity_type, entity_id, action, new_value) VALUES (?, ?, ?, ?)",
            ("feature", feature_id, "status_changed", status)
        )
    if workflow_stage:
        cursor.execute(
            "INSERT INTO history (entity_type, entity_id, action, new_value) VALUES (?, ?, ?, ?)",
            ("feature", feature_id, "workflow_stage_changed", workflow_stage)
        )
    
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "message": f"Feature {feature_id} updated"
    }

def main():
    parser = argparse.ArgumentParser(description="Feature management")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new feature")
    create_parser.add_argument("--product-id", type=int, required=True, help="Product ID")
    create_parser.add_argument("--name", required=True, help="Feature name")
    create_parser.add_argument("--branch", help="Git branch name")
    create_parser.add_argument("--priority", default="medium", help="Priority (low/medium/high)")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List features")
    list_parser.add_argument("--product-id", type=int, help="Filter by product ID")
    list_parser.add_argument("--status", help="Filter by status")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update a feature")
    update_parser.add_argument("--id", type=int, required=True, help="Feature ID")
    update_parser.add_argument("--status", help="New status")
    update_parser.add_argument("--workflow-stage", help="New workflow stage")
    update_parser.add_argument("--priority", help="New priority")
    
    args = parser.parse_args()
    
    try:
        if args.command == "create":
            result = create_feature(args.product_id, args.name, args.branch, args.priority)
        elif args.command == "list":
            result = list_features(args.product_id, args.status)
        elif args.command == "update":
            result = update_feature(args.id, args.status, args.workflow_stage, args.priority)
        
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))
        sys.exit(1)

if __name__ == "__main__":
    main()
