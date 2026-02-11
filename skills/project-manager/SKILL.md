```skill
---
name: project-manager
description: AIMEN 项目管理技能包，用于初始化项目环境（.aimen 目录）、管理工作状态和项目数据库。
---

# Project Manager Skill

管理 `.aimen/` 目录下的项目状态，包括身份文件、宪法、工作状态和项目数据库。

## 目录结构

初始化后将在项目根目录创建：

```
.aimen/
 identity.md       # AIMEN 身份设定
 constitution.md   # 项目开发宪法（核心原则与规范）
 situation.md      # 当前工作状态（AIMEN 自管理）
 project.db        # 项目管理数据库（SQLite）
```

## 核心概念

**三层管理结构**：
- **Requirement（需求）**：最高层级，如"用户管理系统"
- **Feature（功能）**：中间层级，如"用户注册"、"密码重置"
- **Task（任务）**：最小执行单元，遵循 TDD 流程开发

**TDD 任务生命周期**：
每个 Task 必须遵循 TDD 流程，状态流转如下：
```
todo  write_test  red  green  refactor  done
```
- **todo**：待开始
- **write_test**：编写测试用例
- **red**：运行测试，确认测试失败（红灯）
- **green**：编写最小化实现代码，使测试通过（绿灯）
- **refactor**：重构优化代码，保持测试通过
- **done**：任务完成，所有测试通过
- **blocked**：被阻塞，需要等待外部依赖
- **cancelled**：已取消

**状态文件**：
- **situation.md**：AIMEN 的工作记忆，记录当前正在做什么（由脚本或 AIMEN 直接维护）
- **project.db**：结构化的项目数据，用 SQL 管理所有需求/功能/任务

## 可用脚本

所有脚本位于 `skills/project-manager/scripts/`，**从项目根目录执行**。输出均为 JSON 格式。

---

### 1. 初始化  `init.py`

首次使用时初始化 `.aimen/` 目录，创建 identity.md、constitution.md、situation.md、project.db。

```bash
# 默认初始化（身份文件使用默认模板）
python skills/project-manager/scripts/init.py

# 指定身份内容（直接传入文本）
python skills/project-manager/scripts/init.py --identity "你是一个猫娘女仆，性格温柔可爱..."

# 从文件读取身份内容（@ 前缀）
python skills/project-manager/scripts/init.py --identity @path/to/identity_content.md
```

**说明**：
- 如果 `.aimen/` 已存在，不会覆盖已有的 situation.md 和 constitution.md
- identity.md 始终会被更新为传入的内容
- project.db 会执行 schema 创建（IF NOT EXISTS，安全幂等）
- constitution.md 提供默认的 TDD + SDD 规范模板，可根据项目需要修改

---

### 2. 工作状态管理  `situation.py`

管理 `.aimen/situation.md`，记录 AIMEN 当前工作上下文。

```bash
# 查看当前状态
python skills/project-manager/scripts/situation.py show

# 更新状态（可只更新部分字段，未指定的字段保持不变）
python skills/project-manager/scripts/situation.py update \
  --requirement "用户管理系统" \
  --feature "用户注册功能" \
  --task "实现注册表单验证" \
  --status "green - 编写实现代码" \
  --note "测试已编写并确认失败，开始实现"

# 只更新任务和状态
python skills/project-manager/scripts/situation.py update --task "编写单元测试" --status "write_test"

# 重置为空闲状态
python skills/project-manager/scripts/situation.py clear
```

> **注意**：AIMEN 也可以直接编辑 `.aimen/situation.md` 文件，无需通过脚本。脚本的优势是保持格式规范。

---

### 3. 数据库操作  `db.py`

直接执行 SQL 操作 `.aimen/project.db`。AIMEN 自行编写 SQL，无需复杂的 CLI 封装。

```bash
# 查询数据
python skills/project-manager/scripts/db.py exec \
  --sql "SELECT * FROM requirements"

# 参数化插入（防注入）
python skills/project-manager/scripts/db.py exec \
  --sql "INSERT INTO requirements(name, description, priority) VALUES(?, ?, ?)" \
  --params '["用户管理系统", "用户注册登录权限管理", "high"]'

# 更新数据
python skills/project-manager/scripts/db.py exec \
  --sql "UPDATE tasks SET status='done', completed_at=CURRENT_TIMESTAMP WHERE id=?" \
  --params '[1]'

# 执行多条 SQL（脚本模式，用分号分隔）
python skills/project-manager/scripts/db.py script --sql "
  UPDATE tasks SET status='done', completed_at=CURRENT_TIMESTAMP WHERE id=1;
  INSERT INTO changelog(entity_type, entity_id, field, old_value, new_value) VALUES('task', 1, 'status', 'refactor', 'done');
"

# 查看数据库 schema
python skills/project-manager/scripts/db.py schema
```

---

### 4. 实用查询  `query.py`

常用查询的快捷封装，避免每次手写 SQL。

```bash
# 查看当前正在执行的工作（TDD 进行中的任务 + 活跃功能）
python skills/project-manager/scripts/query.py current

# 查看待执行的任务（todo 状态，按优先级排序，默认 10 条）
python skills/project-manager/scripts/query.py pending --limit 5

# 查看最近完成的任务（默认 10 条）
python skills/project-manager/scripts/query.py completed --limit 5

# 项目总览统计（需求/功能/任务各状态计数 + 最近变更记录）
python skills/project-manager/scripts/query.py overview
```

---

## 数据库结构

### requirements（需求）

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| id | INTEGER | 自增主键 | |
| name | TEXT |  | 需求名称（必填） |
| description | TEXT | NULL | 需求描述 |
| status | TEXT | 'active' | active / paused / completed / archived |
| priority | TEXT | 'medium' | low / medium / high / critical |
| created_at | TIMESTAMP | 当前时间 | 创建时间 |
| updated_at | TIMESTAMP | 当前时间 | 更新时间 |

### features（功能）

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| id | INTEGER | 自增主键 | |
| requirement_id | INTEGER |  | 关联需求 ID（必填，外键） |
| name | TEXT |  | 功能名称（必填） |
| description | TEXT | NULL | 功能描述 |
| branch | TEXT | NULL | Git 分支名 |
| status | TEXT | 'planning' | planning / implementing / testing / completed / paused |
| workflow_stage | TEXT | 'specify' | SDD 阶段：specify / clarify / plan / tasks / analyze / implement |
| priority | TEXT | 'medium' | low / medium / high / critical |
| created_at | TIMESTAMP | 当前时间 | 创建时间 |
| updated_at | TIMESTAMP | 当前时间 | 更新时间 |

### tasks（任务） TDD 驱动

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| id | INTEGER | 自增主键 | |
| feature_id | INTEGER |  | 关联功能 ID（必填，外键） |
| title | TEXT |  | 任务标题（必填） |
| description | TEXT | NULL | 任务详细描述 |
| file_path | TEXT | NULL | 实现文件路径 |
| test_file | TEXT | NULL | 测试文件路径 |
| status | TEXT | 'todo' | TDD 状态：todo / write_test / red / green / refactor / done / blocked / cancelled |
| tdd_stage | TEXT | NULL | 可选的 TDD 阶段备注（如失败原因、重构要点等） |
| priority | TEXT | 'medium' | low / medium / high / critical |
| created_at | TIMESTAMP | 当前时间 | 创建时间 |
| updated_at | TIMESTAMP | 当前时间 | 更新时间 |
| completed_at | TIMESTAMP | NULL | 完成时间（status 变为 done 时设置） |

### changelog（变更日志）

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| id | INTEGER | 自增主键 | |
| entity_type | TEXT |  | requirement / feature / task |
| entity_id | INTEGER |  | 对应实体的 ID |
| field | TEXT |  | 变更的字段名 |
| old_value | TEXT | NULL | 旧值 |
| new_value | TEXT |  | 新值 |
| created_at | TIMESTAMP | 当前时间 | 变更时间 |

---

## TDD 任务操作 SQL 示例

### 创建任务
```sql
INSERT INTO tasks(feature_id, title, description, file_path, test_file, priority)
VALUES(1, '用户注册验证', '实现注册表单的前端校验逻辑', 'src/components/RegisterForm.vue', 'tests/RegisterForm.test.ts', 'high');
```

### TDD 流转：开始编写测试
```sql
UPDATE tasks SET status='write_test', updated_at=CURRENT_TIMESTAMP WHERE id=1;
```

### TDD 流转：确认测试失败（Red）
```sql
UPDATE tasks SET status='red', tdd_stage='测试编写完成，3个测试用例均失败', updated_at=CURRENT_TIMESTAMP WHERE id=1;
```

### TDD 流转：实现代码使测试通过（Green）
```sql
UPDATE tasks SET status='green', tdd_stage='所有3个测试用例通过', updated_at=CURRENT_TIMESTAMP WHERE id=1;
```

### TDD 流转：重构优化（Refactor）
```sql
UPDATE tasks SET status='refactor', tdd_stage='提取公共验证函数', updated_at=CURRENT_TIMESTAMP WHERE id=1;
```

### TDD 流转：完成任务（Done）
```sql
UPDATE tasks SET status='done', tdd_stage=NULL, completed_at=CURRENT_TIMESTAMP, updated_at=CURRENT_TIMESTAMP WHERE id=1;
```

### 记录状态变更日志
```sql
INSERT INTO changelog(entity_type, entity_id, field, old_value, new_value)
VALUES('task', 1, 'status', 'red', 'green');
```

---

## 其他常用 SQL 示例

### 创建需求
```sql
INSERT INTO requirements(name, description, priority)
VALUES('用户管理系统', '用户注册、登录、权限管理', 'high');
```

### 创建功能
```sql
INSERT INTO features(requirement_id, name, description, branch)
VALUES(1, '用户注册', '实现完整的用户注册流程', '001-user-register');
```

### 推进功能工作流阶段
```sql
UPDATE features SET workflow_stage='implement', status='implementing', updated_at=CURRENT_TIMESTAMP WHERE id=1;
```

### 查询某功能下所有任务（含 TDD 状态）
```sql
SELECT t.id, t.title, t.status, t.tdd_stage, t.priority, t.file_path, t.test_file
FROM tasks t WHERE t.feature_id = 1 ORDER BY t.id;
```

### 查询项目整体进度
```sql
SELECT r.name AS requirement, f.name AS feature, f.workflow_stage,
       COUNT(CASE WHEN t.status='done' THEN 1 END) AS done,
       COUNT(CASE WHEN t.status IN ('write_test','red','green','refactor') THEN 1 END) AS doing,
       COUNT(CASE WHEN t.status='todo' THEN 1 END) AS todo,
       COUNT(t.id) AS total
FROM requirements r
JOIN features f ON f.requirement_id = r.id
LEFT JOIN tasks t ON t.feature_id = f.id
GROUP BY r.id, f.id;
```

### 最近变更历史
```sql
SELECT c.*,
  CASE c.entity_type
    WHEN 'requirement' THEN (SELECT name FROM requirements WHERE id=c.entity_id)
    WHEN 'feature' THEN (SELECT name FROM features WHERE id=c.entity_id)
    WHEN 'task' THEN (SELECT title FROM tasks WHERE id=c.entity_id)
  END AS entity_name
FROM changelog c ORDER BY c.created_at DESC LIMIT 20;
```

---

## 使用模式

### 新项目初始化
1. 执行 `init.py --identity "..."` 创建 `.aimen/` 目录（含 constitution.md）
2. 根据需要修改 `.aimen/constitution.md` 调整项目规范
3. 用 `db.py` 创建第一个 requirement
4. 用 `situation.py update` 记录当前工作上下文

### 开始新需求
1. `db.py exec` 插入 requirement  feature  tasks（指定 file_path 和 test_file）
2. `situation.py update` 更新当前工作状态
3. 按 SDD 流程推进 workflow_stage

### TDD 开发单个任务
1. `status  write_test`：编写测试文件
2. `status  red`：运行测试，确认全部失败
3. `status  green`：编写实现代码，使测试通过
4. `status  refactor`：重构优化，保持测试通过
5. `status  done`：标记完成
6. 每次状态变更都应写入 changelog 和更新 situation.md

### 继续工作（恢复上下文）
1. 读取 `.aimen/situation.md` 了解上次工作进度
2. `query.py current` 查看数据库中 TDD 进行中的任务
3. 根据当前 TDD 阶段继续执行

### 项目回顾
1. `query.py overview` 查看整体统计
2. `query.py completed` 查看最近完成的工作

---

## 重要约定

1. **所有脚本输出 JSON 格式**，便于 AIMEN 解析
2. **数据库操作通过 `db.py`**，AIMEN 自行编写 SQL，灵活高效
3. **situation.md 是工作记忆**，每次任务切换 / TDD 阶段变更时应更新
4. **Task 必须遵循 TDD 流程**：write_test  red  green  refactor  done
5. **建议写入 changelog**，便于追踪变更历史
6. **从项目根目录执行**所有脚本命令
```
