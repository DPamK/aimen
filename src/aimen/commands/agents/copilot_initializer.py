"""GitHub Copilot agent initializer."""

from pathlib import Path

from .base import BaseAgentInitializer


class CopilotInitializer(BaseAgentInitializer):
    """Initializer for GitHub Copilot environment.

    GitHub Copilot requires specific file naming conventions:
    - agents:   xxx.md → .github/agents/xxx.agent.md
    - commands: xxx.md → .github/prompts/xxx.prompt.md  (directory also renamed)
    - skills:   copied as-is into .github/skills/ (default behaviour)
    """

    def get_target_dir(self) -> Path:
        return Path.cwd() / ".github"

    def get_success_message(self) -> str:
        return "✅ GitHub Copilot install complete!"

    def get_placeholders(self) -> dict[str, str]:
        return {
            "{{QUESTION_TOOL}}": "vscode_askQuestions",
        }

    def setup_agents(self, src: Path, target: Path) -> list[Path]:
        """Install agents, renaming each file to <stem>.agent.md."""
        dst = target / "agents"
        dst.mkdir(parents=True, exist_ok=True)
        written_files: list[Path] = []
        for f in sorted(src.iterdir()):
            if f.is_file():
                out = dst / f"{f.stem}.agent.md"
                out.write_text(self._apply_placeholders(f.read_text(encoding="utf-8")), encoding="utf-8")
                written_files.append(out)
        return written_files

    def setup_commands(self, src: Path, target: Path) -> list[Path]:
        """Install commands into prompts/, renaming each file to <stem>.prompt.md."""
        dst = target / "prompts"
        dst.mkdir(parents=True, exist_ok=True)
        written_files: list[Path] = []
        for f in sorted(src.iterdir()):
            if f.is_file():
                out = dst / f"{f.stem}.prompt.md"
                out.write_text(self._apply_placeholders(f.read_text(encoding="utf-8")), encoding="utf-8")
                written_files.append(out)
        return written_files
