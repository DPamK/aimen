"""AIMEN CLI - Main command line interface."""

import argparse
import sys
from .commands import init_command, program_command, memory_command


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for aimen CLI."""
    parser = argparse.ArgumentParser(
        prog="aimen",
        description="AIMEN - AI-driven Development Workflow",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="<command>")

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize a new AIMEN project")
    init_parser.add_argument(
        "--mode",
        choices=["dev", "quick"],
        help="Work mode (default: dev)",
    )
    init_parser.add_argument(
        "--agent",
        choices=["claude", "cursor", "copilot", "opencode", "codex", "gemini", "qwen"],
        help="AI agent to use (default: claude)",
    )

    # program command
    program_parser = subparsers.add_parser("program", help="Project management tool")
    program_subparsers = program_parser.add_subparsers(dest="subcommand", metavar="<subcommand>")

    # program init
    prog_init = program_subparsers.add_parser("init", help="Initialize a new project")
    prog_init.add_argument("project_name", help="Project name")
    prog_init.add_argument("-t", "--text", required=True, help="Project description")

    # program add
    prog_add = program_subparsers.add_parser("add", help="Add a new task")
    prog_add.add_argument("project_id", help="Project ID")
    prog_add.add_argument("-n", "--name", required=True, help="Task name")
    prog_add.add_argument("-t", "--text", required=True, help="Task description")
    prog_add.add_argument("-c", "--criteria", required=True, help="Acceptance criteria")

    # program remove
    prog_remove = program_subparsers.add_parser("remove", help="Remove project or task")
    prog_remove.add_argument("project_id", help="Project ID")
    prog_remove.add_argument("task_id", nargs="?", help="Task ID (optional)")

    # program status
    prog_status = program_subparsers.add_parser("status", help="Show project status")
    prog_status.add_argument("project_id", nargs="?", help="Project ID (optional)")
    prog_status.add_argument("task_id", nargs="?", help="Task ID (optional)")

    # program orch
    prog_orch = program_subparsers.add_parser("orch", help="Set project orchestration")
    prog_orch.add_argument("project_id", help="Project ID")
    prog_orch.add_argument("orchestration", help="Orchestration text")

    # program update
    prog_update = program_subparsers.add_parser("update", help="Update project or task")
    prog_update.add_argument("id", help="Project ID (P-xxx) or Task ID (T-xxx)")
    prog_update.add_argument("--name", help="New name")
    prog_update.add_argument("--description", help="New description")
    prog_update.add_argument("--status", help="New status (project: 未开发/开发中/已完成, task: ⚪/🟢/🔴/🟡)")
    prog_update.add_argument("--notes", help="Notes")
    prog_update.add_argument("--criteria", help="Acceptance criteria (task only)")
    prog_update.add_argument("--script", help="Acceptance script (task only)")
    prog_update.add_argument("--orchestration", help="Orchestration config (project only)")

    # memory command
    memory_parser = subparsers.add_parser("memory", help="Memory and identity management")
    memory_subparsers = memory_parser.add_subparsers(dest="subcommand", metavar="<subcommand>")

    # memory init
    memory_subparsers.add_parser("init", help="Initialize memory structure")

    return parser, program_parser, memory_parser


def main():
    """Main entry point for aimen CLI."""
    parser, program_parser, memory_parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    try:
        if args.command == "init":
            init_command.execute(args)
        elif args.command == "program":
            if not args.subcommand:
                program_parser.print_help()
                sys.exit(0)
            program_command.execute(args)
        elif args.command == "memory":
            if not args.subcommand:
                memory_parser.print_help()
                sys.exit(0)
            memory_command.execute(args)
        else:
            parser.print_help()
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
