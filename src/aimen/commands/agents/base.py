"""Base agent initializer class."""

from abc import ABC, abstractmethod
from pathlib import Path

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files  # type: ignore


def _copy_files(src_dir: Path, dst_dir: Path) -> list[Path]:
    """Recursively copy files from src_dir into dst_dir."""
    dst_dir.mkdir(parents=True, exist_ok=True)
    written_files: list[Path] = []
    for item in sorted(src_dir.iterdir()):
        if item.is_file():
            target = dst_dir / item.name
            target.write_text(item.read_text(encoding="utf-8"), encoding="utf-8")
            written_files.append(target)
        elif item.is_dir():
            written_files.extend(_copy_files(item, dst_dir / item.name))
    return written_files


_SECTION_METHODS = {
    "agents":   "setup_agents",
    "commands": "setup_commands",
    "skills":   "setup_skills",
}


class BaseAgentInitializer(ABC):
    """Base class for initializing AI agent environments.

    Subclasses must implement get_target_dir(), and may override any of
    setup_agents(), setup_commands(), or setup_skills() to customize how
    each template section is installed.
    """

    def __init__(self, mode: str = "dev"):
        self.mode = mode

    @abstractmethod
    def get_target_dir(self) -> Path:
        """Return the target root directory for this agent's files."""
        pass

    def get_success_message(self) -> str:
        """Return the success message printed after installation."""
        return "✅ Installation complete!"
    def get_placeholders(self) -> dict[str, str]:
        """Return placeholder substitutions applied to all installed files.

        Keys are placeholder strings in the template (e.g. ``{{QUESTION_TOOL}}``);
        values are the tool-specific replacements.

        Override in subclasses to define tool-specific values.
        """
        return {}

    def _apply_placeholders(self, content: str) -> str:
        """Replace all placeholders in *content* and return the result."""
        for placeholder, value in self.get_placeholders().items():
            content = content.replace(placeholder, value)
        return content

    def _install_files(self, src_dir: Path, dst_dir: Path) -> list[Path]:
        """Recursively copy files from src_dir into dst_dir, applying placeholder substitutions."""
        dst_dir.mkdir(parents=True, exist_ok=True)
        written_files: list[Path] = []
        for item in sorted(src_dir.iterdir()):
            if item.is_file():
                target = dst_dir / item.name
                content = self._apply_placeholders(item.read_text(encoding="utf-8"))
                target.write_text(content, encoding="utf-8")
                written_files.append(target)
            elif item.is_dir():
                written_files.extend(self._install_files(item, dst_dir / item.name))
        return written_files
    # ------------------------------------------------------------------
    # Section methods — override in subclasses to customise behaviour
    # ------------------------------------------------------------------

    def setup_agents(self, src: Path, target: Path) -> list[Path]:
        """Install the agents section.

        Default behaviour: copy files as-is into target/agents/.

        Args:
            src:    Source agents directory from the template.
            target: Target root directory returned by get_target_dir().
        """
        return self._install_files(src, target / "agents")

    def setup_commands(self, src: Path, target: Path) -> list[Path]:
        """Install the commands section.

        Default behaviour: copy files as-is into target/commands/.

        Args:
            src:    Source commands directory from the template.
            target: Target root directory returned by get_target_dir().
        """
        return self._install_files(src, target / "commands")

    def setup_skills(self, src: Path, target: Path) -> list[Path]:
        """Install the skills section.

        Default behaviour: copy files as-is into target/skills/.

        Args:
            src:    Source skills directory from the template.
            target: Target root directory returned by get_target_dir().
        """
        return self._install_files(src, target / "skills")

    # ------------------------------------------------------------------
    # Orchestration
    # ------------------------------------------------------------------

    def setup(self) -> list[Path]:
        """Execute the full agent installation and return all written paths."""
        template_base = self._get_template_path()
        if not template_base.exists():
            print(f"  ⚠️  Warning: Template not found: {template_base}")
            return []

        target_dir = self.get_target_dir()
        written_files: list[Path] = []

        for section_dir in sorted(template_base.iterdir()):
            if not section_dir.is_dir():
                continue
            method_name = _SECTION_METHODS.get(section_dir.name)
            if method_name:
                method = getattr(self, method_name)
                written_files.extend(method(section_dir, target_dir))

        print(self.get_success_message())
        return written_files

    def _get_template_path(self) -> Path:
        """Return the template base directory for the current mode."""
        try:
            template_base = Path(str(files("aimen.template").joinpath(self.mode)))
        except (TypeError, FileNotFoundError):
            from .. import __file__ as init_file
            template_base = Path(init_file).parent.parent / "template" / self.mode
        return template_base
