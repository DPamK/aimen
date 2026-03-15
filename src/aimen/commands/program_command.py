"""AIMEN program command - Project management tool."""

from ..database import (
    create_program, get_program, get_all_programs, update_program, delete_program,
    create_task, get_task, get_tasks_by_program, update_task, delete_task
)


def execute(args):
    """Execute the program command."""
    subcommand = args.subcommand
    
    if subcommand == "init":
        cmd_init(args.project_name, args.text)
    elif subcommand == "add":
        cmd_add(args.project_id, args.name, args.text, args.criteria)
    elif subcommand == "remove":
        cmd_remove(args.project_id, args.requirement_id)
    elif subcommand == "status":
        cmd_status(args.project_id, args.requirement_id)
    elif subcommand == "orch":
        cmd_orch(args.project_id, args.orchestration)
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
    """Add a new requirement."""
    # Verify program exists
    program = get_program(project_id)
    if not program:
        print(f"❌ Project {project_id} not found.")
        return
    
    task_id = create_task(project_id, name, description, criteria)
    print(f"✅ Requirement added!")
    print(f"   ID: {task_id}")
    print(f"   Name: {name}")
    print(f"   Status: ⚪")


def cmd_remove(project_id: str, requirement_id: str = None):
    """Remove project or requirement."""
    if requirement_id:
        # Remove requirement
        task = get_task(requirement_id)
        if not task:
            print(f"❌ Requirement {requirement_id} not found.")
            return
        delete_task(requirement_id)
        print(f"✅ Requirement {requirement_id} removed.")
    else:
        # Remove project
        program = get_program(project_id)
        if not program:
            print(f"❌ Project {project_id} not found.")
            return
        delete_program(project_id)
        print(f"✅ Project {project_id} and all requirements removed.")


def cmd_status(project_id: str = None, requirement_id: str = None):
    """Show project status."""
    if requirement_id and project_id:
        # Show specific requirement
        task = get_task(requirement_id)
        if not task:
            print(f"❌ Requirement {requirement_id} not found.")
            return
        
        print(f"\n📋 Requirement: {task['name']}")
        print(f"   ID: {task['id']}")
        print(f"   Status: {task['status']}")
        print(f"   Description: {task['description']}")
        print(f"   Acceptance Criteria: {task['acceptance_criteria']}")
        if task['acceptance_script']:
            print(f"   Acceptance Script: {task['acceptance_script']}")
        if task['notes']:
            print(f"   Notes: {task['notes']}")
    
    elif project_id:
        # Show all requirements for a project
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
            print(f"\n   Requirements ({len(tasks)}):")
            for task in tasks:
                print(f"   - [{task['status']}] {task['id']}: {task['name']}")
        else:
            print("\n   No requirements yet.")
    
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
            print(f"       Progress: {completed}/{total} requirements completed")
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
