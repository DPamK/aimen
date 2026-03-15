"""AIMEN init command - Initialize a new project."""

import os
import shutil
from pathlib import Path
from ..database import init_db


def execute(args):
    """Execute the init command."""
    print_aimen_logo()
    
    # Interactive tool selection
    tool = select_tool_interactive()
    
    if not tool:
        print("Error: No tool selected.")
        return
    
    print(f"\n🚀 Initializing AIMEN project with {tool}...")
    
    # Create tool-specific directory
    if tool == "claude":
        setup_claude_code()
    elif tool == "github":
        setup_github_copilot()
    
    # Create .aimen directory and database
    create_aimen_directory()
    
    print(f"\n✅ Project initialized successfully!")
    print(f"📁 .aimen/programs.db created")


def print_aimen_logo():
    """Print AIMEN logo."""
    logo = """
╔══════════════════════════════════════════╗
║                                          ║
║   ███╗   A██I██M██E██N██ ███╗            ║
║   ███║   AI-driven Development   ███║            ║
║   ███║   Workflow System         ███║            ║
║                                          ║
╚══════════════════════════════════════════╝
    """
    print(logo)


def select_tool_interactive() -> str:
    """Interactive tool selection."""
    print("\n🤖 Select AI Tool:")
    print("  1. Claude Code")
    print("  2. GitHub Copilot")
    print()
    
    try:
        while True:
            choice = input("Enter choice (1-2): ").strip()
            if choice == "1":
                return "claude"
            elif choice == "2":
                return "github"
            else:
                print("Invalid choice. Please enter 1 or 2.")
    except EOFError:
        print("\nError: No input provided. Please run interactively.")
        return None


def setup_claude_code():
    """Setup Claude Code directory structure."""
    claude_dir = Path.cwd() / ".claude"
    
    # Create directories
    for subdir in ["agents", "commands", "skills"]:
        (claude_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    # Copy templates
    copy_templates("claude_code", claude_dir)
    
    print("  📁 Created .claude/ directory")
    print("  📁 Created .claude/agents/, .claude/commands/, .claude/skills/")


def setup_github_copilot():
    """Setup GitHub Copilot directory structure."""
    github_dir = Path.cwd() / ".github"
    
    # Create directories
    for subdir in ["agents", "commands", "skills"]:
        (github_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    # Copy templates
    copy_templates("github_copilot", github_dir)
    
    print("  📁 Created .github/ directory")
    print("  📁 Created .github/agents/, .github/commands/, .github/skills/")


def copy_templates(template_name: str, target_dir: Path):
    """Copy templates to target directory."""
    template_base = Path(__file__).parent.parent.parent.parent / "templates" / template_name
    
    if not template_base.exists():
        print(f"  ⚠️  Warning: Template not found: {template_base}")
        return
    
    for subdir in ["agents", "commands", "skills"]:
        src_dir = template_base / subdir
        dst_dir = target_dir / subdir
        
        if src_dir.exists():
            for item in src_dir.iterdir():
                if item.is_file():
                    shutil.copy2(item, dst_dir / item.name)


def create_aimen_directory():
    """Create .aimen directory and initialize database."""
    aimen_dir = Path.cwd() / ".aimen"
    aimen_dir.mkdir(exist_ok=True)
    
    # Initialize database
    init_db()
    
    print("  📁 Created .aimen/ directory")
    print("  💾 Initialized programs.db")
