#!/usr/bin/env python3
"""Manage .aimen/situation.md - AIMEN's working context file."""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime


SITUATION_PATH = Path(".aimen") / "situation.md"


def parse_situation():
    """Parse situation.md and extract structured fields."""
    content = SITUATION_PATH.read_text(encoding="utf-8")

    fields = {
        "project": "(无)",
        "project_id": "",
        "feature": "(无)",
        "feature_id": "",
        "task": "(无)",
        "task_id": "",
        "status": "空闲",
        "updated_at": "",
        "note": "(无)"
    }

    in_note = False
    note_lines = []
    for line in content.split("\n"):
        # Parse note section
        if line.strip() == "## 备注":
            in_note = True
            continue
        if in_note:
            if line.startswith("## "):
                in_note = False
            else:
                note_lines.append(line)
            continue

        # Parse bullet fields
        line_stripped = line.strip()
        if line_stripped.startswith("- **项目**："):
            fields["project"] = line_stripped.split("：", 1)[1].strip()
        elif line_stripped.startswith("- **项目 ID**："):
            fields["project_id"] = line_stripped.split("：", 1)[1].strip()
        elif line_stripped.startswith("- **功能**："):
            fields["feature"] = line_stripped.split("：", 1)[1].strip()
        elif line_stripped.startswith("- **功能 ID**："):
            fields["feature_id"] = line_stripped.split("：", 1)[1].strip()
        elif line_stripped.startswith("- **开发任务**："):
            fields["task"] = line_stripped.split("：", 1)[1].strip()
        elif line_stripped.startswith("- **任务 ID**："):
            fields["task_id"] = line_stripped.split("：", 1)[1].strip()
        elif line_stripped.startswith("- **执行状态**："):
            fields["status"] = line_stripped.split("：", 1)[1].strip()
        elif line_stripped.startswith("- **更新时间**："):
            fields["updated_at"] = line_stripped.split("：", 1)[1].strip()

    note_text = "\n".join(note_lines).strip()
    if note_text:
        fields["note"] = note_text

    return fields


def render_situation(fields):
    """Render situation data into markdown format."""
    return f"""# AIMEN 工作状态

> 此文件由 AIMEN 管理，记录当前工作上下文与进度。

## 当前执行

- **项目**：{fields.get('project', '(无)')}
- **项目 ID**：{fields.get('project_id', '')}
- **功能**：{fields.get('feature', '(无)')}
- **功能 ID**：{fields.get('feature_id', '')}
- **开发任务**：{fields.get('task', '(无)')}
- **任务 ID**：{fields.get('task_id', '')}
- **执行状态**：{fields.get('status', '空闲')}
- **更新时间**：{fields.get('updated_at', '')}

## 备注

{fields.get('note', '(无)')}
"""


def update_situation(project=None, feature=None, task=None, status=None, note=None,
                     project_id=None, feature_id=None, task_id=None):
    """Update situation.md with provided fields (only updates non-None fields)."""
    if not SITUATION_PATH.exists():
        return {"success": False, "error": f"{SITUATION_PATH} not found. Run init.py first."}

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current = parse_situation()

    if project is not None:
        current["project"] = project
    if project_id is not None:
        current["project_id"] = project_id
    if feature is not None:
        current["feature"] = feature
    if feature_id is not None:
        current["feature_id"] = feature_id
    if task is not None:
        current["task"] = task
    if task_id is not None:
        current["task_id"] = task_id
    if status is not None:
        current["status"] = status
    if note is not None:
        current["note"] = note
    current["updated_at"] = now

    content = render_situation(current)
    SITUATION_PATH.write_text(content, encoding="utf-8")

    return {
        "success": True,
        "message": "situation.md updated",
        "data": current
    }


def clear_situation():
    """Reset situation.md to idle state."""
    if not SITUATION_PATH.exists():
        return {"success": False, "error": f"{SITUATION_PATH} not found. Run init.py first."}

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current = {
        "project": "(无)",
        "project_id": "",
        "feature": "(无)",
        "feature_id": "",
        "task": "(无)",
        "task_id": "",
        "status": "空闲",
        "updated_at": now,
        "note": "(无)"
    }

    content = render_situation(current)
    SITUATION_PATH.write_text(content, encoding="utf-8")

    return {
        "success": True,
        "message": "situation.md reset to idle",
        "data": current
    }


def show_situation():
    """Show current situation."""
    if not SITUATION_PATH.exists():
        return {"success": False, "error": f"{SITUATION_PATH} not found. Run init.py first."}

    current = parse_situation()
    return {
        "success": True,
        "data": current
    }


def main():
    parser = argparse.ArgumentParser(description="Manage .aimen/situation.md")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Update command
    update_parser = subparsers.add_parser("update", help="Update situation fields")
    update_parser.add_argument("--project", help="Current project name")
    update_parser.add_argument("--project-id", help="Current project ID")
    update_parser.add_argument("--feature", help="Current feature name")
    update_parser.add_argument("--feature-id", help="Current feature ID")
    update_parser.add_argument("--task", help="Current task description")
    update_parser.add_argument("--task-id", help="Current task ID")
    update_parser.add_argument("--status", help="Execution status (e.g. 空闲, 开发中, 测试中, 已完成)")
    update_parser.add_argument("--note", help="Notes / remarks")

    # Clear command
    subparsers.add_parser("clear", help="Reset situation to idle state")

    # Show command
    subparsers.add_parser("show", help="Show current situation")

    args = parser.parse_args()

    try:
        if args.command == "update":
            result = update_situation(
                project=args.project,
                project_id=args.project_id,
                feature=args.feature,
                feature_id=args.feature_id,
                task=args.task,
                task_id=args.task_id,
                status=args.status,
                note=args.note
            )
        elif args.command == "clear":
            result = clear_situation()
        elif args.command == "show":
            result = show_situation()

        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
