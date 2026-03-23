"""AIMEN program command - Project management tool."""

from textwrap import wrap

from ..database import (
    create_program, get_program, get_all_programs, update_program, delete_program,
    create_task, get_task, get_tasks_by_program, update_task, delete_task
)

# Status presets
PROGRAM_STATUS_OPTIONS = ["未开发", "开发中", "已完成"]
TASK_STATUS_OPTIONS = ["⚪", "🟢", "🔴", "🟡"]
TASK_STATUS_LABELS = {
    "⚪": "未开始",
    "🟢": "已完成",
    "🔴": "阻塞",
    "🟡": "进行中",
}
TASK_STATUS_DETAILS = {
    "⚪": "任务尚未开始执行",
    "🟢": "任务已完成，可进行验收",
    "🔴": "任务被阻塞，需要先排除障碍",
    "🟡": "任务正在推进中",
}


def execute(args):
    """Execute the program command."""
    subcommand = args.subcommand

    if subcommand == "init":
        cmd_init(args.project_name, args.text)
    elif subcommand == "add":
        cmd_add(args.project_id, args.name, args.text, args.criteria)
    elif subcommand == "remove":
        cmd_remove(args.project_id, args.task_id)
    elif subcommand == "status":
        cmd_status(args.project_id, args.task_id)
    elif subcommand == "orch":
        cmd_orch(args.project_id, args.orchestration)
    elif subcommand == "update":
        cmd_update(
            args.id, args.name, args.description, args.status,
            args.notes, args.criteria, args.script, args.orchestration
        )
    else:
        print("Unknown subcommand. Use 'aimen program --help' for usage.")


def _print_title(title: str) -> None:
    print(f"\n{title}")
    print("=" * len(title))


def _print_kv(label: str, value, indent: int = 0) -> None:
    prefix = " " * indent
    text = "-" if value in (None, "") else str(value)
    wrapped_lines = wrap(text, width=88) or [text]
    print(f"{prefix}{label}: {wrapped_lines[0]}")
    for line in wrapped_lines[1:]:
        print(f"{prefix}{' ' * (len(label) + 2)}{line}")


def _get_task_stats(tasks: list[dict]) -> dict[str, int]:
    stats = {status: 0 for status in TASK_STATUS_OPTIONS}
    for task in tasks:
        status = task.get("status", "⚪")
        stats[status] = stats.get(status, 0) + 1
    return stats


def _format_progress(completed: int, total: int, width: int = 20) -> str:
    if total <= 0:
        return "[--------------------] 0%"

    filled = round((completed / total) * width)
    bar = "#" * filled + "-" * (width - filled)
    percent = round((completed / total) * 100)
    return f"[{bar}] {percent}%"


def _print_task_summary(tasks: list[dict], indent: int = 0) -> None:
    stats = _get_task_stats(tasks)
    completed = stats["🟢"]
    total = len(tasks)
    prefix = " " * indent

    print(f"{prefix}Progress: {_format_progress(completed, total)} ({completed}/{total})")
    print(
        f"{prefix}Tasks: ⚪ {stats['⚪']}  "
        f"🟡 {stats['🟡']}  "
        f"🔴 {stats['🔴']}  "
        f"🟢 {stats['🟢']}"
    )


def _print_task_list(tasks: list[dict], indent: int = 0) -> None:
    prefix = " " * indent
    if not tasks:
        print(f"{prefix}No tasks yet.")
        return

    for index, task in enumerate(tasks, start=1):
        status = task["status"]
        label = TASK_STATUS_LABELS.get(status, status)
        print(f"{prefix}{index:>2}. {status} {task['id']}  {task['name']}  [{label}]")
        if task.get("description"):
            description = wrap(str(task["description"]), width=80) or [str(task["description"])]
            for line in description:
                print(f"{prefix}    {line}")


def _format_task_status(status: str) -> str:
    label = TASK_STATUS_LABELS.get(status, status)
    detail = TASK_STATUS_DETAILS.get(status, "")
    if detail:
        return f"{status} {label} ({detail})"
    return f"{status} {label}"


def cmd_init(project_name: str, description: str):
    """Initialize a new project."""
    program_id = create_program(project_name, description)
    print(f"✅ Project created!")
    print(f"   ID: {program_id}")
    print(f"   Name: {project_name}")
    print(f"   Description: {description}")
    print(f"   Status: 未开发")


def cmd_add(project_id: str, name: str, description: str, criteria: str):
    """Add a new task."""
    # Verify program exists
    program = get_program(project_id)
    if not program:
        print(f"❌ Project {project_id} not found.")
        return
    
    task_id = create_task(project_id, name, description, criteria)
    print(f"✅ Task added!")
    print(f"   ID: {task_id}")
    print(f"   Name: {name}")
    print(f"   Status: ⚪")


def cmd_remove(project_id: str, task_id: str = None):
    """Remove project or task."""
    if task_id:
        # Remove task
        task = get_task(task_id)
        if not task:
            print(f"❌ Task {task_id} not found.")
            return
        delete_task(task_id)
        print(f"✅ Task {task_id} removed.")
    else:
        # Remove project
        program = get_program(project_id)
        if not program:
            print(f"❌ Project {project_id} not found.")
            return
        delete_program(project_id)
        print(f"✅ Project {project_id} and all tasks removed.")


def cmd_status(project_id: str = None, task_id: str = None):
    """Show project status."""
    # Allow querying a task directly by its ID (T- prefix) without project_id
    if project_id and project_id.startswith("T-") and not task_id:
        task_id, project_id = project_id, None

    if task_id:
        # Show specific task
        task = get_task(task_id)
        if not task:
            print(f"❌ Task {task_id} not found.")
            return

        program = get_program(task["program_id"])

        _print_title(f"Task {task['id']}")
        _print_kv("Name", task["name"])
        _print_kv("Status", _format_task_status(task["status"]))
        _print_kv("Project", f"{task['program_id']}  {program['name']}" if program else task["program_id"])
        _print_kv("Project Description", program["description"] if program else "-")
        _print_kv("Description", task["description"])
        _print_kv("Acceptance Criteria", task["acceptance_criteria"])
        if task['acceptance_script']:
            _print_kv("Acceptance Script", task["acceptance_script"])
        if task['notes']:
            _print_kv("Notes", task["notes"])

    elif project_id:
        # Show all tasks for a project
        program = get_program(project_id)
        if not program:
            print(f"❌ Project {project_id} not found.")
            return

        tasks = get_tasks_by_program(project_id)

        _print_title(f"Project {program['id']}")
        _print_kv("Name", program["name"])
        _print_kv("Status", program["status"])
        _print_kv("Description", program["description"])
        if program['orchestration']:
            _print_kv("Orchestration", program["orchestration"])
        if program['notes']:
            _print_kv("Notes", program["notes"])

        print()
        _print_task_summary(tasks)
        print("\nTask List")
        print("---------")
        _print_task_list(tasks)

    else:
        # Show all projects
        programs = get_all_programs()
        if not programs:
            print("No projects found.")
            return

        _print_title("All Projects")
        for prog in programs:
            tasks = get_tasks_by_program(prog['id'])
            print(f"\n{prog['id']}  {prog['name']}")
            print(f"{'-' * min(len(prog['id']) + len(prog['name']) + 2, 60)}")
            _print_kv("Status", prog["status"], indent=2)
            _print_kv("Description", prog["description"], indent=2)
            _print_task_summary(tasks, indent=2)
            if prog['orchestration']:
                _print_kv("Orchestration", prog["orchestration"], indent=2)


def cmd_orch(project_id: str, orchestration: str):
    """Set project orchestration."""
    program = get_program(project_id)
    if not program:
        print(f"❌ Project {project_id} not found.")
        return

    update_program(project_id, orchestration=orchestration)
    print(f"✅ Orchestration updated for project {project_id}.")
    print(f"   {orchestration}")


def cmd_update(id: str, name: str = None, description: str = None, status: str = None,
               notes: str = None, criteria: str = None, script: str = None, orchestration: str = None):
    """Update project or task fields."""
    # Determine if it's a project or task by ID prefix
    if id.startswith("P-"):
        # Update project
        program = get_program(id)
        if not program:
            print(f"❌ Project {id} not found.")
            return

        # Validate status if provided
        if status and status not in PROGRAM_STATUS_OPTIONS:
            print(f"❌ Invalid status. Valid options: {', '.join(PROGRAM_STATUS_OPTIONS)}")
            return

        # Build update fields
        updates = {}
        if name:
            updates["name"] = name
        if description is not None:
            updates["description"] = description
        if status:
            updates["status"] = status
        if notes is not None:
            updates["notes"] = notes
        if orchestration is not None:
            updates["orchestration"] = orchestration

        if not updates:
            print("⚠️ No fields provided to update.")
            return

        update_program(id, **updates)
        print(f"✅ Project {id} updated!")
        for field, value in updates.items():
            print(f"   {field}: {value}")

    elif id.startswith("T-"):
        # Update task
        task = get_task(id)
        if not task:
            print(f"❌ Task {id} not found.")
            return

        # Validate status if provided
        if status and status not in TASK_STATUS_OPTIONS:
            print(f"❌ Invalid status. Valid options: {', '.join(TASK_STATUS_OPTIONS)}")
            return

        # Build update fields
        updates = {}
        if name:
            updates["name"] = name
        if description is not None:
            updates["description"] = description
        if status:
            updates["status"] = status
        if notes is not None:
            updates["notes"] = notes
        if criteria is not None:
            updates["acceptance_criteria"] = criteria
        if script is not None:
            updates["acceptance_script"] = script

        if not updates:
            print("⚠️ No fields provided to update.")
            return

        update_task(id, **updates)
        print(f"✅ Task {id} updated!")
        for field, value in updates.items():
            print(f"   {field}: {value}")

    else:
        print(f"❌ Invalid ID format. Expected P-xxx or T-xxx, got: {id}")
