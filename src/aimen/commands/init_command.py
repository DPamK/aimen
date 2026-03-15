"""AIMEN init command - Initialize a new project."""

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
    
    print(f"\nInitializing AIMEN project with {tool}...")
    
    # Create tool-specific directory
    if tool == "claude":
        setup_claude_code()
    elif tool == "copilot":
        setup_github_copilot()
    else:
        print(f"⚠️  No specific setup for {tool}, creating basic structure.")
        return
    
    # Create .aimen directory and database
    create_aimen_directory()
    
    print(f"Project initialized successfully!")


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
        ("copilot", "GitHub Copilot"),
        ("cursor", "Cursor"),
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
    for subdir in ["agents", "commands", "skills"]:
        (claude_dir / subdir).mkdir(parents=True, exist_ok=True)

    _install_template(claude_dir)
    print(f"✅ Claude Code install complete!")


def setup_github_copilot():
    """Setup GitHub Copilot directory structure."""
    github_dir = Path.cwd() / ".github"
    for subdir in ["agents", "commands", "skills"]:
        (github_dir / subdir).mkdir(parents=True, exist_ok=True)

    _install_template(github_dir, transformers={
        "agents":   lambda f, c: [(f"{Path(f).stem}.agent.md", c)],
        "commands": lambda f, c: [(f"{Path(f).stem}.command.md", c)],
    })
    print(f"✅ GitHub Copilot install complete!")


def _install_template(target_dir: Path, transformers=None):
    """Load template files and write them to target_dir.

    transformers: {section: (filename, content) -> [(new_filename, new_content)]}
    Return [] to skip a file, multiple tuples for one-to-many output.
    """
    template_base = Path(__file__).parent.parent.parent.parent / "template"

    if not template_base.exists():
        print(f"  ⚠️  Warning: Template not found: {template_base}")
        return

    for section in ["agents", "commands"]:
        src_dir = template_base / section
        dst_dir = target_dir / section
        transform = (transformers or {}).get(section, lambda f, c: [(f, c)])
        if src_dir.exists():
            for item in sorted(src_dir.iterdir()):
                if item.is_file():
                    content = item.read_text(encoding="utf-8")
                    for new_filename, new_content in transform(item.name, content):
                        (dst_dir / new_filename).write_text(new_content, encoding="utf-8")

    src_skills = template_base / "skills"
    dst_skills = target_dir / "skills"
    if src_skills.exists():
        for item in sorted(src_skills.iterdir()):
            if item.is_dir():
                shutil.copytree(str(item), dst_skills / item.name, dirs_exist_ok=True)


def create_aimen_directory():
    """Create .aimen directory and initialize database."""
    aimen_dir = Path.cwd() / ".aimen"
    aimen_dir.mkdir(exist_ok=True)
    
    # Initialize database
    init_db()
