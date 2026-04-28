# AIMEN Agent Instructions

你正在一个使用 AIMEN Quick 模式的项目中工作。Quick 模式强调快速理解需求、自动实现、自动验收，并在完成后简洁汇报。

## 项目上下文

- 开始任务前，优先读取 `.aimen/identity.md`、`.aimen/memory.md`、`.aimen/consituation.md` 和 `.aimen/worklog.md`（如果存在）。
- 如果缺少必要上下文，先根据当前代码和用户输入做保守判断；无法安全判断时，通过 {{QUESTION_TOOL}} 询问用户。
- 重要工作节点需要记录到 `.aimen/worklog.md`。

## 工作原则

- 先提取用户需求中的目标、边界和最小验收条件。
- 优先复用项目现有架构、工具链、测试方式和代码风格。
- 能自动验证的改动必须运行验证；无法验证时说明原因。
- 不要硬编码密钥、Token、账号、密码或其他敏感信息。

## AIMEN 命令

- `aimen program status [project_id] [task_id]`：查看 Project 或 Task 状态。
- `aimen program update <id> ...`：更新 Project 或 Task 状态、说明、备注、验收标准等字段。
- `aimen memory init`：初始化 AIMEN 记忆文件。

## Sub Agent 分工

- `developer`：负责功能实现。
- `cto`：负责技术方案和疑难分析。
- `debuger`：负责运行错误和缺陷修复。

当工具支持 sub agent 时，优先根据职责分派任务；当工具不支持时，按照上述职责在当前会话中模拟分阶段执行。
