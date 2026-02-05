---
description: 执行技术规划，生成设计文件和研究文档
---

# Agent Plan - 技术规划和设计

## 职责

执行完整的技术规划工作流程，包括：
- Phase 0: 研究和技术选择验证
- Phase 1: 设计数据模型、API合约和集成指南
- 宪法检查 (初始和最终)
- 生成可用于任务分解的完整设计文档

## 输入规范

```text
$ARGUMENTS = [可选的用户上下文]
```

必需文件：
- `specs/[###-feature-name]/spec.md` (来自agent-specify/clarify)
- `.specify/memory/constitution.md`
- `.specify/templates/plan-template.md`

## 执行流程

### Step 1: 初始化

1. 运行 `.specify/scripts/powershell/setup-plan.ps1 -Json` 获取：
   - FEATURE_SPEC - 规范文件路径
   - IMPL_PLAN - 规划文件路径
   - SPECS_DIR - 特性目录
   - BRANCH - 当前分支名称
2. 加载规范、宪法和规划模板

### Step 2: 填充规划基础信息

从spec.md和上下文中填充：
- 技术背景 (语言、依赖、存储、测试、平台、项目类型、性能目标、约束、规模)
- 参考spec中的所有内容
- 对于不确定的，使用 `NEEDS CLARIFICATION` 标记

### Step 3: 宪法初始检查

验证规范是否符合constitution.md中的所有MUST原则：
- 如果违反 → ERROR: 列出违反的原则，要求修复
- 如果符合 → 继续到Phase 0

### Phase 0: 研究和澄清

**目标**: 解决所有技术不确定性

1. **提取未知项**:
   - 每个 `NEEDS CLARIFICATION` → 研究任务
   - 每个关键依赖 → 最佳实践任务
   - 每个集成点 → 模式任务

2. **生成研究任务**示例:
   ```text
   - Research [NEEDS CLARIFICATION field] for [feature context]
   - Find best practices for [technology] in [domain]
   - Evaluate [alternative 1] vs [alternative 2] for [purpose]
   ```

3. **编制发现**到 `research.md`:
   - 决策: [选择了什么]
   - 原理: [为什么选择]
   - 考虑的备选方案: [还评估了什么]

**输出**: `specs/[###-feature-name]/research.md`

### Phase 1: 设计和合约

**前置条件**: `research.md` 完成 (所有NEEDS CLARIFICATION已解决)

#### 1.1 数据模型设计

从功能规范中提取实体到 `data-model.md`：
- 实体名称、字段、关系
- 验证规则 (从需求推导)
- 状态转换 (如适用)

结构示例：
```markdown
## [Entity Name]
- Fields: [list with types and constraints]
- Primary Key: [identifier]
- Relationships: [references to other entities]
- Validation Rules: [from requirements]
- State Transitions: [if applicable]
```

#### 1.2 API合约生成

从功能需求生成API合约到 `contracts/`：
- 每个用户操作 → 一个端点
- 使用标准REST或GraphQL模式
- 包含请求、响应、错误处理

输出格式：
- OpenAPI 3.0 schema (YAML/JSON)
- 或GraphQL schema (.graphql)
- 目录结构: `contracts/[entity]/[method].yaml` 或类似

#### 1.3 代理上下文更新

运行 `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`：
- 检测正在使用的AI代理类型
- 更新代理特定的上下文文件
- 仅添加当前规划中的新技术
- 保留标记之间的手动修改

#### 1.4 快速启动指南

创建 `quickstart.md` 用于测试和集成：
- 测试场景示例
- 集成步骤
- 常见问题和解决方案

### Step 4: 宪法最终检查

重新验证设计是否符合constitution.md：
- 数据模型是否遵循宪法约束
- API设计是否符合宪法规则
- 所有MUST原则都得到尊重

**如果失败**:
- ERROR: 列出违反的原则
- 要求返回设计步骤修复
- 不能继续到任务阶段

### Step 5: 验证和报告

检查所有Phase 1输出：
- ✓ data-model.md 完整
- ✓ contracts/ 目录存在且有规范
- ✓ quickstart.md 实用且清晰
- ✓ 宪法检查通过
- ✓ 代理上下文已更新

## 输出规范

### Phase 0 输出
- `specs/[###-feature-name]/research.md` - 研究发现和技术决策

### Phase 1 输出

**数据设计**:
- `specs/[###-feature-name]/data-model.md` - 数据实体和关系

**API设计**:
- `specs/[###-feature-name]/contracts/` - API规范文件
  - 子文件示例: `contracts/user-api.yaml`, `contracts/schema.graphql`

**文档和指南**:
- `specs/[###-feature-name]/quickstart.md` - 快速启动指南

**规划文件**:
- `specs/[###-feature-name]/plan.md` - 更新的实现规划 (所有字段已填充)

**上下文更新**:
- 代理特定的上下文文件 (由update-agent-context.ps1维护)

### 执行结果报告

```markdown
## 技术规划完成

**分支**: [###-feature-name]

**Phase 0: 研究**
- 识别的研究主题: [N]
- research.md 生成: ✓

**Phase 1: 设计**
- 识别的实体: [N]
  - 在 data-model.md 中文档化
- 识别的API端点: [N]
  - OpenAPI规范在 contracts/ 中
- Quickstart指南: ✓

**宪法检查**
- 初始检查: ✓ 通过
- 最终检查: ✓ 通过
- 违反的原则: 无

**生成的文件**:
- specs/[###-feature-name]/research.md
- specs/[###-feature-name]/plan.md
- specs/[###-feature-name]/data-model.md
- specs/[###-feature-name]/contracts/[files]
- specs/[###-feature-name]/quickstart.md

**下一步**:
- 执行 `/aimen.tasks` 分解为可执行任务
- 可选: `/aimen.checklist` 验证需求质量

**技术栈总结**:
- 语言: [X]
- 主要依赖: [列表]
- 存储: [X]
- 目标平台: [X]
```

## 成功标准

- ✓ 所有Phase 0研究任务完成
- ✓ 所有Phase 1设计文件生成
- ✓ 宪法检查通过 (初始和最终)
- ✓ 没有遗留的NEEDS CLARIFICATION (来自Phase 0)
- ✓ data-model.md 包含至少一个实体
- ✓ contracts/ 包含至少一个API规范
- ✓ quickstart.md 有实用内容
- ✓ plan.md 完全填充，无占位符

## 约束和限制

- 必须完全通过宪法检查（不能绕过MUST原则）
- 所有文件路径使用绝对路径
- research.md 必须解决所有NEEDS CLARIFICATION
- 数据模型必须从功能需求推导，不能发明新的实体
- API设计必须直接支持用户故事

## 错误处理

| 错误 | 处理 |
|------|------|
| 找不到spec.md | 错误: 缺少先决条件，运行 `/aimen.specify` 先 |
| 宪法初始检查失败 | 错误: 规范违反宪法原则，修复规范后重试 |
| Phase 0 未解决 | 错误: 研究任务未完成，完成research.md后重试 |
| 宪法最终检查失败 | 错误: 设计违反宪法，修复设计后重试 |
| 无法提取实体 | 错误: 数据模型无法从规范推导，需要澄清规范 |
| 技术栈不清楚 | 使用: 合理默认值或NEEDS CLARIFICATION标记 |

## 可选步骤

- **Checklist**: 可选运行 `/aimen.checklist` 验证需求质量 (在tasking之前)
- **多次迭代**: 可以多次运行plan阶段，每次更新research.md和设计文件

## 下一步指导

规划完成后的选择：

1. **需要验证一致性** → 执行 `/aimen.analyze` (可选但推荐)
2. **准备实现** → 执行 `/aimen.tasks` (推荐)
3. **需要质量检查** → 执行 `/aimen.checklist` (可选)

