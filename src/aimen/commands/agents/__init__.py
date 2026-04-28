"""Agent initializers for AIMEN."""

from .base import BaseAgentInitializer, _copy_files
from .claude_initializer import ClaudeInitializer
from .codex_initializer import CodexInitializer
from .copilot_initializer import CopilotInitializer
from .cursor_initializer import CursorInitializer
from .opencode_initializer import OpenCodeInitializer

__all__ = [
    "BaseAgentInitializer",
    "ClaudeInitializer",
    "CodexInitializer",
    "CopilotInitializer",
    "CursorInitializer",
    "OpenCodeInitializer",
    "_copy_files",
]
