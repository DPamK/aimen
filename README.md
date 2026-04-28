# AIMEN

A self-hosted vibe coding assistant that makes AI-driven development simple and accessible.

## Why AIMEN?

Unlike complex tools like spec-kit, AIMEN is designed with **zero learning curve**. You only need two commands:

- **`cto`** - Architecture design & requirements management
- **`aimen`** - Task execution & development workflow

That's it. No complex configuration, no steep learning curve.

## Features

- **Self-hosted** - Full control over your development environment
- **Multi-agent support** - Supports Claude Code, OpenCode, Cursor, GitHub Copilot, and OpenAI Codex (Gemini & Qwen coming soon)
- **Two modes** - Dev mode (full workflow) and Quick mode (rapid MVP)
- **YOLO mode** - Fully automatic execution, no step-by-step confirmation
- **TDD workflow** - Built-in test-driven development process
- **Smart task management** - Automatic project and task tracking
- **Interactive development** - AI agents communicate with you through guided questions

## Installation

```bash
# Install as a global tool
uv tool install git+https://github.com/DPamK/aimen.git

# Or clone and install locally
git clone https://github.com/DPamK/aimen.git
cd aimen
uv tool install .
```

## Quick Start

### Initialize Your Project

```bash
aimen init
```

This command sets up the agent directory with all necessary configuration files. You can specify an agent and mode:

```bash
aimen init --agent claude   # Claude Code    → .claude/
aimen init --agent opencode # OpenCode       → .opencode/
aimen init --agent cursor   # Cursor         → .cursor/
aimen init --agent copilot  # GitHub Copilot → .github/
aimen init --agent codex    # OpenAI Codex   → AGENTS.md, .codex/, .agents/
```

```bash
aimen init --mode dev    # Dev mode (default)
aimen init --mode quick  # Quick mode
```

> **Note:** Gemini and Qwen support is coming soon.

### Generated Agent Files

AIMEN installs a project-level instruction file from the template `AGENTS.md` and adapts it to each agent tool:

| Agent | Project instructions | Agents | Commands / Skills |
|-------|----------------------|--------|-------------------|
| Claude Code | `CLAUDE.md` | `.claude/agents/` | `.claude/commands/` |
| OpenCode | `AGENTS.md` | `.opencode/agents/` | `.opencode/commands/` |
| Cursor | `AGENTS.md` | `.cursor/agents/` | `.cursor/commands/` |
| GitHub Copilot | `.github/copilot-instructions.md` | `.github/agents/*.agent.md` | `.github/prompts/*.prompt.md` |
| OpenAI Codex | `AGENTS.md` | `.codex/agents/*.toml` | `.agents/skills/*/SKILL.md` |

## Modes

AIMEN provides two workflow modes to suit different use cases:

### Dev Mode
Full development workflow designed for production-quality features.
- Separate `/cto` and `/aimen` commands give you full control over each phase
- CTO handles requirements design; AIMEN coordinates developer, tester, and debugger agents
- Follows strict TDD principles throughout

### Quick Mode
Streamlined workflow for rapidly building an MVP.
- CTO is integrated as an agent under AIMEN’s coordination
- AIMEN automatically invokes CTO when requirements are needed
- Fewer manual steps, faster iteration

### YOLO Mode
Both Dev and Quick modes support **YOLO mode** — fully automatic, no-confirmation execution.
When YOLO is enabled, AIMEN runs the entire workflow end-to-end without pausing for your approval at each step. Choose this when you want maximum speed and trust the agent to handle everything autonomously.

## Development Workflow

AIMEN follows a structured development process:

1. **CTO Phase** - Requirements gathering and architecture design
2. **Development Phase** - TDD-based implementation by developer agent
3. **Testing Phase** - Verification scripts by tester agent
4. **Debug Phase** - Bug fixes by debugger agent (if needed)
5. **Documentation** - Automatic documentation updates

## Agent Roles

| Agent | Role |
|-------|------|
| **CTO** | Architecture design, requirements analysis, task breakdown |
| **AIMEN** | Main coordinator, manages workflow and communication |
| **Developer** | Writes code following TDD principles |
| **Tester** | Creates verification scripts |
| **Debugger** | Fixes bugs and handles failures |

## Directory Structure

```
.aimen/
├── consituation.md    # Project context and configuration
├── memory.md          # Development memory and key notes
├── identity.md        # User identity preferences
├── notebook_CTO.md    # CTO's working notes
└── verify/            # Verification scripts
    └── verify_*.py
```
