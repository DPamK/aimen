---
description: 将规划分解为可执行的、依赖排序的任务
---

# Agent Tasks - 任务分解和生成

## 职责

根据规划和设计文档生成可执行的、依赖排序的任务列表，包括：
- 从技术栈和用户故事生成任务
- 映射实体和API端点到任务
- 创建正确格式化的checklistformat任务
- 生成依赖图和并行执行建议

## 输入规范

```text
$ARGUMENTS = [可选的用户上下文]
```

必需文件：
- `specs/[###-feature-name]/plan.md` (来自agent-plan)
- `specs/[###-feature-name]/spec.md` (用户故事和优先级)

可选文件：
- `specs/[###-feature-name]/data-model.md`
- `specs/[###-feature-name]/contracts/`
- `specs/[###-feature-name]/research.md`
- `specs/[###-feature-name]/quickstart.md`

## 执行流程

### Step 1: 初始化

1. 运行先决条件检查: `.specify/scripts/powershell/check-prerequisites.ps1 -Json`
2. 解析JSON获取FEATURE_DIR和AVAILABLE_DOCS
3. 从FEATURE_DIR加载所有可用文档

### Step 2: 加载设计文档

```
plan.md (强制)
  ├── 技术栈提取
  └── 项目结构

spec.md (强制)
  ├── 用户故事提取
  └── 优先级确定

data-model.md (可选)
  ├── 实体列表
  └── 关系

contracts/ (可选)
  ├── API端点列表
  └── 操作映射

research.md (可选)
  ├── 技术决策
  └── 依赖选择

quickstart.md (可选)
  └── 测试场景
```

### Step 3: 任务生成工作流

#### 3.1 提取上下文

从plan.md：
- 编程语言和版本
- 主要依赖库
- 存储技术
- 测试框架
- 项目结构 (源代码目录布局)

#### 3.2 提取用户故事

从spec.md：
- 按优先级排序的用户故事
- 每个故事的验收标准
- 功能需求映射

#### 3.3 映射实体到故事 (如有data-model.md)

```
User Story 1 (P1)
├── 需求A
│   └── 对应实体: User, Profile
├── 需求B
│   └── 对应实体: Session
└── ...
```

#### 3.4 映射端点到故事 (如有contracts/)

```
User Story 1 (P1)
├── POST /users (创建用户)
├── GET /users/{id} (获取用户)
├── POST /sessions (创建会话)
└── ...
```

#### 3.5 提取技术决策 (如有research.md)

- 技术选择和原因
- 依赖选择
- 集成点

### Step 4: 生成任务清单

#### 4.1 Phase 1: 设置任务

```
- [ ] T001 创建项目结构 per implementation plan
- [ ] T002 初始化[包管理器] (npm/pip/cargo等)
- [ ] T003 配置[测试框架] (pytest/jest/cargo test等)
- [ ] T004 设置[CI/CD] (如计划中指定)
- [ ] T005 创建README和基本文档
```

#### 4.2 Phase 2: 基础任务

所有用户故事的阻挡前置条件：

```
- [ ] T010 实现数据库架构 (如适用)
- [ ] T011 创建基础模型 (所有实体)
- [ ] T012 实现认证/授权 (如需要)
- [ ] T013 创建API基础架构 (路由、中间件等)
- [ ] T014 配置日志和监控 (如宪法要求)
```

#### 4.3 Phase 3+: 按用户故事的阶段

对于每个用户故事 (按优先级顺序)：

```
### Phase 3: User Story 1 - [故事标题] (P1)

Goal: [故事目标]

Independent Test: [如何独立测试此故事]

- [ ] T020 [P] [US1] 实现[实体]模型在src/models/[entity].py
- [ ] T021 [P] [US1] 创建[实体]的数据库迁移
- [ ] T022 [US1] 实现[实体]服务在src/services/[entity]_service.py
- [ ] T023 [P] [US1] 创建API端点GET /[entities] 在src/routes/[entities].py
- [ ] T024 [P] [US1] 创建API端点POST /[entities] 在src/routes/[entities].py
- [ ] T025 [US1] 实现验证逻辑在[entity]_service.py
- [ ] T026 [US1] 添加[故事]的集成测试在tests/integration/test_[story].py
```

#### 4.4 最后Phase: 抛光和交叉关注

```
- [ ] T100 添加API文档 (Swagger/GraphQL Playground)
- [ ] T101 创建部署脚本
- [ ] T102 添加性能测试 (如NFR要求)
- [ ] T103 安全审计和修复
- [ ] T104 最终集成测试
- [ ] T105 用户验收测试 (UAT)
```

### Step 5: 任务格式验证

**严格的checklistformat**:
```
- [ ] [TaskID] [P?] [Story?] Description with file path
```

详细规则：
1. **Checkbox**: 必须以 `- [ ]` 开头
2. **TaskID**: T001, T002, T003... (执行顺序)
3. **[P] 标记**: 仅当任务可并行化时包含
   - 不同的文件，没有依赖于未完成任务的
4. **[Story] 标记**: 仅对用户故事阶段的任务
   - 格式: [US1], [US2], [US3]...
   - Setup phase: 不包含
   - Foundational phase: 不包含
   - 用户故事阶段: 必须包含
   - Polish phase: 不包含
5. **Description**: 清晰的操作，带有确切的文件路径

**有效示例**:
- ✅ `- [ ] T001 Create project structure per implementation plan`
- ✅ `- [ ] T005 [P] Implement authentication middleware in src/middleware/auth.py`
- ✅ `- [ ] T012 [P] [US1] Create User model in src/models/user.py`
- ✅ `- [ ] T014 [US1] Implement UserService in src/services/user_service.py`

**无效示例**:
- ❌ `- [ ] Create User model` (缺少ID和故事标签)
- ❌ `- [ ] T012 Create User model` (缺少用户故事标签)

### Step 6: 生成依赖图

创建依赖关系可视化：

```markdown
## Dependency Graph

```
T001 (Project Setup)
└── T002 (Initialize Package Manager)
    └── T003 (Configure Testing)
        └── T010 (Database Schema)
            ├── T020 (US1 - Entity Model) → T021, T022, T023, T024
            │   ├── T022 (Service) → T025, T026
            │   ├── T023 (API GET) → [Independent]
            │   └── T024 (API POST) → [Independent]
            └── T030 (US2 - ...) → ...
```
```

### Step 7: 识别并行机会

```markdown
## Parallel Execution Examples

### Per User Story
User Story 1 can be implemented in parallel groups:
- Group 1 (Parallel): T020, T021, T023, T024 (different files)
- Group 2 (Sequential): T022 → T025, T026

### Across Stories
After T010 (Database Schema):
- US1 tasks can start independently of US2 tasks
- Different team members can work on US1, US2, US3 simultaneously
```

### Step 8: MVP范围建议

```markdown
## MVP Scope

**Suggested MVP** (User Story 1 + Foundation):
- Phase 1: Setup
- Phase 2: Foundation
- Phase 3: User Story 1
- Phase 4: Polish (minimal)

**Estimated effort**: [X] tasks, [Y] days

**Beyond MVP**:
- Phase 3.2: User Story 2
- Phase 3.3: User Story 3
- Phase 4: Full Polish
```

### Step 9: 验证和写入

1. 验证所有用户故事都有任务
2. 验证所有任务严格遵循checklistformat
3. 验证无重复或遗漏
4. 写入tasks.md

## 输出规范

### 主输出文件
- `specs/[###-feature-name]/tasks.md` - 完整的任务清单

### 包含的章节

1. **功能概述** - 来自规范
2. **技术背景** - 来自规划
3. **Phase 1: Setup** - 初始化任务
4. **Phase 2: Foundation** - 基础任务
5. **Phase 3+: User Stories** - 按优先级的故事
6. **Phase Final: Polish** - 抛光任务
7. **Dependency Graph** - 依赖可视化
8. **Parallel Execution Opportunities** - 并行建议
9. **MVP Scope** - 最小可行产品建议

### 执行结果报告

```markdown
## 任务生成完成

**功能**: [###-feature-name]
**总任务数**: [N]

**按Phase的任务分布**:
- Phase 1 (Setup): [N] tasks
- Phase 2 (Foundation): [N] tasks
- Phase 3 (US1): [N] tasks
- Phase 3.2 (US2): [N] tasks (可选)
- ...
- Phase Final (Polish): [N] tasks

**用户故事覆盖**:
- [US1]: [N] 任务
- [US2]: [N] 任务 (如适用)
- ...

**并行机会**:
- [识别的并行组数]
- 可加速开发

**MVP范围**:
- Phases: 1, 2, 3 (User Story 1)
- 任务数: [X]
- 估计工作量: [Y]

**tasks.md 位置**:
- specs/[###-feature-name]/tasks.md

**下一步**:
- 可选: `/aimen.analyze` 一致性验证
- 或: `/aimen.implement` 开始实现
```

## 成功标准

- ✓ 所有用户故事都有对应的任务
- ✓ 任务格式100%符合checklistformat
- ✓ TaskID: T001, T002... (无间隙，按执行顺序)
- ✓ [P]标记仅用于真正可并行的任务
- ✓ [Story]标记仅用于用户故事阶段任务
- ✓ 每个任务都包含文件路径
- ✓ 依赖关系清晰且可视化
- ✓ MVP范围定义清晰
- ✓ 没有重复或遗漏的任务

## 约束和限制

- TaskID必须是T001, T002... (无间隙)
- [P]标记仅用于不同文件、无依赖的任务
- [Story]标记仅用于用户故事阶段
- 所有文件路径必须基于plan.md中的项目结构
- 任务必须能独立执行和验证

## 错误处理

| 错误 | 处理 |
|------|------|
| 找不到plan.md | 错误: 缺少规划，运行 `/aimen.plan` 先 |
| 找不到spec.md | 错误: 缺少规范，运行 `/aimen.specify` 先 |
| 无法生成故事任务 | 错误: 规范或规划不足，需要澄清 |
| TaskID有间隙 | 错误: 重新编号，确保T001...TNxx连续 |
| [P]标记不正确 | 警告: 检查并行性，可能阻塞实现 |
| 缺少故事标签 | 错误: 所有US阶段任务必须有标签 |

## 可选步骤

- **分析**: 可选运行 `/aimen.analyze` 验证spec/plan/tasks的一致性
- **迭代**: 可多次运行，每次细化任务

## 下一步指导

任务生成完成后：

1. **需要一致性验证** → 执行 `/aimen.analyze` (可选但推荐)
2. **准备实现** → 执行 `/aimen.implement` (推荐)
3. **需要质量检查** → 执行 `/aimen.checklist` (在implement之前)

