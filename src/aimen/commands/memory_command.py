"""AIMEN memory command - Memory and identity management."""

from pathlib import Path


MEMORY_TEMPLATE = """# Memory

## Long-term Memory

### Key Decisions
- 

### Important Context
- 

### Project History
- 

## Short-term Memory

### Current Focus
- 

### Recent Changes
- 

### Pending Tasks
- 
"""

IDENTITY_TEMPLATE = """# Identity

## Core Identity
- Name: 
- Role: 
- Purpose: 

## Capabilities
- 

## Constraints
- 

## Preferences
- 

## Communication Style
- 
"""


def execute(args):
    """Execute the memory command."""
    subcommand = args.subcommand

    if subcommand == "init":
        cmd_init()
    else:
        print("Unknown subcommand. Use 'aimen memory --help' for usage.")


def cmd_init():
    """Initialize memory structure in .aimen directory."""
    aimen_dir = Path.cwd() / ".aimen"

    if not aimen_dir.exists():
        print("ERROR: .aimen directory not found. Run 'aimen init' first.")
        return

    # Create memory.md
    memory_file = aimen_dir / "memory.md"
    if memory_file.exists():
        print("WARNING: memory.md already exists. Skipping.")
    else:
        memory_file.write_text(MEMORY_TEMPLATE, encoding="utf-8")
        print("Created memory.md")

    # Create identity.md
    identity_file = aimen_dir / "identity.md"
    if identity_file.exists():
        print("WARNING: identity.md already exists. Skipping.")
    else:
        identity_file.write_text(IDENTITY_TEMPLATE, encoding="utf-8")
        print("Created identity.md")

    # Create pocket directory
    pocket_dir = aimen_dir / "pocket"
    if pocket_dir.exists():
        print("WARNING: pocket directory already exists. Skipping.")
    else:
        pocket_dir.mkdir(parents=True, exist_ok=True)
        print("Created pocket directory")

    print("\nMemory initialization complete!")
