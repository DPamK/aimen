# Database Schema

## Tables

### products
```sql
id              INTEGER PRIMARY KEY
name            TEXT NOT NULL
description     TEXT
status          TEXT DEFAULT 'active'
created_at      TIMESTAMP
updated_at      TIMESTAMP
```

### features
```sql
id              INTEGER PRIMARY KEY
product_id      INTEGER NOT NULL
name            TEXT NOT NULL
branch          TEXT UNIQUE
status          TEXT DEFAULT 'planning'
priority        TEXT DEFAULT 'medium'
workflow_stage  TEXT DEFAULT 'specify'
created_at      TIMESTAMP
updated_at      TIMESTAMP
```

### tasks
```sql
id              INTEGER PRIMARY KEY
feature_id      INTEGER NOT NULL
task_id         TEXT NOT NULL
phase           TEXT
description     TEXT NOT NULL
file_path       TEXT
status          TEXT DEFAULT 'todo'
created_at      TIMESTAMP
updated_at      TIMESTAMP
```

### history
```sql
id              INTEGER PRIMARY KEY
entity_type     TEXT NOT NULL
entity_id       INTEGER NOT NULL
action          TEXT NOT NULL
old_value       TEXT
new_value       TEXT
created_at      TIMESTAMP
```

## Relations

```
products (1) ──→ (N) features
features (1) ──→ (N) tasks
```

## Enums

**Product Status**: active, paused, completed  
**Feature Status**: planning, implementing, testing, completed  
**Task Status**: todo, doing, done  
**Workflow Stage**: specify, clarify, plan, tasks, analyze, implement  
**Priority**: low, medium, high
