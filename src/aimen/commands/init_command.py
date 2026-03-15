"""AIMEN init command - Initialize a new project."""

import os
import shutil
from pathlib import Path
from ..database import init_db


def execute(args):
    """Execute the init command."""
    print_aimen_logo()
    
    # Interactive tool selection
    tool = select_tool_interactive(args)
    
    if not tool:
        print("\nCancelled.")
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
    CYAN = "\033[36m"
    YELLOW = "\033[33m"
    RESET = "\033[0m"
    logo = f"""
{CYAN} █████╗ ██╗███╗   ███╗███████╗███╗   ██╗
██╔══██╗██║████╗ ████║██╔════╝████╗  ██║
███████║██║██╔████╔██║█████╗  ██╔██╗ ██║
██╔══██║██║██║╚██╔╝██║██╔══╝  ██║╚██╗██║
██║  ██║██║██║ ╚═╝ ██║███████╗██║ ╚████║
╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝{RESET}
{YELLOW}      AI-driven Development Workflow{RESET}
"""
    print(logo)


def select_tool_interactive(args) -> str:
    """Select AI agent - use args.agent if set, otherwise interactive arrow-key menu."""
    if getattr(args, "agent", None):
        return args.agent

    options = [
        ("claude", "Claude Code"),
        ("cursor", "Cursor"),
        ("github-copilot", "GitHub Copilot"),
        ("gemini", "Gemini"),
        ("qwen", "Qwen"),
    ]
    return _arrow_select("🤖 Select AI Agent", options)


def _arrow_select(title: str, options: list) -> str:
    """Display an arrow-key navigable menu and return the selected value."""
    import questionary

    choices = [questionary.Choice(label, value=value) for value, label in options]
    result = questionary.select(title, choices=choices).ask()
    return result  # None if ESC / Ctrl-C



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
