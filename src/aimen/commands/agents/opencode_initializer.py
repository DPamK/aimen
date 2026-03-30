"""OpenCode agent initializer."""

from pathlib import Path

from .base import BaseAgentInitializer


class OpenCodeInitializer(BaseAgentInitializer):
    """Initializer for OpenCode environment.

    OpenCode uses the same file layout as Claude Code,
    only the target directory differs (.opencode instead of .claude).
    """

    def get_target_dir(self) -> Path:
        return Path.cwd() / ".opencode"

    def get_success_message(self) -> str:
        return "✅ OpenCode install complete!"

    def get_placeholders(self) -> dict[str, str]:
        return {
            "{{QUESTION_TOOL}}": "Question",
        }
