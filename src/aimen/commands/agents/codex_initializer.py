"""OpenAI Codex agent initializer."""

from pathlib import Path

from .base import BaseAgentInitializer


class CodexInitializer(BaseAgentInitializer):
    """Initializer for OpenAI Codex.

    Codex uses project instructions from AGENTS.md, custom subagents from
    .codex/agents/*.toml, and skills from .agents/skills/*/SKILL.md.
    """

    def get_target_dir(self) -> Path:
        return Path.cwd()

    def get_success_message(self) -> str:
        return "鉁?Codex install complete!"

    def get_placeholders(self) -> dict[str, str]:
        return {
            "{{QUESTION_TOOL}}": "ask the user in the current Codex thread",
        }

    def setup_agents(self, src: Path, target: Path) -> list[Path]:
        """Install template agents as Codex subagent TOML files."""
        dst = target / ".codex" / "agents"
        dst.mkdir(parents=True, exist_ok=True)

        written_files: list[Path] = []
        for f in sorted(src.iterdir()):
            if not f.is_file():
                continue

            metadata, body = self._split_frontmatter(
                self._apply_placeholders(f.read_text(encoding="utf-8"))
            )
            name = metadata.get("name", f.stem)
            description = metadata.get("description", f.stem)

            out = dst / f"{f.stem}.toml"
            out.write_text(
                "\n".join(
                    [
                        f'name = "{self._toml_escape(name)}"',
                        f'description = "{self._toml_escape(description)}"',
                        'developer_instructions = """',
                        body.replace('"""', '\\"\\"\\"').rstrip(),
                        '"""',
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            written_files.append(out)

        return written_files

    def setup_commands(self, src: Path, target: Path) -> list[Path]:
        """Install template commands as Codex skills."""
        dst = target / ".agents" / "skills"
        written_files: list[Path] = []

        for f in sorted(src.iterdir()):
            if not f.is_file():
                continue

            metadata, body = self._split_frontmatter(
                self._apply_placeholders(f.read_text(encoding="utf-8"))
            )
            name = metadata.get("name", f.stem)
            description = metadata.get("description", f.stem)

            skill_dir = dst / f.stem
            skill_dir.mkdir(parents=True, exist_ok=True)
            out = skill_dir / "SKILL.md"
            out.write_text(
                "\n".join(
                    [
                        "---",
                        f"name: {name}",
                        f"description: {description}",
                        "---",
                        "",
                        body.lstrip(),
                    ]
                ),
                encoding="utf-8",
            )
            written_files.append(out)

        return written_files

    def setup_skills(self, src: Path, target: Path) -> list[Path]:
        return self._install_files(src, target / ".agents" / "skills")

    def _split_frontmatter(self, content: str) -> tuple[dict[str, str], str]:
        normalized = content.replace("\r\n", "\n")
        if not normalized.startswith("---\n"):
            return {}, content

        try:
            _, frontmatter, body = normalized.split("---", 2)
        except ValueError:
            return {}, content

        metadata: dict[str, str] = {}
        for line in frontmatter.splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip().strip('"').strip("'")

        return metadata, body.lstrip()

    def _toml_escape(self, value: str) -> str:
        return value.replace("\\", "\\\\").replace('"', '\\"')
