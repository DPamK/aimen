"""AIMEN program command - Project management tool."""

from ..database import (
    create_program, get_program, get_all_programs, update_program, delete_program,
    create_task, get_task, get_tasks_by_program, update_task, delete_task
)

# Status presets
PROGRAM_STATUS_OPTIONS = ["未开发", "开发中", "已完成"]
TASK_STATUS_OPTIONS = ["⚪", "🟢", "🔴", "🟡"]


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
        
        print(f"\n📋 Task: {task['name']}")
        print(f"   ID: {task['id']}")
        print(f"   Status: {task['status']}")
        print(f"   Description: {task['description']}")
        print(f"   Acceptance Criteria: {task['acceptance_criteria']}")
        if task['acceptance_script']:
            print(f"   Acceptance Script: {task['acceptance_script']}")
        if task['notes']:
            print(f"   Notes: {task['notes']}")
    
    elif project_id:
        # Show all tasks for a project
        program = get_program(project_id)
        if not program:
            print(f"❌ Project {project_id} not found.")
            return
        
        print(f"\n📊 Project: {program['name']} ({program['id']})")
        print(f"   Status: {program['status']}")
        print(f"   Description: {program['description']}")
        if program['orchestration']:
            print(f"   Orchestration: {program['orchestration']}")
        
        tasks = get_tasks_by_program(project_id)
        if tasks:
            print(f"\n   Tasks ({len(tasks)}):")
            for task in tasks:
                print(f"   - [{task['status']}] {task['id']}: {task['name']}")
        else:
            print("\n   No tasks yet.")
    
    else:
        # Show all projects
        programs = get_all_programs()
        if not programs:
            print("No projects found.")
            return
        
        print("\n📊 All Projects:")
        for prog in programs:
            tasks = get_tasks_by_program(prog['id'])
            completed = sum(1 for t in tasks if '🟢' in t['status'])
            total = len(tasks)
            print(f"\n   [{prog['status']}] {prog['id']}: {prog['name']}")
            print(f"       Description: {prog['description']}")
            print(f"       Progress: {completed}/{total} tasks completed")
            if prog['orchestration']:
                print(f"       Orchestration: {prog['orchestration']}")


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
