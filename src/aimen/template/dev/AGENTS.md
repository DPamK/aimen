# AIMEN Agent Instructions

你正在一个使用 AIMEN 工作流管理需求、任务和开发状态的项目中工作。

## 项目上下文

- 开始执行任务前，优先读取 `.aimen/identity.md`、`.aimen/memory.md`、`.aimen/consituation.md` 和 `.aimen/worklog.md`（如果存在）。
- 需求、Project 和 Task 状态由 `aimen program` 命令维护。
- 重要工作节点需要记录到 `.aimen/worklog.md`。

## 工作原则

- 先理解当前 Project 和 Task 的状态，再进行开发、测试或修复。
- 涉及不明确需求、权限、认证、外部服务或敏感配置时，需要通过 {{QUESTION_TOOL}} 向用户确认。
- 不要硬编码密钥、Token、账号、密码或其他敏感信息。
- 修改代码前先阅读相关上下文，遵循项目现有结构和风格。
- 对功能开发保持 TDD 倾向：先明确验收标准，优先补测试，再实现功能。

## AIMEN 命令

- `aimen program status [project_id] [task_id]`：查看 Project 或 Task 状态。
- `aimen program update <id> ...`：更新 Project 或 Task 状态、说明、备注、验收标准等字段。
- `aimen memory init`：初始化 AIMEN 记忆文件。

## Sub Agent 分工

- `developer`：负责功能开发。
- `tester`：负责验收脚本和测试补充。
- `debuger`：负责缺陷定位和修复。

当工具支持 sub agent 时，优先根据职责分派任务；当工具不支持时，按照上述职责在当前会话中模拟分阶段执行。
