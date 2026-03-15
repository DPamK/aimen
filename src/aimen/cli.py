"""AIMEN CLI - Main command line interface."""

import argparse
import sys
from .commands import init_command, program_command


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for aimen CLI."""
    parser = argparse.ArgumentParser(
        prog="aimen",
        description="AIMEN - AI-driven Development Workflow System",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="<command>")

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize a new AIMEN project")

    # program command
    program_parser = subparsers.add_parser("program", help="Project management tool")
    program_subparsers = program_parser.add_subparsers(dest="subcommand", metavar="<subcommand>")

    # program init
    prog_init = program_subparsers.add_parser("init", help="Initialize a new project")
    prog_init.add_argument("project_name", help="Project name")
    prog_init.add_argument("-t", "--text", required=True, help="Project description")

    # program add
    prog_add = program_subparsers.add_parser("add", help="Add a new requirement")
    prog_add.add_argument("project_id", help="Project ID")
    prog_add.add_argument("-n", "--name", required=True, help="Requirement name")
    prog_add.add_argument("-t", "--text", required=True, help="Requirement description")
    prog_add.add_argument("-c", "--criteria", required=True, help="Acceptance criteria")

    # program remove
    prog_remove = program_subparsers.add_parser("remove", help="Remove project or requirement")
    prog_remove.add_argument("project_id", help="Project ID")
    prog_remove.add_argument("requirement_id", nargs="?", help="Requirement ID (optional)")

    # program status
    prog_status = program_subparsers.add_parser("status", help="Show project status")
    prog_status.add_argument("project_id", nargs="?", help="Project ID (optional)")
    prog_status.add_argument("requirement_id", nargs="?", help="Requirement ID (optional)")

    # program orch
    prog_orch = program_subparsers.add_parser("orch", help="Set project orchestration")
    prog_orch.add_argument("project_id", help="Project ID")
    prog_orch.add_argument("orchestration", help="Orchestration text")

    return parser


def main():
    """Main entry point for aimen CLI."""
    parser = create_parser()
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
