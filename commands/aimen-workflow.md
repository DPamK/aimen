---
description: AIMEN工作流协调器 - 管理整个项目开发生命周期，调用sub agents完成各阶段工作
---

# AIMEN Workflow Orchestrator

## 概述

这是AIMEN工作流系统的主协调器。它：
1. 检查项目的当前开发阶段
2. 提供用户选择下一步操作
3. 调用相应的sub agent完成工作
4. 更新工作流状态
5. 引导用户完整项目生命周期

## 工作流状态

工作流状态保存在 `aimen/workflow-state.md` 中，包含：
- 当前项目
- 已完成阶段
- 当前阶段
- 下一个建议操作

## 快速开始

```
/aimen-workflow [项目名称]
```

示例：
```
/aimen-workflow 创建用户认证系统
/aimen-workflow 实现支付处理
```

## 主工作流

### 初始化阶段

**用户输入**: 项目名称或需求描述

**Agent对话**:
```
👋 欢迎使用AIMEN工作流系统

您想做什么？

(A) 创建新的项目治理宪法
(B) 添加新功能到现有项目
(C) 继续现有项目的开发

请选择: _
```

### 分支1: 创建新项目

如果用户选择 (A) - 创建新项目：

```
📋 现在我们来建立您的项目治理宪法

这个宪法将定义您的项目原则和开发规范。

请描述您的项目原则:
(示例: "测试优先、代码简洁、文档完整")

→ 调用 agent-constitution.md
```

**成功后**:
```
✓ 宪法已创建: constitution.md v1.0.0

下一步?

(A) 添加新功能
(B) 查看宪法详情
(C) 修改宪法

请选择: _
```

### 分支2: 添加新功能

无论从哪来，最终都会到功能添加流程：

```
✨ 让我们开始添加新功能

请描述您想要实现的功能:
(示例: "我想添加用户认证")

→ 调用 agent-specify.md
```

**成功后**:
```
✓ 功能规范已创建: specs/001-user-auth/spec.md

规范摘要:
- 用户故事数: 3
- 澄清需求: 0

下一步?

(A) 澄清规范细节 (推荐: 如有澄清需求)
(B) 直接进行技术规划
(C) 修改规范

请选择: _
```

### 澄清阶段 (可选)

```
❓ 我有一些问题需要澄清

Q1: API应该是REST还是GraphQL?
  (A) REST
  (B) GraphQL

请选择: _
```

**对每个问题**:
1. 显示问题和选项
2. 等待用户回答
3. 编码答案到规范
4. 继续下一个问题

**完成后**:
```
✓ 澄清完成

下一步?
(A) 进行技术规划
(B) 再次查看规范

请选择: _
```

### 规划阶段

```
📐 开始技术规划

我将执行:
- Phase 0: 研究和技术选择验证
- Phase 1: 设计数据模型和API合约

这可能需要一些时间...

→ 调用 agent-plan.md
```

**进度示例**:
```
⏳ Phase 0: 研究...
   ✓ 研究技术选择 (JavaScript, Node.js, Express)
   ✓ 研究认证模式 (JWT推荐)

⏳ Phase 1: 设计...
   ✓ 生成数据模型: data-model.md
   ✓ 生成API合约: contracts/user-api.yaml
   ✓ 生成快速启动: quickstart.md

✓ 规划完成
```

**成功后**:
```
✓ 技术规划完成

生成的文件:
- specs/001-user-auth/research.md
- specs/001-user-auth/data-model.md
- specs/001-user-auth/contracts/
- specs/001-user-auth/quickstart.md

下一步?

(A) 分解为可执行任务
(B) 验证一致性 (推荐)
(C) 查看设计详情

请选择: _
```

### 分析阶段 (可选)

```
🔍 执行交叉工件分析

检查 spec → plan → tasks 的一致性...

→ 调用 agent-analyze.md
```

**结果示例**:
```
分析报告:
- CRITICAL issues: 0
- HIGH issues: 1
  - Spec中"快速"未量化
    建议: 添加"<100ms p95"
- MEDIUM issues: 2
- LOW issues: 0

建议: 修复HIGH问题后继续
```

**根据结果**:
- 有CRITICAL → 返回修改 → 重新分析
- 有HIGH → 决定修复或接受风险 → 继续
- 仅MEDIUM/LOW → 安全继续实现

### 任务分解阶段

```
🎯 分解为可执行任务

生成 tasks.md:
- Phase 1: Setup (5 tasks)
- Phase 2: Foundation (6 tasks)
- Phase 3: User Story 1 (8 tasks)
- Phase 4: Polish (4 tasks)

总计: 23 个任务

→ 调用 agent-tasks.md
```

**成功后**:
```
✓ 任务分解完成

tasks.md 已生成: specs/001-user-auth/tasks.md

任务统计:
- 总数: 23
- 可并行: 12
- 按优先级排序: ✓

建议MVP范围:
- Phase 1 + Phase 2 + Phase 3 (User Story 1)
- 工作量: ~X天

下一步?

(A) 开始实现
(B) 创建质量检查清单
(C) 再次查看任务

请选择: _
```

### 质量检查清单 (可选)

```
✅ 创建需求质量检查清单

您想检查什么方面?

(A) 用户体验 (UX) 需求质量
(B) API设计 需求质量
(C) 安全性 需求质量
(D) 所有方面 (综合清单)

请选择: _
```

**生成检查清单**:
```
✓ 清单生成: checklists/ux.md

包含项目:
- 需求完整性: 12 items
- 需求清晰性: 8 items
- 需求一致性: 6 items

使用清单验证规范质量，然后返回继续实现。
```

### 实现阶段

```
⚙️ 开始实现

我将按顺序执行所有任务:

Phase 1: Setup
→ 调用 agent-implement.md (T001-T005)

Phase 2: Foundation
→ 调用 agent-implement.md (T010-T015)

Phase 3: User Story 1
→ 调用 agent-implement.md (T020-T027)

Phase 4: Polish
→ 调用 agent-implement.md (T100-T104)

这可能需要一些时间，取决于复杂性...
```

**实时进度**:
```
⏱️ Phase 1: Setup (5/5 tasks)
   ✓ T001 Create project structure
   ✓ T002 Initialize npm
   ✓ T003 Configure testing
   ✓ T004 Setup CI/CD
   ✓ T005 Create README

⏱️ Phase 2: Foundation (6/6 tasks)
   ✓ T010 Create database schema
   ✓ T011 Create base models
   ✓ T012 Implement authentication
   ✓ T013 Create API infrastructure
   ✓ T014 Configure logging
   ✓ T015 Add validation

⏱️ Phase 3: User Story 1 (8/8 tasks)
   [继续...]

进度: 19/23 (82%)
```

**完成**:
```
🎉 实现完成!

✓ 所有23个任务已完成
✓ .gitignore 已创建
✓ .dockerignore 已创建
✓ 代码结构符合规划

生成的文件:
- src/ directory (完整的源代码)
- tests/ directory (单元和集成测试)
- .gitignore, .dockerignore
- docs/ (API文档)

下一步?

(A) 创建Git提交并推送
(B) 运行本地测试
(C) 部署到测试环境
(D) 查看实现摘要

请选择: _
```

## 状态管理

### 工作流状态文件格式

`aimen/workflow-state.md`:

```yaml
---
project_name: "用户认证系统"
branch: "001-user-auth"
feature_dir: "/path/to/specs/001-user-auth"
started_at: "2025-02-05T10:30:00Z"
---

## 当前进度

### 已完成阶段
- ✓ Constitution (v1.0.0)
- ✓ Specification (spec.md)
- ✓ Planning (plan.md, design files)
- ✓ Tasking (tasks.md)

### 当前阶段
- ⏳ Analyzing
  - 初始化: 完成
  - 检测通过: 进行中
  - 生成报告: 待做

### 下一步
- (A) 完成分析
- (B) 开始实现
- (C) 修改规范/规划

## 配置

- 项目类型: Node.js
- 技术栈: Express, PostgreSQL, Jest
- 宪法版本: 1.0.0
```

### 状态更新

每个agent完成时：
1. 更新已完成阶段
2. 更新当前阶段状态
3. 更新下一步建议

## 关键决策树

### "现在应该做什么?"

```
当前有规范? 
├─ NO → suggest: `/aimen-workflow` (添加新功能)
└─ YES → 有规划?
    ├─ NO → suggest: 运行规划
    └─ YES → 有任务?
        ├─ NO → suggest: 分解任务
        └─ YES → 有实现?
            ├─ NO → suggest: 开始实现
            └─ YES → suggest: 完成或添加新功能
```

### "应该跳过哪个阶段?"

```
澄清需要?
├─ YES → 运行 `/aimen.clarify`
└─ NO → 直接规划

需要质量检查?
├─ YES → 运行 `/aimen.checklist`
└─ NO → 跳过

需要分析?
├─ YES → 运行 `/aimen.analyze`
└─ NO → 直接实现
```

## 错误恢复

如果任何agent失败：

```
❌ 阶段失败

[错误详情]

选项:

(A) 重试该阶段
(B) 跳过并继续 (风险警告)
(C) 返回修改前置条件
(D) 停止工作流

请选择: _
```

## 集成提示

### 与版本控制集成

```
实现完成后:

git add -A
git commit -m "feat: implement [feature-name] (all tasks complete)"
git push origin 001-user-auth
```

### 与CI/CD集成

```
推送后自动:
1. 运行测试套件
2. 运行linting
3. 部署到staging (可选)
```

## 高级用法

### 多个并发功能

可同时处理多个功能开发：
- 功能1: 在阶段3 (Planning)
- 功能2: 在阶段5 (Implementation)
- 功能3: 在阶段4 (Tasking)

每个功能都有独立的 `specs/[###-feature-name]/` 目录。

### 返工和迭代

如果需要修改：
1. 选择"修改" 选项
2. 进行更改
3. 重新运行该阶段的agent
4. 状态会自动更新

### 快速模式

跳过可选阶段快速实现：
```
Constitution → Specify → Plan → Tasks → Implement (跳过 Clarify & Analyze)
```

### 质量模式

包含所有质量检查：
```
Constitution → Specify → Clarify → Plan → Checklist → Tasks → Analyze → Implement
```

