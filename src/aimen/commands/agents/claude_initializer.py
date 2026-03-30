"""Claude Code agent initializer."""

from pathlib import Path

from .base import BaseAgentInitializer


class ClaudeInitializer(BaseAgentInitializer):
    """Initializer for Claude Code environment.

    Claude Code stores agents, commands, and skills directly under .claude/
    using the default file layout, so no section overrides are needed.
    """

    def get_target_dir(self) -> Path:
        return Path.cwd() / ".claude"

    def get_success_message(self) -> str:
        return "✅ Claude Code install complete!"

    def get_placeholders(self) -> dict[str, str]:
        return {
            "{{QUESTION_TOOL}}": "Question",
        }
