#!/usr/bin/env python3
"""Execute SQL commands on .aimen/project.db."""

import sqlite3
import json
import sys
import argparse
from pathlib import Path


DB_PATH = Path(".aimen") / "project.db"


def execute_sql(sql, params=None):
    """Execute a single SQL statement and return results."""
    if not DB_PATH.exists():
        return {"success": False, "error": f"Database not found at {DB_PATH}. Run init.py first."}

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)

        result = {"success": True}
        sql_upper = sql.strip().upper()

        # SELECT / WITH / PRAGMA → return rows
        if sql_upper.startswith("SELECT") or sql_upper.startswith("WITH") or sql_upper.startswith("PRAGMA"):
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            data = [dict(row) for row in rows]
            result["data"] = data
            result["columns"] = columns
            result["count"] = len(data)
            result["message"] = f"Query returned {len(data)} row(s)"
        else:
            conn.commit()
            result["affected_rows"] = cursor.rowcount
            result["last_id"] = cursor.lastrowid
            result["message"] = f"Statement executed, {cursor.rowcount} row(s) affected"

        return result

    except Exception as e:
        conn.rollback()
        return {"success": False, "error": str(e), "sql": sql}
    finally:
        conn.close()


def execute_script(sql_script):
    """Execute multiple SQL statements as a script."""
    if not DB_PATH.exists():
        return {"success": False, "error": f"Database not found at {DB_PATH}. Run init.py first."}

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        conn.executescript(sql_script)
        return {"success": True, "message": "Script executed successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        conn.close()


def show_schema():
    """Show database schema."""
    return execute_sql("""
        SELECT type, name, sql
        FROM sqlite_master
        WHERE type IN ('table', 'index') AND name NOT LIKE 'sqlite_%'
        ORDER BY type, name
    """)


def main():
    parser = argparse.ArgumentParser(description="Execute SQL on .aimen/project.db")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Execute single SQL
    exec_parser = subparsers.add_parser("exec", help="Execute a single SQL statement")
    exec_parser.add_argument("--sql", required=True, help="SQL statement to execute")
    exec_parser.add_argument("--params", help="JSON array of parameters for parameterized queries")

    # Execute SQL script (multiple statements)
    script_parser = subparsers.add_parser("script", help="Execute multiple SQL statements")
    script_parser.add_argument("--sql", required=True, help="SQL script with multiple statements separated by ;")

    # Show schema
    subparsers.add_parser("schema", help="Show database table schema")

    args = parser.parse_args()

    try:
        if args.command == "exec":
            params = json.loads(args.params) if args.params else None
            result = execute_sql(args.sql, params)
        elif args.command == "script":
            result = execute_script(args.sql)
        elif args.command == "schema":
            result = show_schema()

        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
