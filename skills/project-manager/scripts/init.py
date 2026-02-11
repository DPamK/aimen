#!/usr/bin/env python3
"""Initialize the .aimen project management directory."""

import sqlite3
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime


AIMEN_DIR = Path(".aimen")


def get_constitution_template():
    """Return the initial constitution.md template."""
    return """# [PROJECT_NAME] Constitution
<!-- Example: Spec Constitution, TaskFlow Constitution, etc. -->

## Core Principles

### [PRINCIPLE_1_NAME]
<!-- Example: I. Library-First -->
[PRINCIPLE_1_DESCRIPTION]
<!-- Example: Every feature starts as a standalone library; Libraries must be self-contained, independently testable, documented; Clear purpose required - no organizational-only libraries -->

### [PRINCIPLE_2_NAME]
<!-- Example: II. CLI Interface -->
[PRINCIPLE_2_DESCRIPTION]
<!-- Example: Every library exposes functionality via CLI; Text in/out protocol: stdin/args → stdout, errors → stderr; Support JSON + human-readable formats -->

### [PRINCIPLE_3_NAME]
<!-- Example: III. Test-First (NON-NEGOTIABLE) -->
[PRINCIPLE_3_DESCRIPTION]
<!-- Example: TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced -->

### [PRINCIPLE_4_NAME]
<!-- Example: IV. Integration Testing -->
[PRINCIPLE_4_DESCRIPTION]
<!-- Example: Focus areas requiring integration tests: New library contract tests, Contract changes, Inter-service communication, Shared schemas -->

### [PRINCIPLE_5_NAME]
<!-- Example: V. Observability, VI. Versioning & Breaking Changes, VII. Simplicity -->
[PRINCIPLE_5_DESCRIPTION]
<!-- Example: Text I/O ensures debuggability; Structured logging required; Or: MAJOR.MINOR.BUILD format; Or: Start simple, YAGNI principles -->

## [SECTION_2_NAME]
<!-- Example: Additional Constraints, Security Requirements, Performance Standards, etc. -->

[SECTION_2_CONTENT]
<!-- Example: Technology stack requirements, compliance standards, deployment policies, etc. -->

## [SECTION_3_NAME]
<!-- Example: Development Workflow, Review Process, Quality Gates, etc. -->

[SECTION_3_CONTENT]
<!-- Example: Code review requirements, testing gates, deployment approval process, etc. -->

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

[GOVERNANCE_RULES]
<!-- Example: All PRs/reviews must verify compliance; Complexity must be justified; Use [GUIDANCE_FILE] for runtime development guidance -->

**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]
<!-- Example: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->

"""


def get_situation_template():
    """Return the initial situation.md template."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""# AIMEN 工作状态

> 此文件由 AIMEN 管理，记录当前工作上下文与进度。

## 当前执行

- **需求**：(无)
- **功能**：(无)
- **开发任务**：(无)
- **执行状态**：空闲
- **更新时间**：{now}

## 备注

(无)
"""


def init_database(db_path):
    """Create the SQLite database with schema."""
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS requirements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'active',
            priority TEXT DEFAULT 'medium',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            requirement_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            branch TEXT,
            status TEXT DEFAULT 'planning',
            workflow_stage TEXT DEFAULT 'specify',
            priority TEXT DEFAULT 'medium',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (requirement_id) REFERENCES requirements(id)
        );

        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feature_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            file_path TEXT,
            test_file TEXT,
            status TEXT DEFAULT 'todo',
            tdd_stage TEXT DEFAULT NULL,
            priority TEXT DEFAULT 'medium',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (feature_id) REFERENCES features(id)
        );

        CREATE TABLE IF NOT EXISTS changelog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_type TEXT NOT NULL,
            entity_id INTEGER NOT NULL,
            field TEXT NOT NULL,
            old_value TEXT,
            new_value TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()


def init_project(identity_content=None):
    """Initialize the .aimen directory with all required files."""
    # Create .aimen directory
    AIMEN_DIR.mkdir(exist_ok=True)

    results = []

    # Create identity.md
    identity_path = AIMEN_DIR / "identity.md"
    if identity_content:
        identity_path.write_text(identity_content, encoding="utf-8")
        results.append(f"Created {identity_path} with provided identity")
    else:
        if not identity_path.exists():
            identity_path.write_text("# AIMEN Identity\n\n默认模式：高级智能秘书\n", encoding="utf-8")
            results.append(f"Created {identity_path} with default identity")
        else:
            results.append(f"{identity_path} already exists, skipped")

    # Create constitution.md
    constitution_path = AIMEN_DIR / "constitution.md"
    if not constitution_path.exists():
        now = datetime.now().strftime("%Y-%m-%d")
        constitution_content = get_constitution_template().replace("{{DATE}}", now)
        constitution_path.write_text(constitution_content, encoding="utf-8")
        results.append(f"Created {constitution_path}")
    else:
        results.append(f"{constitution_path} already exists, skipped")

    # Create situation.md
    situation_path = AIMEN_DIR / "situation.md"
    if not situation_path.exists():
        situation_path.write_text(get_situation_template(), encoding="utf-8")
        results.append(f"Created {situation_path}")
    else:
        results.append(f"{situation_path} already exists, skipped")

    # Create project.db
    db_path = AIMEN_DIR / "project.db"
    init_database(db_path)
    results.append(f"Initialized database at {db_path}")

    return {
        "success": True,
        "message": "Project initialized successfully",
        "details": results,
        "path": str(AIMEN_DIR.resolve())
    }


def main():
    parser = argparse.ArgumentParser(description="Initialize .aimen project management directory")
    parser.add_argument(
        "--identity", type=str,
        help="Identity content for identity.md. Prefix with @ to read from file (e.g. @path/to/file.md)"
    )

    args = parser.parse_args()

    identity_content = None
    if args.identity:
        if args.identity.startswith("@"):
            file_path = Path(args.identity[1:])
            if file_path.exists():
                identity_content = file_path.read_text(encoding="utf-8")
            else:
                print(json.dumps({"success": False, "error": f"File not found: {file_path}"}, ensure_ascii=False))
                sys.exit(1)
        else:
            identity_content = args.identity

    try:
        result = init_project(identity_content)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
