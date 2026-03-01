#!/usr/bin/env python3
"""Utility queries for project management - common shortcuts."""

import sqlite3
import json
import sys
import argparse
from pathlib import Path


DB_PATH = Path(".aimen") / "project.db"


def get_connection():
    """Get database connection or exit with error."""
    if not DB_PATH.exists():
        print(json.dumps(
            {"success": False, "error": f"Database not found at {DB_PATH}. Run init.py first."},
            ensure_ascii=False
        ))
        sys.exit(1)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def current_work():
    """Get current active work context: doing tasks + active features."""
    conn = get_connection()
    try:
        cursor = conn.cursor()

        # Currently executing tasks (TDD in-progress: status in active TDD stages)
        cursor.execute("""
            SELECT t.id, t.title, t.description, t.status, t.tdd_stage, t.file_path, t.test_file, t.priority,
                   f.id AS feature_id, f.name AS feature_name, f.workflow_stage, f.branch,
                   p.id AS project_id, p.name AS project_name
            FROM tasks t
            JOIN features f ON t.feature_id = f.id
            JOIN project p ON f.project_id = p.id
            WHERE t.status IN ('write_test', 'red', 'green', 'refactor', 'blocked')
            ORDER BY t.updated_at DESC
        """)
        doing_tasks = [dict(row) for row in cursor.fetchall()]

        # Active features (not completed / not paused)
        cursor.execute("""
            SELECT f.id, f.name, f.status, f.workflow_stage, f.branch, f.priority,
                   p.name AS project_name,
                   COUNT(CASE WHEN t.status = 'done' THEN 1 END) AS done_count,
                   COUNT(CASE WHEN t.status IN ('write_test','red','green','refactor') THEN 1 END) AS doing_count,
                   COUNT(CASE WHEN t.status = 'todo' THEN 1 END) AS todo_count,
                   COUNT(CASE WHEN t.status = 'blocked' THEN 1 END) AS blocked_count,
                   COUNT(t.id) AS total_tasks
            FROM features f
            JOIN project p ON f.project_id = p.id
            LEFT JOIN tasks t ON t.feature_id = f.id
            WHERE f.status NOT IN ('completed', 'paused')
            GROUP BY f.id
            ORDER BY f.updated_at DESC
        """)
        active_features = [dict(row) for row in cursor.fetchall()]

        return {
            "success": True,
            "data": {
                "doing_tasks": doing_tasks,
                "active_features": active_features
            },
            "summary": f"正在执行 {len(doing_tasks)} 个任务，{len(active_features)} 个活跃功能"
        }
    finally:
        conn.close()


def pending_tasks(limit=10):
    """Get next N pending (todo) tasks, ordered by priority."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT t.id, t.title, t.description, t.priority, t.file_path,
               f.id AS feature_id, f.name AS feature_name, f.branch,
               p.name AS project_name
        FROM tasks t
        JOIN features f ON t.feature_id = f.id
        JOIN project p ON f.project_id = p.id
        WHERE t.status = 'todo'
          AND f.status NOT IN ('completed', 'paused')
        ORDER BY
            CASE t.priority
                WHEN 'critical' THEN 0
                WHEN 'high' THEN 1
                WHEN 'medium' THEN 2
                WHEN 'low' THEN 3
            END,
            t.created_at ASC
        LIMIT ?
    """, (limit,))

        tasks = [dict(row) for row in cursor.fetchall()]
        return {
            "success": True,
            "data": tasks,
            "message": f"待执行任务 {len(tasks)} 条（最多显示 {limit} 条）"
        }
    finally:
        conn.close()


def completed_tasks(limit=10):
    """Get last N completed tasks, most recent first."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT t.id, t.title, t.description, t.file_path, t.test_file,
               COALESCE(t.completed_at, t.updated_at) AS finished_at,
               f.id AS feature_id, f.name AS feature_name,
               p.name AS project_name
        FROM tasks t
        JOIN features f ON t.feature_id = f.id
        JOIN project p ON f.project_id = p.id
        WHERE t.status = 'done'
        ORDER BY COALESCE(t.completed_at, t.updated_at) DESC
        LIMIT ?
    """, (limit,))

        tasks = [dict(row) for row in cursor.fetchall()]
        return {
            "success": True,
            "data": tasks,
            "message": f"已完成任务 {len(tasks)} 条（最多显示 {limit} 条）"
        }
    finally:
        conn.close()


def overview():
    """Get overall project statistics."""
    conn = get_connection()
    try:
        cursor = conn.cursor()

        # project stats
        cursor.execute("SELECT status, COUNT(*) AS cnt FROM project GROUP BY status")
        proj_stats = {row["status"]: row["cnt"] for row in cursor.fetchall()}

        # Feature stats
        cursor.execute("SELECT status, COUNT(*) AS cnt FROM features GROUP BY status")
        feat_stats = {row["status"]: row["cnt"] for row in cursor.fetchall()}

        # Task stats
        cursor.execute("SELECT status, COUNT(*) AS cnt FROM tasks GROUP BY status")
        task_stats = {row["status"]: row["cnt"] for row in cursor.fetchall()}

        # Recent changelog
        cursor.execute("""
            SELECT entity_type, entity_id, field, old_value, new_value, created_at
            FROM changelog
            ORDER BY created_at DESC
            LIMIT 10
        """)
        recent = [dict(row) for row in cursor.fetchall()]

        total_tasks = sum(task_stats.values()) if task_stats else 0
        done_tasks = task_stats.get("done", 0)

        return {
            "success": True,
            "data": {
                "project": proj_stats,
                "features": feat_stats,
                "tasks": task_stats,
                "recent_changelog": recent
            },
            "summary": (
                f"项目 {sum(proj_stats.values()) if proj_stats else 0} 个,"
                f"功能 {sum(feat_stats.values()) if feat_stats else 0} 个，"
                f"任务 {total_tasks} 个（已完成 {done_tasks}）"
            )
        }
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="Project management utility queries")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Current work
    subparsers.add_parser("current", help="Show current active work (doing tasks & active features)")

    # Pending tasks
    pending_parser = subparsers.add_parser("pending", help="Show next pending tasks")
    pending_parser.add_argument("--limit", type=int, default=10, help="Max results (default: 10)")

    # Completed tasks
    completed_parser = subparsers.add_parser("completed", help="Show recently completed tasks")
    completed_parser.add_argument("--limit", type=int, default=10, help="Max results (default: 10)")

    # Overview
    subparsers.add_parser("overview", help="Show project statistics overview")

    args = parser.parse_args()

    try:
        if args.command == "current":
            result = current_work()
        elif args.command == "pending":
            result = pending_tasks(args.limit)
        elif args.command == "completed":
            result = completed_tasks(args.limit)
        elif args.command == "overview":
            result = overview()

        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
