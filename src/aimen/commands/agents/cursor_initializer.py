"""Cursor agent initializer."""

from pathlib import Path

from .base import BaseAgentInitializer


class CursorInitializer(BaseAgentInitializer):
    """Initializer for Cursor environment.

    Cursor uses the same file layout as Claude Code,
    only the target directory differs (.cursor instead of .claude).
    """

    def get_target_dir(self) -> Path:
        return Path.cwd() / ".cursor"

    def get_success_message(self) -> str:
        return "✅ Cursor install complete!"
