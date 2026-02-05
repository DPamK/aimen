# AIMEN 工作流系统 - 配置和指南

## 项目配置

### 基本设置

```yaml
project_name: "AIMEN - AI-Driven Methodology for Engineering"
version: "1.0.0"
created: "2025-02-05"

# 工作目录
workspace_root: "e:\\githubLibrary\\aimen"
specs_dir: "e:\\githubLibrary\\aimen\\specs"
agents_dir: "e:\\githubLibrary\\aimen\\agents"
commands_dir: "e:\\githubLibrary\\aimen\\commands"
docs_dir: "e:\\githubLibrary\\aimen\\doc"

# 规范工具配置
specify_config: ".specify"
specify_memory: ".specify/memory"
specify_scripts: ".specify/scripts/powershell"
specify_templates: ".specify/templates"
```

## 工作流组件

### 核心命令

**主协调器**:
- `commands/aimen-workflow.md` - 工作流主entry point

### Sub Agents

**治理**:
- `agents/agent-constitution.md` - 项目宪法管理

**需求**:
- `agents/agent-specify.md` - 功能规范生成
- `agents/agent-clarify.md` - 需求澄清

**设计**:
- `agents/agent-plan.md` - 技术规划和设计

**任务**:
- `agents/agent-tasks.md` - 任务分解

**质量**:
- `agents/agent-analyze.md` - 交叉工件分析
- (agent-checklist 可选，在plan基础上)

**执行**:
- `agents/agent-implement.md` - 实现执行

### 文档

**架构**:
- `doc/spec-kit-workflow.md` - Spec-Kit工作流完整文档
- `doc/agent-architecture.md` - Sub Agent架构设计

**状态**:
- `aimen/workflow-state.md` - 当前项目状态追踪

**配置**:
- `aimen/config.md` - 本文件

## 使用快速参考

### 启动新项目

```bash
# 1. 创建项目治理宪法
/aimen.constitution 

# 2. 添加新功能
/aimen.specify 添加用户认证

# 3. 澄清规范 (可选)
/aimen.clarify

# 4. 执行规划
/aimen.plan

# 5. 生成检查清单 (可选)
/aimen.checklist

# 6. 分解任务
/aimen.tasks

# 7. 分析一致性 (可选但推荐)
/aimen.analyze

# 8. 执行实现
/aimen.implement
```

### 最小工作流

```bash
/aimen.constitution
/aimen.specify [特性描述]
/aimen.plan
/aimen.tasks
/aimen.implement
```

### 质量保证工作流

```bash
/aimen.constitution
/aimen.specify [特性描述]
/aimen.clarify
/aimen.plan
/aimen.checklist
/aimen.tasks
/aimen.analyze
/aimen.implement
```

## 文件约定

### 目录结构

```
aimen/
├── agents/                          # Sub Agent定义
│   ├── agent-constitution.md
│   ├── agent-specify.md
│   ├── agent-clarify.md
│   ├── agent-plan.md
│   ├── agent-tasks.md
│   ├── agent-analyze.md
│   └── agent-implement.md
├── commands/                        # 主Command和工具命令
│   └── aimen-workflow.md           # 主协调器
├── doc/                            # 文档
│   ├── spec-kit-workflow.md        # 完整工作流说明
│   ├── agent-architecture.md       # Agent架构设计
│   └── config.md                   # 本文件
├── aimen/                          # 工作流配置和状态
│   ├── config.md                   # 配置 (本文件)
│   └── workflow-state.md           # 项目状态追踪
└── skills/                         # 可选: 技能库

specs/                              # 功能规范目录
├── 001-feature-name/
│   ├── spec.md                     # 功能规范
│   ├── plan.md                     # 技术规划
│   ├── research.md                 # 研究发现 (可选)
│   ├── data-model.md               # 数据模型
│   ├── quickstart.md               # 快速启动指南
│   ├── contracts/                  # API规范
│   ├── tasks.md                    # 任务清单
│   └── checklists/                 # 检查清单 (可选)
├── 002-feature-name/
└── ...
```

### 命名约定

**特性分支和目录**:
- 格式: `[###]-[short-name]`
- 示例: `001-user-auth`, `002-payment-integration`
- 编号: 全局递增整数

**任务ID**:
- 格式: `T[###]`
- 示例: `T001`, `T002`, `T100`
- 无间隙，按执行顺序

**阶段标记**:
- 用户故事: `[US1]`, `[US2]`...
- 并行化: `[P]` (仅真正并行的任务)

## 技术栈支持

### 支持的编程语言

- JavaScript/TypeScript (Node.js)
- Python
- Java
- C#/.NET
- Go
- Ruby
- PHP
- Rust
- Kotlin
- C++/C
- Swift
- R

### 支持的框架和工具

**Web框架**:
- Express, Fastify (Node.js)
- Django, FastAPI, Flask (Python)
- Spring Boot (Java)
- ASP.NET (C#)
- Gin, Echo (Go)
- Rails (Ruby)
- Laravel (PHP)
- Actix-web (Rust)

**数据库**:
- PostgreSQL, MySQL, MariaDB (SQL)
- MongoDB (NoSQL)
- Redis (Cache)
- DynamoDB (AWS)
- Firestore (Google)

**测试框架**:
- Jest, Mocha (JavaScript)
- pytest (Python)
- JUnit (Java)
- NUnit, xUnit (C#)
- Go testing
- RSpec (Ruby)
- PHPUnit (PHP)
- Rust built-in

**CI/CD**:
- GitHub Actions
- GitLab CI
- Jenkins
- CircleCI
- Travis CI

**容器化**:
- Docker
- Kubernetes
- Docker Compose

## 决策历史

### v1.0.0 (2025-02-05)

初始发布，包含：
- 8个核心agent（宪法、规范、澄清、规划、任务、分析、实现）
- 1个主协调器命令
- 完整的工作流文档
- Agent架构设计文档
- 项目状态追踪系统

**关键设计决策**:
- Agent模式: 每个工作阶段一个agent，便于维护和扩展
- 可选阶段: clarify、checklist、analyze为可选，支持快速工作流
- 状态追踪: 在workflow-state.md中维护单一事实来源
- 文档驱动: 每个阶段生成文档作为下一阶段输入

## 最佳实践

### 项目初始化

1. **创建宪法**: 定义项目原则和治理规则
2. **文档优先**: 所有决策都应该在spec中清晰记录
3. **明确原则**: constitution.md中的原则应该是可测试的

### 规范编写

1. **用户故事**: 按优先级P1→P2→P3排序
2. **澄清需求**: 使用[NEEDS CLARIFICATION]标记歧义，但最多3个
3. **验收标准**: 每个用户故事都应该有Given-When-Then格式的验收标准

### 规划执行

1. **研究优先**: Phase 0确保所有技术决策都有根据
2. **设计完整**: Phase 1应该生成所有关键工件 (data-model, contracts)
3. **宪法检查**: 在Phase 0和Phase 1之后都要检查

### 任务分解

1. **细粒度**: 任务应该小到可以在1-2天内完成
2. **并行识别**: 正确标记[P]以识别可并行任务
3. **故事映射**: [Story]标记应该清晰映射到spec中的用户故事

### 实现执行

1. **按Phase顺序**: 不要跳过Phase，按顺序执行
2. **验证输出**: 每个任务都应该验证生成的文件
3. **进度跟踪**: 在workflow-state.md中更新进度

## 故障排查

### 问题: "我找不到我的规范文件"

**解决**:
1. 检查 `specs/` 目录
2. 查找特性分支目录: `[###-feature-name]`
3. 规范文件应该在: `specs/[###-feature-name]/spec.md`

### 问题: "规范和规划不一致"

**解决**:
1. 运行 `/aimen.analyze` 检查一致性
2. 根据分析报告修改相关文件
3. 如需要，重新运行 `/aimen.plan` 或 `/aimen.tasks`

### 问题: "我想修改已完成的规范"

**解决**:
1. 编辑 `specs/[###-feature-name]/spec.md`
2. 重新运行后续阶段的agent (plan/tasks/implement)
3. 状态会自动更新

### 问题: "任务太多/太少"

**解决**:
1. 检查spec.md中的用户故事数量
2. 检查plan.md中的技术复杂性
3. 重新运行 `/aimen.tasks` 重新生成
4. 可以手动编辑tasks.md（不推荐，但可行）

## 扩展和定制

### 添加新的agent

1. 创建 `agents/agent-[name].md`
2. 遵循现有agent的格式和约定
3. 在aimen-workflow.md中添加调用
4. 更新workflow-state.md支持新阶段

### 添加新的工具命令

1. 创建 `commands/[tool-name].md`
2. 从aimen-workflow.md调用
3. 文档化在README中

### 定制检查清单

1. 创建 `aimen/templates/checklist-[domain].md`
2. agent-checklist会加载并使用这些模板

## 联系和支持

对于问题或改进建议，请查看：
- 完整工作流文档: `doc/spec-kit-workflow.md`
- Agent架构设计: `doc/agent-architecture.md`
- 项目状态: `aimen/workflow-state.md`

---

**最后更新**: 2025-02-05  
**版本**: 1.0.0  
**维护**: AIMEN项目团队

