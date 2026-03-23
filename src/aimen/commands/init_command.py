"""AIMEN init command - Initialize a new project."""

import subprocess
import sys
from pathlib import Path
from typing import Callable

# Ensure stdout uses UTF-8 on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files  # type: ignore

from ..database import init_db


# SectionHandler: (src_section_dir, tool_root_dir) -> list[Path]
SectionHandler = Callable[[Path, Path], list[Path]]


# ---------------------------------------------------------------------------
# Shared helper
# ---------------------------------------------------------------------------

def _copy_section(src_dir: Path, dst_dir: Path) -> list[Path]:
    """Copy files and subdirs from src_dir into dst_dir (default behaviour)."""
    dst_dir.mkdir(parents=True, exist_ok=True)
    written_files: list[Path] = []
    for item in sorted(src_dir.iterdir()):
        if item.is_file():
            target = dst_dir / item.name
            target.write_text(item.read_text(encoding="utf-8"), encoding="utf-8")
            written_files.append(target)
        elif item.is_dir():
            written_files.extend(_copy_section(item, dst_dir / item.name))
    return written_files


# ---------------------------------------------------------------------------
# GitHub Copilot handlers
# ---------------------------------------------------------------------------

def _copilot_agents(src: Path, root: Path) -> list[Path]:
    dst = root / "agents"
    dst.mkdir(parents=True, exist_ok=True)
    written_files: list[Path] = []
    for f in sorted(src.iterdir()):
        if f.is_file():
            target = dst / f"{f.stem}.agent.md"
            target.write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
            written_files.append(target)
    return written_files


def _copilot_commands(src: Path, root: Path) -> list[Path]:
    dst = root / "prompts"
    dst.mkdir(parents=True, exist_ok=True)
    written_files: list[Path] = []
    for f in sorted(src.iterdir()):
        if f.is_file():
            target = dst / f"{f.stem}.prompt.md"
            target.write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
            written_files.append(target)
    return written_files


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
    initialized_files: list[Path] = []
    if tool == "claude":
        initialized_files = setup_claude_code(mode)
    elif tool == "copilot":
        initialized_files = setup_github_copilot(mode)
    else:
        print(f"暂不支持 {tool} 的自动化安装，未来可期！")
        return
    
    # Create .aimen directory and database
    create_aimen_directory()

    gitignore_path = ensure_database_ignored()
    ensure_git_repository()
    commit_initialized_files(initialized_files + [gitignore_path])
    
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



def setup_claude_code(mode: str = "dev") -> list[Path]:
    """Setup Claude Code directory structure."""
    written_files = _install_template(Path.cwd() / ".claude", mode, {})
    print("✅ Claude Code install complete!")
    return written_files


def setup_github_copilot(mode: str = "dev") -> list[Path]:
    """Setup GitHub Copilot directory structure."""
    written_files = _install_template(Path.cwd() / ".github", mode, _COPILOT_HANDLERS)
    print("✅ GitHub Copilot install complete!")
    return written_files


def _install_template(target_dir: Path, mode: str, handlers: dict[str, SectionHandler]) -> list[Path]:
    """Traverse template/<mode>/ and dispatch each section dir to its handler.

    For each section directory found in the template:
      - If a handler is registered for that section name, call it.
      - Otherwise fall back to _copy_section (copies as-is into target_dir/<section>).

    handler signature: (src_section_dir: Path, tool_root_dir: Path) -> list[Path]
    """
    try:
        template_base = Path(str(files("aimen.template").joinpath(mode)))
    except (TypeError, FileNotFoundError):
        template_base = Path(__file__).parent.parent / "template" / mode

    if not template_base.exists():
        print(f"  ⚠️  Warning: Template not found: {template_base}")
        return []

    written_files: list[Path] = []
    for section_dir in sorted(template_base.iterdir()):
        if not section_dir.is_dir():
            continue
        handler = handlers.get(section_dir.name, lambda s, t: _copy_section(s, t / s.name))
        written_files.extend(handler(section_dir, target_dir))

    return written_files




def create_aimen_directory():
    """Create .aimen directory and initialize database."""
    aimen_dir = Path.cwd() / ".aimen"
    aimen_dir.mkdir(exist_ok=True)
    
    # Initialize database
    init_db()


def ensure_database_ignored() -> Path:
    """Ensure the local AIMEN database is ignored by Git."""
    gitignore_path = Path.cwd() / ".gitignore"
    rule = ".aimen/programs.db"

    if gitignore_path.exists():
        content = gitignore_path.read_text(encoding="utf-8")
    else:
        content = ""

    existing_rules = {line.strip() for line in content.splitlines() if line.strip()}
    if rule in existing_rules:
        return gitignore_path

    lines: list[str] = []
    if content:
        lines.append(content.rstrip("\n"))
        lines.append("")
    lines.append("# AIMEN")
    lines.append(rule)
    gitignore_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("✅ Added .aimen/programs.db to .gitignore")
    return gitignore_path


def ensure_git_repository() -> None:
    """Initialize a Git repository when the current project is not already tracked."""
    git_dir = Path.cwd() / ".git"
    if git_dir.exists():
        return

    if _run_git_command("rev-parse", "--is-inside-work-tree", check=False).returncode == 0:
        return

    result = _run_git_command("init", check=False)
    if result.returncode != 0:
        raise RuntimeError(f"Git repository initialization failed: {result.stderr.strip() or result.stdout.strip()}")

    print("✅ Git repository initialized")


def commit_initialized_files(paths: list[Path]) -> None:
    """Commit only the files created or updated by the init command."""
    existing_paths = [str(path) for path in dict.fromkeys(path.resolve() for path in paths) if path.exists()]
    if not existing_paths:
        return

    add_result = _run_git_command("add", "--", *existing_paths, check=False)
    if add_result.returncode != 0:
        raise RuntimeError(f"Failed to stage initialized files: {add_result.stderr.strip() or add_result.stdout.strip()}")

    diff_result = _run_git_command("diff", "--cached", "--quiet", check=False)
    if diff_result.returncode == 0:
        print("ℹ️  No new initialization changes to commit")
        return

    if diff_result.returncode not in {0, 1}:
        raise RuntimeError(f"Unable to inspect staged changes: {diff_result.stderr.strip() or diff_result.stdout.strip()}")

    commit_result = _run_git_command("commit", "-m", "Initialize AIMEN project", check=False)
    if commit_result.returncode != 0:
        message = commit_result.stderr.strip() or commit_result.stdout.strip()
        raise RuntimeError(f"Failed to create initial commit: {message}")

    print("✅ Initialization files committed")


def _run_git_command(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Run a Git command in the current working directory."""
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=Path.cwd(),
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=check,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("Git is not installed or not available in PATH") from exc
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() or exc.stdout.strip() or "Unknown git error"
        raise RuntimeError(message) from exc

    return result
