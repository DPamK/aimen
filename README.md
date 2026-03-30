# AIMEN

A self-hosted vibe coding assistant that makes AI-driven development simple and accessible.

## Why AIMEN?

Unlike complex tools like spec-kit, AIMEN is designed with **zero learning curve**. You only need two commands:

- **`cto`** - Architecture design & requirements management
- **`aimen`** - Task execution & development workflow

That's it. No complex configuration, no steep learning curve.

## Features

- **Self-hosted** - Full control over your development environment
- **Multi-agent support** - Supports Claude Code, OpenCode, Cursor, and GitHub Copilot (Gemini & Qwen coming soon)
- **Two modes** - Dev mode (advanced) and Quick mode (simplified workflow)
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

### 1. Initialize Your Project

```bash
aimen init
```

This command sets up the agent directory with all necessary configuration files. You can specify an agent and mode:

```bash
aimen init --agent claude   # Claude Code  → .claude/
aimen init --agent opencode # OpenCode     → .opencode/
aimen init --agent cursor   # Cursor       → .cursor/
aimen init --agent copilot  # GitHub Copilot → .github/
```

> **Note:** Gemini and Qwen support is coming soon.

### 2. Define Requirements with CTO

Use the `cto` command to discuss your feature requirements with an AI architect:

```bash
/cto "I want to build a user authentication system"
```

The CTO agent will:
- Ask clarifying questions about your requirements
- Design the technical architecture
- Create structured Program and Task definitions
- Define acceptance criteria for each task

### 3. Execute Development with AIMEN

Once requirements are defined, use the `aimen` command to start development:

```bash
/aimen
```

The AIMEN agent will:
- Coordinate between specialized sub-agents (developer, tester, debugger)
- Follow TDD principles for implementation
- Run verification scripts automatically
- Update documentation as needed

## Project Management

AIMEN includes built-in project management tools:

```bash
# Create a new program (project)
aimen program init "My Feature" -t "Feature description"

# Add a task to the program
aimen program add P-001 -n "User Login" -t "Implement login" -c "User can log in with valid credentials"

# View all programs and tasks
aimen program status

# View specific program
aimen program status P-001

# Set task orchestration
aimen program orch P-001 "Run tasks in sequence: T-001 -> T-002 -> T-003"

# Update task status
aimen program update T-001 --status "🟢"
```

## Modes

AIMEN supports two workflow modes:

### Dev Mode
- CTO is a **command** (`/cto`)
- You manually invoke CTO for requirements, then `/aimen` for development
- More control over the workflow

### Easy Mode
- CTO is an **agent** under AIMEN's coordination
- AIMEN automatically calls CTO when you have new requirements
- Simplified workflow, less manual switching

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

