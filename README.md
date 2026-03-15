# AIMEN - AI-driven Development Workflow System

## Installation

```bash
# Using uv
uv sync

# Or install in development mode
uv pip install -e .
```

## Usage

### Initialize a project

```bash
aimen init
```

### Project Management

```bash
# Initialize a new project
aimen program init "My Project" -t "Project description"

# Add a requirement
aimen program add <project_id> -n "Feature name" -t "Description" -c "Acceptance criteria"

# View status
aimen status
aimen status <project_id>
aimen status <project_id> <requirement_id>

# Set orchestration
aimen program orch <project_id> "Orchestration text"

# Remove
aimen program remove <project_id>
aimen program remove <project_id> <requirement_id>
```
