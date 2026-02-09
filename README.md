# AIMEN — AI-driven Development Workflow System

AIMEN 是一个面向“从需求到落地”的 AI 开发工作流系统：通过**主协调器 + 多个专业 Agent**协同推进工作，并用 **SQLite** 持久化追踪 **产品（Product）→ 功能（Feature）→ 任务（Task）** 的全链路状态。

## 核心特性

- **多 Agent 协作工作流**：以统一流程组织从需求澄清到实现交付的步骤  
  `specify → clarify → plan → tasks → analyze → implement`
- **状态管理与可追踪性（SQLite）**：产品 / 功能 / 任务三层管理，并记录状态变更历史
- **脚本化项目管理能力**：提供一组脚本用于初始化数据库、创建/更新产品与功能、拆分任务、查询状态统计等
- **可扩展的 Agent/上下文管理**：支持通过计划文件生成/更新不同模型或平台的 agent 上下文文件（如 Copilot / Claude / Gemini 等）
- **更高效的交互**：通过 AskUserQuestion 风格的问询，在关键决策点快速收集用户偏好与约束

## 适用场景

- 你希望用 AI 推进开发，但又需要**结构化流程**而不是零散对话
- 你需要把“想法 → 计划 → 任务 → 进度”落到可追踪的系统里
- 你希望多种 Agent 分工（产品/架构/实现/测试/发布等）并保持一致上下文

## 快速开始（概览）

> 下面以“初始化数据库 → 新建产品/功能 → 拆任务 → 查询状态”为主线。
> 具体脚本名称与参数以仓库内脚本为准（建议结合 `SKILL.md` 阅读）。

1. 初始化 SQLite 数据库（创建 products/features/tasks/history 等表）
2. 创建一个 Product
3. 在 Product 下创建 Feature，并根据工作流推进状态
4. 为 Feature 拆分 Task，更新任务状态
5. 查询当前工作状态与统计信息（例如当前进行中的功能、任务分布等）

## 工作流说明

AIMEN 推荐的标准节奏：

1. **specify**：把目标写成清晰的需求/规格（范围、用户故事、验收标准）
2. **clarify**：收集关键决策与约束（技术栈、接口、数据、边界情况）
3. **plan**：输出可执行计划（结构、模块拆分、风险点、里程碑）
4. **tasks**：将计划拆成可跟踪任务（依赖、优先级、完成定义）
5. **analyze**：实现前分析与设计校对（避免返工，明确测试策略）
6. **implement**：实现、测试、迭代与交付

## 项目结构（建议）

> 下面是基于最近提交内容的“典型结构”描述；以仓库实际目录为准。

- `README.md`：项目介绍与入口
- `SKILL.md`：项目管理/工作流能力说明
- `*.py`：产品/功能/任务/状态/流转等管理脚本（例如 init_db、product、feature、task、status、transition）
- `project.db`：SQLite 数据库文件（如有提交或本地生成）
- `update-agent-context.ps1`：根据计划文件更新/生成 agent 上下文文件
- `templates/`（或同类目录）：agent 文件、spec/plan/tasks/checklist 等模板

## 使用建议

- 把一个 Feature 当作最小可交付单元：每个 Feature 都有清晰验收标准
- 坚持“先 plan 后 tasks”：先把结构与风险想清楚，再拆分可执行任务
- 状态变更要落库：保证可回溯、可统计、可复盘

## Roadmap（可选）

- 更完整的示例：从 0 到 1 创建一个产品与功能，并展示任务拆分与状态流转
- 增加 CI/自动化：将状态检查、模板生成、任务同步接入流水线
- 更细粒度的 Agent 分工与提示词规范

## License

如仓库包含 LICENSE 文件，请以其为准。
