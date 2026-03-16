"""AIMEN init command - Initialize a new project."""

import shutil
from pathlib import Path
from typing import Callable
from ..database import init_db


# SectionHandler: (src_section_dir, tool_root_dir) -> None
SectionHandler = Callable[[Path, Path], None]


# ---------------------------------------------------------------------------
# Shared helper
# ---------------------------------------------------------------------------

def _copy_section(src_dir: Path, dst_dir: Path) -> None:
    """Copy files and subdirs from src_dir into dst_dir (default behaviour)."""
    dst_dir.mkdir(parents=True, exist_ok=True)
    for item in sorted(src_dir.iterdir()):
        if item.is_file():
            (dst_dir / item.name).write_text(item.read_text(encoding="utf-8"), encoding="utf-8")
        elif item.is_dir():
            shutil.copytree(item, dst_dir / item.name, dirs_exist_ok=True)


# ---------------------------------------------------------------------------
# GitHub Copilot handlers
# ---------------------------------------------------------------------------

def _copilot_agents(src: Path, root: Path) -> None:
    dst = root / "agents"
    dst.mkdir(parents=True, exist_ok=True)
    for f in sorted(src.iterdir()):
        if f.is_file():
            (dst / f"{f.stem}.agent.md").write_text(f.read_text(encoding="utf-8"), encoding="utf-8")


def _copilot_commands(src: Path, root: Path) -> None:
    dst = root / "prompts"
    dst.mkdir(parents=True, exist_ok=True)
    for f in sorted(src.iterdir()):
        if f.is_file():
            (dst / f"{f.stem}.prompt.md").write_text(f.read_text(encoding="utf-8"), encoding="utf-8")


_COPILOT_HANDLERS: dict[str, SectionHandler] = {
    "agents":   _copilot_agents,
    "commands": _copilot_commands,
}

# ---------------------------------------------------------------------------


def execute(args):
    """Execute the init command."""
    print_aimen_logo()
    
    # Interactive mode selection
    mode = select_mode_interactive(args)

    if not mode:
        print("\nCancelled.")
        return

    # Interactive tool selection
    tool = select_tool_interactive(args)

    if not tool:
        print("\nCancelled.")
        return

    print(f"\nInitializing AIMEN project with {tool} ({mode} mode)...")

    # Create tool-specific directory
    if tool == "claude":
        setup_claude_code(mode)
    elif tool == "copilot":
        setup_github_copilot(mode)
    else:
        print(f"暂不支持 {tool} 的自动化安装，未来可期！")
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


def select_mode_interactive(args) -> str:
    """Select work mode - use args.mode if set, otherwise interactive arrow-key menu."""
    if getattr(args, "mode", None):
        return args.mode

    options = [
        ("dev",  "Dev  - 完整开发模式"),
        ("easy", "Easy - 简易模式"),
    ]
    return _arrow_select("⚙️  Select Work Mode", options)


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



def setup_claude_code(mode: str = "dev"):
    """Setup Claude Code directory structure."""
    _install_template(Path.cwd() / ".claude", mode, {})
    print("✅ Claude Code install complete!")


def setup_github_copilot(mode: str = "dev"):
    """Setup GitHub Copilot directory structure."""
    _install_template(Path.cwd() / ".github", mode, _COPILOT_HANDLERS)
    print("✅ GitHub Copilot install complete!")


def _install_template(target_dir: Path, mode: str, handlers: dict[str, SectionHandler]) -> None:
    """Traverse template/<mode>/ and dispatch each section dir to its handler.

    For each section directory found in the template:
      - If a handler is registered for that section name, call it.
      - Otherwise fall back to _copy_section (copies as-is into target_dir/<section>).

    handler signature: (src_section_dir: Path, tool_root_dir: Path) -> None
    """
    template_base = Path(__file__).parent.parent.parent.parent / "template" / mode
    if not template_base.exists():
        print(f"  ⚠️  Warning: Template not found: {template_base}")
        return

    for section_dir in sorted(template_base.iterdir()):
        if not section_dir.is_dir():
            continue
        handler = handlers.get(section_dir.name, lambda s, t: _copy_section(s, t / s.name))
        handler(section_dir, target_dir)




def create_aimen_directory():
    """Create .aimen directory and initialize database."""
    aimen_dir = Path.cwd() / ".aimen"
    aimen_dir.mkdir(exist_ok=True)
    
    # Initialize database
    init_db()
