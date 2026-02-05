# AIMEN 工作流系统 - Sub Agent 架构设计

## 概述

AIMEN 工作流系统采用 Agent-Based 架构，将 Spec-Kit 的完整工作流程分解为独立的、可协调的子Agent。每个Agent负责一个特定的工作阶段，接收上一阶段的输出作为输入，生成本阶段的输出，并交付给下一个Agent。

## Agent 交互模型

```
主 Command (aimen-workflow.md)
    ├── 检查工作流状态 (workflow-state.md)
    ├── 询问用户下一步操作
    └── 调用对应的 Sub Agent
        ├── Agent 执行工作
        ├── Agent 报告结果
        ├── 更新工作流状态
        └── 返回主 Command
    └── 根据结果决定下一步 Agent 或工作流完成
```

## Sub Agents 清单

| Agent | 文件名 | 职责 | 输入 | 输出 |
|-------|--------|------|------|------|
| 宪法Agent | agent-constitution.md | 创建/更新项目治理宪法 | 项目原则描述 | constitution.md v.X.Y.Z |
| 规范Agent | agent-specify.md | 创建功能规范 | 特性描述 | spec.md + 分支 |
| 澄清Agent | agent-clarify.md | 澄清规范歧义 | spec.md + 歧义 | 更新的spec.md |
| 规划Agent | agent-plan.md | 执行技术规划 | spec.md + constitution.md | research.md, design文件 |
| 任务Agent | agent-tasks.md | 分解为可执行任务 | plan.md + spec.md | tasks.md |
| 分析Agent | agent-analyze.md | 交叉工件一致性分析 | spec.md + plan.md + tasks.md | 分析报告 |
| 实现Agent | agent-implement.md | 执行实现计划 | tasks.md + plan.md | 源代码 + ignore文件 |

## Agent 通用接口规范

### 输入约定

每个Agent接收以下标准输入：

```markdown
## User Input

\`\`\`text
$ARGUMENTS
\`\`\`

You **MUST** consider the user input before proceeding (if not empty).
```

**$ARGUMENTS** 包含：
- 用户直接输入的参数
- 工作流状态中的上下文信息
- 先前步骤生成的文件路径

### 输出约定

每个Agent输出应包含：

1. **执行摘要** - 这个Agent做了什么
2. **生成的文件** - 输出文件的路径和说明
3. **状态更新** - 返回给主Command的状态信息
4. **错误处理** - 遇到的任何错误或警告

### 错误处理规范

所有Agent应使用一致的错误处理模式：

```
ERROR: [错误类别] - [详细说明]
REMEDIATION: [建议修复步骤]
NEXT_STEP: [用户应执行的操作]
```

**错误类别**:
- `MISSING_INPUT` - 缺少必需输入
- `INVALID_FORMAT` - 输入格式不符合预期
- `GATE_FAILURE` - 检查门失败 (如宪法检查)
- `PREREQUISITE_NOT_MET` - 先决条件不满足
- `EXECUTION_ERROR` - 执行过程中出错

## 详细Agent规范

### 1. Agent Constitution (宪法Agent)

**文件**: `agents/agent-constitution.md`

**职责**: 创建和管理项目治理宪法

**输入**:
- 项目原则描述 ($ARGUMENTS)
- 可选：现有constitution.md (用于更新)

**执行步骤**:
1. 加载constitution模板
2. 识别所有占位符
3. 收集/推导具体值 (用户输入或仓库上下文)
4. 版本递增决策 (MAJOR/MINOR/PATCH)
5. 填充所有占位符
6. 一致性传播检查:
   - 验证plan-template, spec-template, tasks-template 对齐
   - 检查所有command文件中的过时参考
   - 验证README等运行时文档
7. 生成同步影响报告
8. 写入constitution.md

**输出**:
- `.specify/memory/constitution.md` (新版本)
- 版本变更说明
- 受影响模板清单

**约束**:
- 版本必须遵循 MAJOR.MINOR.PATCH 格式
- 不能留下未定义的占位符 (除非显式标记为deferred)
- 日期格式: ISO 8601 (YYYY-MM-DD)

**成功标准**:
- ✓ 没有遗留的未定义占位符
- ✓ 版本号递增正确
- ✓ 所有依赖模板都已检查
- ✓ 同步影响报告完整

---

### 2. Agent Specify (规范Agent)

**文件**: `agents/agent-specify.md`

**职责**: 根据特性描述创建功能规范

**输入**:
- 特性描述 ($ARGUMENTS)
- 现有规范目录结构

**执行步骤**:
1. 从特性描述生成短名称 (2-4单词, action-noun格式)
2. 检查现有分支:
   - 执行 `git fetch --all --prune`
   - 扫描远程分支、本地分支、specs目录
   - 计算下一个编号
3. 调用 `create-new-feature.ps1 -Json`
4. 加载spec-template.md
5. 解析特性描述:
   - 提取关键概念 (角色、行动、数据、约束)
   - 识别用户场景
6. 填充规范:
   - 用户场景和测试 (按P1/P2/P3排序)
   - 功能需求 (每个可测试)
   - 成功标准 (量化+定性)
   - 关键实体
7. 标记歧义 (最多3个 `[NEEDS CLARIFICATION]`)
8. 写入spec.md

**输出**:
- `specs/[###-feature-name]/spec.md`
- 创建的分支: `[###-feature-name]`
- JSON: 分支名称、spec文件路径

**约束**:
- 最多3个[NEEDS CLARIFICATION]标记
- 每个用户故事必须独立可测试
- 每个功能需求必须可测试

**成功标准**:
- ✓ 规范文件创建成功
- ✓ 分支创建成功
- ✓ 至少1个用户故事
- ✓ 所有故事优先级已定义
- ✓ [NEEDS CLARIFICATION]不超过3个

---

### 3. Agent Clarify (澄清Agent)

**文件**: `agents/agent-clarify.md`

**职责**: 通过目标明确的问题澄清规范中的歧义

**输入**:
- 完整的spec.md (来自agent-specify)
- 可选的用户上下文 ($ARGUMENTS)

**执行步骤**:
1. 运行先决条件检查获取规范文件路径
2. 加载规范文件
3. 执行结构化歧义扫描:
   - 功能范围和行为
   - 域名和数据模型
   - 交互和用户体验
   - 非功能属性
   - 集成和依赖
   - 边界情况
   - 约束和权衡
   - 术语和一致性
   - 完成信号
   - 杂项/占位符
4. 为每个Partial/Missing类别生成候选问题
5. 生成最多5个优先级问题
6. 交互式提问循环:
   - 每次提出1个问题
   - 接受答案
   - 可选后续跟进 (最多2个)
7. 将答案编码到spec.md
8. 更新spec.md

**输出**:
- 更新的 `specs/[###-feature-name]/spec.md`
- 澄清对话日志 (可选)

**约束**:
- 最多10个总问题
- 每个问题需要短答案 (选择或<=5字)
- 只包括有实质影响的澄清

**成功标准**:
- ✓ 所有[NEEDS CLARIFICATION]都已解决
- ✓ 澄清答案已添加到spec.md
- ✓ spec.md仍符合模板结构

---

### 4. Agent Plan (规划Agent)

**文件**: `agents/agent-plan.md`

**职责**: 执行技术规划，生成设计文件

**输入**:
- spec.md (来自agent-specify或agent-clarify)
- constitution.md
- plan-template.md

**执行步骤**:

#### Phase 0: 研究
1. 从技术背景提取未知项
2. 为每个未知/依赖/集成生成研究任务
3. 编制研究发现到research.md:
   - 决策
   - 原理
   - 考虑的备选方案

#### Phase 1: 设计
1. 从规范提取实体 → data-model.md
2. 从功能需求生成API合约 → contracts/
3. 更新代理上下文
4. 创建quickstart.md

#### 宪法检查
- Phase 0之前初始检查
- Phase 1之后最终检查
- 失败则报告ERROR

**输出**:
- `specs/[###-feature-name]/research.md`
- `specs/[###-feature-name]/plan.md` (填充)
- `specs/[###-feature-name]/data-model.md`
- `specs/[###-feature-name]/contracts/` (API规范)
- `specs/[###-feature-name]/quickstart.md`

**约束**:
- 必须通过宪法检查
- 所有NEEDS CLARIFICATION必须解决
- 使用绝对路径

**成功标准**:
- ✓ 所有设计文件生成
- ✓ 宪法检查通过
- ✓ 没有未解决的研究问题

---

### 5. Agent Tasks (任务Agent)

**文件**: `agents/agent-tasks.md`

**职责**: 分解规划为可执行的、依赖排序的任务

**输入**:
- plan.md (来自agent-plan)
- spec.md (用户故事和优先级)
- 可选: data-model.md, contracts/, research.md, quickstart.md

**执行步骤**:
1. 运行先决条件检查
2. 加载设计文档
3. 执行任务生成工作流:
   - 从plan.md提取技术栈和结构
   - 从spec.md提取用户故事和优先级
   - 映射实体到故事 (如有data-model.md)
   - 映射端点到故事 (如有contracts/)
   - 提取技术决策 (如有research.md)
4. 按优先级生成任务:
   - Phase 1: 设置任务
   - Phase 2: 基础任务
   - Phase 3+: 按故事优先级的阶段
   - 最后: 抛光和交叉关注
5. 验证任务格式 (checklistformat):
   - `- [ ] [TaskID] [P?] [Story?] Description with file path`
6. 输出依赖图、并行机会、MVP范围

**输出**:
- `specs/[###-feature-name]/tasks.md`
- 依赖关系图
- 并行执行建议

**约束**:
- TaskID: T001, T002, T003... (执行顺序)
- [P]标记: 仅并行任务
- [Story]标记: 仅用户故事阶段任务
- 每个任务必须包含文件路径

**成功标准**:
- ✓ 所有用户故事都有任务
- ✓ 任务格式100%符合
- ✓ 依赖关系定义清晰
- ✓ 包含MVP范围建议

---

### 6. Agent Analyze (分析Agent)

**文件**: `agents/agent-analyze.md`

**职责**: 执行交叉工件一致性和质量分析

**输入**:
- spec.md (来自agent-specify/clarify)
- plan.md (来自agent-plan)
- tasks.md (来自agent-tasks)
- constitution.md

**执行步骤**:
1. 运行先决条件检查
2. 加载所有工件的最小必需上下文
3. 构建语义模型:
   - 需求清单 (功能+非功能)
   - 用户故事/行动清单
   - 任务覆盖映射
   - 宪法规则集
4. 执行检测通过 (限制50个发现):
   - 重复检测: 识别近似重复需求
   - 歧义检测: 标记模糊词汇
   - 规范不足: 缺少对象/可测量结果
   - 宪法对齐: 检查与MUST原则的冲突
   - 覆盖完整性: 需求→任务映射
5. 生成结构化分析报告:
   - 按优先级排序发现
   - 提供修正建议
6. 输出报告

**输出**:
- 分析报告 (markdown格式)
- 发现汇总 (优先级排序)
- 修正建议清单

**约束**:
- 严格只读 (不修改任何文件)
- 宪法冲突自动CRITICAL
- 最多50个发现
- 超额发现汇总为溢出项

**成功标准**:
- ✓ 报告完成
- ✓ 关键冲突识别
- ✓ 修正建议可执行
- ✓ 用户可明确批准或拒绝

---

### 7. Agent Implement (实现Agent)

**文件**: `agents/agent-implement.md`

**职责**: 执行规划的实现

**输入**:
- tasks.md (来自agent-tasks)
- plan.md (技术栈和结构)
- 可选: data-model.md, contracts/, research.md, quickstart.md
- 可选: checklists/ (检查清单完成度)

**执行步骤**:

#### 验证阶段
1. 运行先决条件检查
2. 检查清单完成度 (如存在):
   - 扫描所有检查清单文件
   - 计算完成度
   - 如不完整，询问用户是否继续

#### 设置阶段
1. 加载实现上下文
2. 创建/验证ignore文件:
   - 检查git仓库 → .gitignore
   - 检查Docker → .dockerignore
   - 检查ESLint → .eslintignore
   - 按技术栈添加模式

#### 执行阶段
1. 解析tasks.md
2. 按Phase顺序执行任务:
   - Phase 1 (设置) → Phase 2 (基础) → Phase 3+ (故事) → 最后 (抛光)
3. 对每个任务:
   - 标记进行中
   - 执行任务
   - 验证输出
   - 标记完成
4. 生成进度报告

**输出**:
- 实现的源代码 (根据plan.md结构)
- 创建/更新的ignore文件
- 进度报告 (完成任务数/总数)

**约束**:
- 必须按Phase顺序执行
- 每个任务必须完成验证
- Ignore文件必须基于检测的技术栈

**成功标准**:
- ✓ 所有Phase执行完成
- ✓ 所有任务标记为完成
- ✓ Ignore文件已创建
- ✓ 代码符合计划中定义的结构

---

## Agent 间通信约定

### 文件路径传递

所有文件路径使用**绝对路径**：
- Windows: `e:\githubLibrary\aimen\specs\001-feature-name\spec.md`
- Unix: `/path/to/aimen/specs/001-feature-name/spec.md`

### JSON输出格式

Agent运行脚本时，输出JSON格式的结构化结果：

```json
{
  "status": "success" | "error" | "warning",
  "stage": "constitution" | "specify" | "clarify" | "plan" | "tasks" | "analyze" | "implement",
  "output_files": {
    "primary": "path/to/primary/file",
    "secondary": ["path/to/secondary/1", "path/to/secondary/2"]
  },
  "summary": "Brief summary of what was accomplished",
  "next_steps": ["Next action 1", "Next action 2"],
  "errors": ["Error 1", "Error 2"] // If any
}
```

### 状态更新格式

每个Agent完成后，返回状态更新给主Command：

```markdown
## 执行结果

**状态**: ✓ 成功 | ⚠ 警告 | ✗ 失败

**完成任务**:
- 生成了spec.md v1-user-auth
- 创建了分支001-user-auth

**输出文件**:
- specs/001-user-auth/spec.md

**后续建议**:
- 执行 `/aimen.clarify` 澄清需求
- 或直接执行 `/aimen.plan` 开始规划

**问题** (如有):
- None
```

---

## Agent 协调规则

### 条件执行

某些Agent是可选的：

| 条件 | Agent | 是否可选 |
|------|-------|---------|
| 规范有歧义 | Clarify | YES (但推荐) |
| 需要质量检查 | Checklist | YES |
| 需要一致性验证 | Analyze | YES (但推荐) |
| 准备实现 | Implement | NO (必须最后执行) |

### 错误恢复

如果任何Agent失败：

1. **生成错误报告** (包含remediation步骤)
2. **不修改工作流状态** (保留失败前的状态)
3. **建议用户操作**:
   - 修复错误
   - 重新运行该Agent
   - 或手动修改生成的文件

### 缓存和重用

- 每个Agent的输出文件是持久的
- 如果重新运行同一Agent，可覆盖先前的输出
- 主Command维护指针以追踪当前阶段

---

## 集成检查清单

设计Sub Agents时的检查清单：

- [ ] 输入约定清晰 (接收$ARGUMENTS和文件路径)
- [ ] 输出约定清晰 (生成的文件和状态更新)
- [ ] 错误处理完整 (所有失败情况都有remediation)
- [ ] 与上/下游Agent的接口定义明确
- [ ] 支持幂等性 (重新运行应产生相同结果)
- [ ] 文件路径使用绝对路径
- [ ] 包含成功标准 (明确的验收条件)
- [ ] 包含约束说明 (不能做什么)
- [ ] 包含决策树 (分支逻辑)
- [ ] 支持跳过步骤 (如某些Agent是可选的)

