"""AIMEN init command - Initialize a new project."""

import subprocess
import sys
from pathlib import Path

# Ensure stdout uses UTF-8 on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from ..database import init_db
from .agents import ClaudeInitializer, CodexInitializer, CopilotInitializer, CursorInitializer, OpenCodeInitializer

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
        initialized_files = ClaudeInitializer(mode).setup()
    elif tool == "copilot":
        initialized_files = CopilotInitializer(mode).setup()
    elif tool == "opencode":
        initialized_files = OpenCodeInitializer(mode).setup()
    elif tool == "cursor":
        initialized_files = CursorInitializer(mode).setup()
    elif tool == "codex":
        initialized_files = CodexInitializer(mode).setup()
    else:
        print(f"暂不支持 {tool} 的自动化安装，未来可期！")
        return
    
    # Create .aimen directory and database
    create_aimen_directory()

    gitignore_path = ensure_database_ignored()
    git_initialized = ensure_git_repository()
    if git_initialized:
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
        ("dev",   "Dev   - 完整开发模式"),
        ("quick", "Quick - 极速模式（一次命令，全自动完成）"),
    ]
    return _arrow_select("⚙️  Select Work Mode", options)


def select_tool_interactive(args) -> str:
    """Select AI agent - use args.agent if set, otherwise interactive arrow-key menu."""
    if getattr(args, "agent", None):
        return args.agent

    options = [
        ("claude",   "Claude Code"),
        ("opencode", "OpenCode"),
        ("copilot",  "GitHub Copilot"),
        ("cursor",   "Cursor"),
        ("codex",    "OpenAI Codex"),
        ("gemini",   "Gemini"),
        ("qwen",     "Qwen"),
    ]
    return _arrow_select("🤖 Select AI Agent", options)


def _arrow_select(title: str, options: list) -> str:
    """Display an arrow-key navigable menu and return the selected value."""
    import questionary

    choices = [questionary.Choice(label, value=value) for value, label in options]
    result = questionary.select(title, choices=choices).ask()
    return result  # None if ESC / Ctrl-C






def create_aimen_directory():
    """Create .aimen directory and initialize database."""
    aimen_dir = Path.cwd() / ".aimen"
    aimen_dir.mkdir(exist_ok=True)
    
    # Initialize database
    init_db()


def ensure_database_ignored() -> Path:
    """Ensure the local AIMEN database is ignored by Git."""
    gitignore_path = Path.cwd() / ".gitignore"
    rule = ".aimen/projects.db"

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


def ensure_git_repository() -> bool:
    """Initialize a Git repository when needed and return whether initialization happened."""
    git_dir = Path.cwd() / ".git"
    if git_dir.exists():
        return False

    if _run_git_command("rev-parse", "--is-inside-work-tree", check=False).returncode == 0:
        return False

    result = _run_git_command("init", check=False)
    if result.returncode != 0:
        raise RuntimeError(f"Git repository initialization failed: {result.stderr.strip() or result.stdout.strip()}")

    print("✅ Git repository initialized")
    return True


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
