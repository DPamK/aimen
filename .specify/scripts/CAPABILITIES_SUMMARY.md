# 合并后 project-manager 的完整能力体系

## 概览

当 `.specify/scripts/bash` 合并到 `project-manager` 技能后，系统将从**纯数据库驱动**演进为**文件系统 + 数据库双驱动**，形成一个完整的**特性全生命周期管理平台**。

---

## 第一部分：核心能力（3 大支柱）

### 1️⃣ Git 分支与文件系统管理

#### 1.1 智能特性分支创建
```bash
# 命令
project-manager feature create \
  "Add user authentication system" \
  --product-id 1 \
  --priority high

# 自动执行：
✓ 生成分支名：001-user-authentication
✓ 创建 git 分支（git checkout -b 001-user-authentication）
✓ 创建目录：specs/001-user-authentication/
✓ 生成 spec.md（从模板）
✓ 在数据库创建特性记录（feature_id=10）
✓ 返回完整信息：
  {
    "feature_id": 10,
    "branch": "001-user-authentication",
    "spec_file": "specs/001-user-authentication/spec.md",
    "status": "planning",
    "environment": "SPECIFY_FEATURE=001-user-authentication"
  }
```

#### 1.2 分支命名智能化
- ✓ 停用词过滤（the, a, to, for 等）
- ✓ GitHub 244 字节限制检查和自动截断
- ✓ 大写转小写、特殊字符规范化
- ✓ 自定义命名支持（`--short-name "custom-name"`）

#### 1.3 特性目录结构管理
```
自动创建的目录结构：
specs/001-feature/
├── spec.md              # 特性规范（必需）
├── plan.md              # 实现计划（必需）
├── tasks.md             # 任务列表（自动生成）
├── research.md          # 调研文档（可选）
├── data-model.md        # 数据模型（可选）
├── quickstart.md        # 快速指南（可选）
└── contracts/           # API 契约（可选）

所有文件从模板生成，自动填充项目名称、日期等
```

#### 1.4 多分支支持
```bash
# 场景：两个开发者分别处理同一特性的不同部分
分支 A：001-auth-backend
分支 B：001-auth-frontend

特性 ID：001（共享）

智能管理：
- 汇总两个分支的进度
- 两个分支共享同一个特性记录
- 但保持独立的任务列表
- 合并时自动检测和警告
```

---

### 2️⃣ 文档和元数据管理

#### 2.1 Plan.md 自动解析和同步
```bash
# plan.md 中的元数据示例
**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, SQLAlchemy
**Storage**: PostgreSQL
**Project Type**: Web Backend

# 自动执行：
✓ 解析提取四个关键字段
✓ 同步到数据库 features 表：
  {
    "language": "Python 3.11",
    "framework": "FastAPI, SQLAlchemy",
    "storage": "PostgreSQL",
    "project_type": "Web Backend"
  }
✓ 生成技术栈摘要：
  "Python 3.11 + FastAPI, SQLAlchemy (DB: PostgreSQL)"
```

#### 2.2 Tasks.md 自动解析和同步
```bash
# tasks.md 中的任务格式
## Phase 1: Setup
- [ ] T001: 创建数据库 schema
- [ ] T002: 实现用户模型

## Phase 2: Implementation
- [ ] T003: 实现登录端点
- [ ] T004: 实现注册端点

# 自动执行：
✓ 扫描 tasks.md 中的所有任务
✓ 自动创建数据库任务记录（如不存在）
✓ 关联 phase 信息
✓ 基于 checkbox 状态更新任务状态：
  [ ] → todo
  [x] → done
✓ 每次脚本运行自动同步差异

# 查询能力
project-manager task list --feature-id 10 --phase "Phase 1"
project-manager task list --feature-id 10 --status doing
```

#### 2.3 研究文档追踪
```bash
# 前置检查能力
project-manager validate --feature-id 10

检查项：
✓ spec.md 存在且非空
✓ plan.md 存在且包含必需字段
✓ tasks.md 存在（如果特性在实现阶段）
✓ 可选文档存在检查：
  - research.md（调研）
  - data-model.md（数据设计）
  - contracts/ （API 定义）
  - quickstart.md（快速指南）

输出报告：
{
  "feature_id": 10,
  "completeness": 85,  # 百分比
  "missing": ["research.md", "contracts/"],
  "warnings": ["data-model.md 应该在实现前准备"],
  "ready_for_next_phase": true
}
```

---

### 3️⃣ 多代理上下文管理

#### 3.1 支持的代理类型（17 种）
```
AI 代理类型：
- Claude Code (CLAUDE.md)
- GitHub Copilot (.github/agents/copilot-instructions.md)
- Cursor IDE (.cursor/rules/specify-rules.mdc)
- Windsurf (.windsurf/rules/specify-rules.md)
- Amazon Q Developer CLI (AGENTS.md)
- And 12 others...

特点：
✓ 自动检测代理文件位置
✓ 支持两种格式：
  - 单一 .md 文件（根目录）
  - 目录结构（.github/agents/, .cursor/ 等）
✓ 智能创建或更新，防止重复
```

#### 3.2 自动生成代理配置内容
```bash
# 基于 plan.md 自动生成配置

[PROJECT NAME]
aimen

[TECHNOLOGY STACK]
- Python 3.11 + FastAPI, SQLAlchemy (DB: PostgreSQL)

[RECENT CHANGES]
- 001-user-authentication: Added Python 3.11 + FastAPI, SQLAlchemy

[PROJECT STRUCTURE]
backend/
frontend/
tests/

[BUILD/TEST COMMANDS]
cd src && pytest && ruff check .

[LANGUAGE CONVENTIONS]
Python 3.11: Follow standard conventions

[Last updated]
2024-02-09

# 特点：
✓ 每个字段都是智能生成的
✓ 基于 plan.md 的元数据自动适配
✓ 支持多语言和框架（Python、JavaScript、Rust 等）
✓ 自动保持最近 3 个特性的更新日志
```

#### 3.3 多代理同步
```bash
# 一条命令，同步所有代理
project-manager agent update-all

执行流程：
1. 解析当前特性的 plan.md
2. 查找所有已配置的代理文件
3. 对每个代理执行：
   ✓ 检查代理文件是否存在
   ✓ 如不存在，从模板创建
   ✓ 如存在，智能更新：
     - 添加新技术栈（去重）
     - 更新最近变更（保留最新 3 条）
     - 更新时间戳
4. 返回同步报告

输出示例：
{
  "agents_updated": 5,
  "agents_created": 0,
  "details": {
    "CLAUDE.md": "updated",
    "GEMINI.md": "updated",
    ".github/agents/copilot-instructions.md": "updated",
    ".cursor/rules/specify-rules.mdc": "updated",
    "QWEN.md": "updated"
  },
  "timestamp": "2024-02-09T10:30:00Z"
}
```

#### 3.4 代理配置查询
```bash
# 查看当前代理配置状态
project-manager agent status

输出：
Configured Agents (5):
  ✓ CLAUDE.md
  ✓ GEMINI.md
  ✓ .github/agents/copilot-instructions.md
  ✓ .cursor/rules/specify-rules.mdc
  ✓ QWEN.md

Last Updated: 2024-02-09 10:30:00
Technology Stack:
  - Python 3.11 + FastAPI, SQLAlchemy (DB: PostgreSQL)

Recent Changes:
  - 001-user-authentication: Added Python 3.11
  - 002-auth-frontend: Added React 18
  - 003-payment-api: Added Stripe integration
```

---

## 第二部分：工作流自动化（6 大场景）

### 场景 1：新特性开发启动

```bash
# 一步启动，自动完成所有初始化
project-manager feature start \
  "Implement OAuth2 integration" \
  --product-id 1 \
  --priority high

# 自动执行的 14 个步骤：
1. ✓ 检查 git 状态
2. ✓ 生成分支名（004-oauth2-integration）
3. ✓ 查询最高特性编号
4. ✓ 创建 git 分支
5. ✓ 创建 specs/004-oauth2-integration/ 目录
6. ✓ 从模板生成 spec.md
7. ✓ 从模板生成 plan.md
8. ✓ 在数据库创建特性记录
9. ✓ 在数据库创建产品关联
10. ✓ 创建历史审计记录
11. ✓ 设置环境变量 SPECIFY_FEATURE
12. ✓ 生成 .editorconfig 提示文件
13. ✓ 输出下一步指引
14. ✓ 可选：打开 VS Code 编辑 plan.md

# 返回值：
{
  "success": true,
  "feature_id": 15,
  "branch": "004-oauth2-integration",
  "spec_file": "specs/004-oauth2-integration/spec.md",
  "plan_file": "specs/004-oauth2-integration/plan.md",
  "next_steps": [
    "Edit spec.md to describe the feature",
    "Edit plan.md to detail the implementation",
    "Run: project-manager plan save",
    "Run: project-manager validate --feature 15"
  ]
}
```

### 场景 2：计划编写后的自动化处理

```bash
# 编写完 plan.md 后
project-manager plan save

# 自动执行：
1. ✓ 解析 plan.md 中的元数据
2. ✓ 验证必需字段完整
3. ✓ 同步到数据库（language, framework, storage, project_type）
4. ✓ 生成技术栈摘要
5. ✓ 更新所有代理配置
6. ✓ 创建 tasks.md 初始模板（如不存在）
7. ✓ 记录审计日志
8. ✓ 检查与其他特性的技术冲突
9. ✓ 输出完成报告

# 报告示例：
✓ Plan saved successfully
✓ Parsed metadata:
  - Language: Python 3.11
  - Framework: FastAPI
  - Storage: PostgreSQL
  - Type: Web Backend
✓ Updated 5 AI agents
✓ Ready for task planning phase

Next: 
  1. Create tasks.md (or let's do it for you with --auto-tasks)
  2. Run: project-manager validate
```

### 场景 3：任务列表创建和追踪

```bash
# 自动从 plan.md 生成 tasks.md 初始结构
project-manager task init --feature-id 15

# 自动执行：
1. ✓ 分析 plan.md 的实现阶段
2. ✓ 推荐任务列表（基于特性类型）
3. ✓ 生成 tasks.md 初始框架
4. ✓ 在数据库创建任务记录
5. ✓ 输出任务创建报告

# 生成的 tasks.md 结构：
## Phase 1: Setup & Environment
- [ ] T001: Set up OAuth2 provider account
- [ ] T002: Create environment configuration

## Phase 2: Backend Implementation  
- [ ] T003: Create OAuth2 service module
- [ ] T004: Implement authorization flow
- [ ] T005: Add token refresh logic

## Phase 3: Frontend Integration
- [ ] T006: Create login component
- [ ] T007: Add authentication state management

## Phase 4: Testing & Deployment
- [ ] T008: Write unit tests
- [ ] T009: Deploy to staging

# 然后手动编辑和运行
project-manager task sync

执行同步：
✓ 扫描 tasks.md 中的所有任务
✓ 更新数据库中的任务状态
✓ 检查新增任务并创建记录
✓ 同步完成
```

### 场景 4：阶段完成检查

```bash
# 规划阶段完成，准备进入实现阶段
project-manager feature advance \
  --feature-id 15 \
  --next-stage implementation

# 自动执行检查：
1. ✓ 验证 spec.md 完整（不能为空）
2. ✓ 验证 plan.md 完整（必需字段齐全）
3. ✓ 验证 tasks.md 存在
4. ✓ 警告检查：
   ⚠ research.md 未创建，建议补充
   ⚠ data-model.md 未创建，建议补充
5. ✓ 执行阶段转换：
   - 更新 db: workflow_stage = 'implementing'
   - 生成状态转换记录
   - 发送通知（可选）

# 失败示例（缺少必需内容）：
✗ Cannot advance to implementation
  Missing: plan.md must contain "Language/Version"
  Missing: plan.md must contain "Primary Dependencies"
  
  Guidance:
    1. Edit specs/004-oauth2-integration/plan.md
    2. Add required fields
    3. Run: project-manager plan save
    4. Try again: project-manager feature advance
```

### 场景 5：特性完成和归档

```bash
# 特性开发完成
project-manager feature complete --feature-id 15

# 自动执行：
1. ✓ 标记所有任务为 done
2. ✓ 更新 db: status = 'completed', completed_at = now()
3. ✓ 生成完成报告：
   - 总耗时
   - 完成的任务数
   - 代码行数变化（可选）
   - 功能贡献摘要
4. ✓ 可选：创建发布笔记
5. ✓ 可选：自动合并到 main（带确认）
6. ✓ 记录最终审计日志

# 完成报告示例：
Feature Completed: 004-oauth2-integration
├── Duration: 14 days
├── Tasks: 9/9 completed
├── Code Changes:
│   ├── Files: +42, -8
│   ├── Lines: +1200, -150
│   └── Commits: 23
├── Documentation:
│   ├── spec.md: ✓
│   ├── plan.md: ✓
│   ├── tasks.md: ✓
│   ├── research.md: ✗
│   └── quickstart.md: ✓
└── Agents Updated: 5 ✓
```

### 场景 6：多特性并行管理

```bash
# 查看所有活跃特性的状态
project-manager status --mode detailed

输出：
Active Features (3):
1. [001-user-authentication] Planning
   ├── Branch: 001-user-auth-backend
   ├── Plan Status: 70% complete
   ├── Tasks: 2/9 done
   ├── Docs: spec.md ✓, plan.md ✓, tasks.md ✓
   ├── Agents: 5 updated (2024-02-09)
   └── Next: Complete plan → setup tasks

2. [002-auth-frontend] Implementing  
   ├── Branch: 002-auth-frontend
   ├── Plan Status: Complete ✓
   ├── Tasks: 5/7 doing
   ├── Docs: spec.md ✓, plan.md ✓, tasks.md ✓, research.md ✓
   ├── Agents: 5 updated (2024-02-08)
   └── Current: Implementing auth UI

3. [003-payment-api] Testing
   ├── Branch: 003-payment-integration
   ├── Plan Status: Complete ✓
   ├── Tasks: 8/8 done
   ├── Docs: All complete ✓
   ├── Agents: 5 updated (2024-02-07)
   └── Next: Deploy to production

Summary:
✓ 2/3 on track
⚠ 001 in planning phase (monitor)
✓ Tech diversity: Python + JavaScript + Rust
```

---

## 第三部分：数据分析和报告（10 大报告类型）

### 报告 1：工作流进度分析

```bash
project-manager report workflow

输出：
WORKFLOW STAGE ANALYSIS
========================
Planning:    2 features (avg 5 days)
Implementing: 1 feature (avg 8 days)
Testing:     1 feature (avg 3 days)
Completed:   12 features (avg 10 days)

Timeline Visualization:
[████░░░░] Planning (40% features)
[██░░░░░░] Implementing (20% features)
[███░░░░░] Testing (20% features)
[██████░░] Completed (40% features)

Bottlenecks:
⚠ Implementing stage takes longest (avg 8 days)
  - Consider parallelization
  - Increase testing early
```

### 报告 2：技术栈分布

```bash
project-manager report tech-stack

输出：
TECHNOLOGY STACK DISTRIBUTION
=============================
Languages:
  Python:     60% (6 features)
  JavaScript: 30% (3 features)
  Rust:       10% (1 feature)

Frameworks:
  FastAPI:    40% (4 features)
  React:      30% (3 features)
  Django:     20% (2 features)
  Actix:      10% (1 feature)

Databases:
  PostgreSQL: 70% (7 features)
  MongoDB:    20% (2 features)
  Redis:      10% (1 feature)

Project Types:
  Web Backend:   50% (5 features)
  Web Frontend:  30% (3 features)
  Data Pipeline: 20% (2 features)
```

### 报告 3：文档完整性检查

```bash
project-manager report documentation

输出：
DOCUMENTATION COMPLETENESS
===========================
Overall Coverage: 78%

Required (必需):
  spec.md:       100% ✓ (10/10 features)
  plan.md:       100% ✓ (10/10 features)

Implementation Phase (实现阶段):
  tasks.md:      95% ⚠ (9/10 features)
  Missing: 002-payment-api

Optional (可选):
  research.md:   60% (6/10 features)
  data-model.md: 50% (5/10 features)
  contracts/:    40% (4/10 features)
  quickstart.md: 30% (3/10 features)

Recommendations:
  1. Add research.md to 4 remaining features
  2. Add data-model.md to 5 features
  3. Create API contracts for 6 features
```

### 报告 4：代理配置覆盖度

```bash
project-manager report agent-coverage

输出：
AI AGENT CONFIGURATION STATUS
=============================
Configured Agents: 5/17

Configured:
  ✓ CLAUDE.md (updated 2024-02-09)
  ✓ GEMINI.md (updated 2024-02-09)
  ✓ .github/agents/copilot-instructions.md (updated 2024-02-08)
  ✓ .cursor/rules/specify-rules.mdc (updated 2024-02-08)
  ✓ QWEN.md (updated 2024-02-09)

Not Configured:
  ✗ Windsurf
  ✗ Amazon Q Developer CLI
  ✗ Kilo Code
  ... (11 more)

Coverage by Technology:
  Python 3.11:        100% agents updated
  FastAPI:            100% agents updated
  React:              80% agents updated
  PostgreSQL:         100% agents updated

Last Sync Report:
  Date: 2024-02-09 10:30:00
  Duration: 2.3 seconds
  Changes: 3 agents updated
```

### 报告 5：完成率趋势

```bash
project-manager report completion-trend --period 30d

输出：
FEATURE COMPLETION TREND (Last 30 Days)
=======================================
Total Features Started: 15
Total Completed: 12
Completion Rate: 80%

Weekly Breakdown:
Week 1: 2/4 completed (50%)
Week 2: 3/4 completed (75%)
Week 3: 4/4 completed (100%)
Week 4: 3/3 completed (100%)

Average Time to Completion: 9.2 days

Trend:
[###░░░░░░] Week 1
[#####░░░░] Week 2
[########░] Week 3
[#########] Week 4

Forecast (Next 30 days):
  Expected Completions: 18-22 features
  Based on current velocity
```

### 报告 6：风险识别

```bash
project-manager report risks

输出：
RISK ANALYSIS
==============
High Priority Warnings:

🔴 HIGH: Feature stuck in planning
  - 001-user-authentication
  - Duration: 18 days (avg: 5 days)
  - Status: 70% plan completion
  - Recommendation: Review plan blocking issues

🟠 MEDIUM: Missing critical documentation
  - 002-auth-frontend
  - Missing: research.md, data-model.md
  - Impact: May delay implementation
  - Recommendation: Complete documentation this week

🟠 MEDIUM: Technology inconsistency
  - 003-payment-api
  - Uses: Python + Node.js mixed
  - Impact: Deployment complexity
  - Recommendation: Consolidate stack

🟡 LOW: Agent configuration outdated
  - Last updated: 2024-02-07 (2 days ago)
  - Agents: 3/5 using outdated specs
  - Impact: Reduced AI assistance accuracy
```

### 报告 7：团队活动日志

```bash
project-manager report activity --feature-id 15 --period 7d

输出：
FEATURE ACTIVITY LOG (Last 7 Days)
==================================
Feature: 004-oauth2-integration

2024-02-09 10:30:00 - plan saved
  └─ Updated metadata: Language, Framework, Storage
  └─ Triggered agent context update (5 agents)

2024-02-09 09:15:00 - task sync
  └─ Updated 3 tasks from tasks.md
  └─ Status changes: 1 todo→doing, 2 done updates

2024-02-08 15:45:00 - workflow stage advanced
  └─ Transitioned: planning → implementing
  └─ Validation checks: all passed ✓

2024-02-08 14:20:00 - feature created
  └─ Branch: 004-oauth2-integration
  └─ Initial docs created

Activity Summary:
  - 4 major milestones
  - 2 documents updated
  - 3 agent configs updated
  - 0 issues/risks
```

### 报告 8：代码变更统计

```bash
project-manager report code-changes --feature-id 15

输出：
CODE CHANGE ANALYSIS - 004-oauth2-integration
==============================================
Total Commits: 23
Date Range: 2024-01-26 to 2024-02-09 (14 days)

Changes by Type:
  Implementation: 18 commits (78%)
  Testing: 3 commits (13%)
  Documentation: 2 commits (9%)

Files Statistics:
  Added: 12 files (+1,200 lines)
  Modified: 8 files (+400 lines, -150 lines)
  Deleted: 2 files (-80 lines)

Language Distribution:
  Python: 70% (+840 lines)
  JavaScript: 20% (+320 lines)
  SQL: 10% (+40 lines)

Velocity:
  Avg Lines/Day: 86 lines
  Avg Commits/Day: 1.6 commits
  Trend: Accelerating ↗
```

### 报告 9：文档和代码对齐

```bash
project-manager report alignment --feature-id 15

输出：
DOCUMENTATION-CODE ALIGNMENT CHECK
===================================
Feature: 004-oauth2-integration

spec.md vs Implementation:
  ✓ All requirements implemented
  ✓ No extra features added
  ✓ No missing features
  Alignment: 100%

plan.md vs Code:
  ✓ Scheduled milestones met
  ✓ No major deviations
  ⚠ Task 5 (token refresh) took 2 days longer
  Alignment: 95%

tasks.md vs Commits:
  ✓ 9/9 tasks completed
  ✓ Code changes match task descriptions
  ✓ Test coverage in place
  Alignment: 100%

README/Documentation:
  ⚠ quickstart.md not updated with new endpoints
  ⚠ API docs partially outdated
  Alignment: 70%

Recommendations:
  1. Update quickstart.md with OAuth2 flow examples
  2. Update API documentation
  3. Consider adding troubleshooting section
```

### 报告 10：版本发布清单

```bash
project-manager report release-checklist --feature-id 15

输出：
RELEASE CHECKLIST - 004-oauth2-integration v1.0
===============================================

Pre-Release Checks:
  ✓ All tests passing (45/45)
  ✓ Code review approved (2 approvals)
  ✓ Documentation complete
  ✓ Deployment tested on staging
  ✓ Performance benchmarks acceptable

Documentation:
  ✓ spec.md: Complete and accurate
  ✓ plan.md: All tasks completed
  ✓ tasks.md: 100% completion
  ✓ quickstart.md: Updated
  ✓ API contracts: In contracts/ folder
  ⚠ Breaking changes list: Pending

Code Quality:
  ✓ Coverage: 92% (threshold: 80%)
  ✓ Linting: All passed
  ✓ Type checking: All passed
  ⚠ Security scan: 1 low-priority issue

AI Agent Readiness:
  ✓ All 5 agents updated
  ✓ Tech stack documented
  ✓ Build commands verified

Ready to Release: YES ✓
  └─ Deploy to production: project-manager deploy --feature 15
  └─ Tag version: v1.0 (auto-generate)
  └─ Create release notes: (auto-generate from activity log)
```

---

## 第四部分：集成能力（与其他系统的协作）

### 集成 1：版本控制系统

```bash
# 自动和 git hooks 集成
.git/hooks/post-commit:
  ✓ 自动扫描 spec.md 变更
  ✓ 自动同步到数据库
  ✓ 自动检查分支命名规范

# 自动和 GitHub Actions 集成
.github/workflows/feature-sync.yml:
  ✓ 创建 PR 时自动更新特性状态
  ✓ 合并 PR 时自动标记任务完成
  ✓ 关闭分支时自动更新代理

# 自动和 pull request 集成
PR 标题自动识别特性：
  "feat: 004-oauth2-integration - add token refresh"
  └─ 自动关联 feature_id: 004
  └─ 自动更新特性进度
  └─ 自动检查所需文档是否完整
```

### 集成 2：CI/CD 流程

```bash
# 触发自动部署前的检查
Before Deployment:
  1. project-manager validate --feature-id 15 --strict
  2. project-manager report alignment
  3. project-manager report risks

# 部署完成后自动更新
After Deployment:
  1. 标记特性为 "deployed"
  2. 生成部署报告
  3. 更新代理配置（"Latest: 004 deployed to production"）
```

### 集成 3：代码审查系统

```bash
# 代码审查时自动检查
Code Review Automation:
  ✓ 验证提交是否在当前特性分支
  ✓ 检查 plan.md 中的实现计划
  ✓ 检查任务完成度
  ✓ 自动生成变更摘要

# 审查评论中自动添加链接
Comment: "This handles task T003 from plan.md"
  └─ 自动添加链接到 plan.md 中的 T003 部分
```

### 集成 4：沟通平台

```bash
# 与 Slack/Teams 集成
Notifications:
  ✓ 特性完成时通知
  ✓ 特性卡住超过 N 天时告警
  ✓ 文档缺失时提醒
  ✓ 代理配置过期时提示

# 自动生成报告链接
Daily Summary Report:
  "3 features completed, 5 in progress, 1 at risk"
  └─ 报告详情: project-manager report daily
```

### 集成 5：项目管理工具

```bash
# 与 Jira/Linear 同步
Bi-directional Sync:
  ✓ 特性创建时自动创建 Issue
  ✓ Issue 更新时同步到 project-manager
  ✓ 任务完成时更新 Issue 状态
  ✓ Jira Epic ← → project-manager Product
```

---

## 第五部分：扩展能力（未来可能性）

### 1. 智能助手
```bash
# AI 驱动的自动化
project-manager ai generate-plan --feature-id 15
  └─ 基于 spec.md 自动生成 plan.md 框架

project-manager ai generate-tasks --feature-id 15
  └─ 基于 plan.md 自动生成 tasks.md

project-manager ai review --feature-id 15
  └─ AI 审查文档完整性和一致性
```

### 2. 时间追踪
```bash
# 自动从 git commits 计算
Time Tracking:
  ✓ 每个任务的实际耗时
  ✓ 计划 vs 实际对比
  ✓ 成员效率分析
  ✓ 改进建议
```

### 3. 团队协作
```bash
# 团队成员管理
project-manager team add --member "alice@example.com"
  ✓ 自动在 CODEOWNERS 中设置
  ✓ 自动配置权限
  ✓ 自动通知

# 代码所有权管理
CODEOWNERS 自动生成，基于特性和成员关联
```

### 4. 知识库
```bash
# 自动从完成的特性中提取知识
project-manager knowledge extract --feature-id 15
  ✓ 提取最佳实践
  ✓ 提取常见问题
  ✓ 提取优化建议
  ✓ 构建可搜索的知识库
```

### 5. 模板和工作流
```bash
# 创建特性类型模板
project-manager template create "web-api"
  ✓ 预定义的文件结构
  ✓ 预定义的任务列表
  ✓ 预定义的检查清单

# 使用模板快速启动
project-manager feature create "..." --template "web-api"
  └─ 自动生成符合模板的所有文件
```

---

## 总结：能力等级

| 等级 | 能力 | 复杂度 | 当前 | 合并后 |
|-----|------|-------|------|-------|
| L1 | 产品 CRUD | ★☆☆☆☆ | ✓ | ✓ |
| L1 | 特性 CRUD | ★★☆☆☆ | ✓ | ✓✓ |
| L1 | 任务 CRUD | ★★☆☆☆ | ✓ | ✓✓ |
| L2 | Git 分支管理 | ★★★☆☆ | ✗ | ✓ |
| L2 | 文件系统管理 | ★★★☆☆ | ✗ | ✓ |
| L2 | 元数据解析 | ★★★☆☆ | ✗ | ✓ |
| L2 | 代理配置 | ★★★★☆ | ✗ | ✓ |
| L3 | 工作流自动化 | ★★★★☆ | 部分 | ✓✓ |
| L3 | 数据分析报告 | ★★★★☆ | ✗ | ✓ |
| L3 | 风险识别 | ★★★★☆ | ✗ | ✓ |
| L4 | 多系统集成 | ★★★★★ | ✗ | ✓ |
| L5 | AI 驱动功能 | ★★★★★ | ✗ | 预留 |

**结论**：合并后，project-manager 将从纯数据库系统升级为全能的**特性生命周期管理平台**，获得 15+ 项新能力。

