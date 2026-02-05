#!/usr/bin/env python3
"""State transition script."""

import sqlite3
import json
import sys
import argparse
from pathlib import Path

DB_PATH = Path(__file__).parent / "project.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def complete_feature(feature_id):
    """Mark feature and all tasks as completed."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Update feature
    cursor.execute(
        """UPDATE features 
           SET status = 'completed', workflow_stage = 'implement', updated_at = CURRENT_TIMESTAMP
           WHERE id = ?""",
        (feature_id,)
    )
    
    # Update all tasks
    cursor.execute(
        "UPDATE tasks SET status = 'done', updated_at = CURRENT_TIMESTAMP WHERE feature_id = ?",
        (feature_id,)
    )
    
    # Log history
    cursor.execute(
        "INSERT INTO history (entity_type, entity_id, action, new_value) VALUES (?, ?, ?, ?)",
        ("feature", feature_id, "completed", "All tasks marked as done")
    )
    
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "message": f"Feature {feature_id} marked as completed"
    }

def pause_feature(feature_id):
    """Pause a feature."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE features SET status = 'paused', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (feature_id,)
    )
    
    # Log history
    cursor.execute(
        "INSERT INTO history (entity_type, entity_id, action, new_value) VALUES (?, ?, ?, ?)",
        ("feature", feature_id, "paused", "Feature paused")
    )
    
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "message": f"Feature {feature_id} paused"
    }

def resume_feature(feature_id):
    """Resume a paused feature."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE features SET status = 'implementing', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (feature_id,)
    )
    
    # Log history
    cursor.execute(
        "INSERT INTO history (entity_type, entity_id, action, new_value) VALUES (?, ?, ?, ?)",
        ("feature", feature_id, "resumed", "Feature resumed")
    )
    
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "message": f"Feature {feature_id} resumed"
    }

def advance_workflow(feature_id, next_stage):
    """Advance feature to next workflow stage."""
    conn = get_connection()
    cursor = conn.cursor()
    
    valid_stages = ["specify", "clarify", "plan", "tasks", "analyze", "implement"]
    if next_stage not in valid_stages:
        return {"success": False, "error": f"Invalid stage. Must be one of: {', '.join(valid_stages)}"}
    
    cursor.execute(
        "UPDATE features SET workflow_stage = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (next_stage, feature_id)
    )
    
    # Log history
    cursor.execute(
        "INSERT INTO history (entity_type, entity_id, action, new_value) VALUES (?, ?, ?, ?)",
        ("feature", feature_id, "workflow_advanced", next_stage)
    )
    
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "message": f"Feature {feature_id} advanced to {next_stage} stage"
    }

def main():
    parser = argparse.ArgumentParser(description="State transition")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Complete feature command
    complete_parser = subparsers.add_parser("complete-feature", help="Complete a feature")
    complete_parser.add_argument("--feature-id", type=int, required=True, help="Feature ID")
    
    # Pause command
    pause_parser = subparsers.add_parser("pause", help="Pause a feature")
    pause_parser.add_argument("--feature-id", type=int, required=True, help="Feature ID")
    
    # Resume command
    resume_parser = subparsers.add_parser("resume", help="Resume a feature")
    resume_parser.add_argument("--feature-id", type=int, required=True, help="Feature ID")
    
    # Advance workflow command
    advance_parser = subparsers.add_parser("advance", help="Advance workflow stage")
    advance_parser.add_argument("--feature-id", type=int, required=True, help="Feature ID")
    advance_parser.add_argument("--next-stage", required=True, help="Next stage")
    
    args = parser.parse_args()
    
    try:
        if args.command == "complete-feature":
            result = complete_feature(args.feature_id)
        elif args.command == "pause":
            result = pause_feature(args.feature_id)
        elif args.command == "resume":
            result = resume_feature(args.feature_id)
        elif args.command == "advance":
            result = advance_workflow(args.feature_id, args.next_stage)
        
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))
        sys.exit(1)

if __name__ == "__main__":
    main()
