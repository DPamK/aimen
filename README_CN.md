# AIMEN

一个开箱即用的自托管 Vibe Coding 助理，让 AI 驱动的开发变得简单易用。

## 为什么选择 AIMEN？

与 spec-kit 等复杂工具不同，AIMEN 的设计理念是**零学习门槛**。你只需要掌握两个命令：

- **`cto`** - 架构设计与需求管理
- **`aimen`** - 任务执行与开发工作流

就这么简单。无需复杂配置，无需陡峭的学习曲线。

## 特性

- **自托管** - 完全掌控你的开发环境
- **多代理支持** - 支持 Claude Code、OpenCode、Cursor、GitHub Copilot（Gemini、Qwen 即将支持）
- **两种模式** - Dev 模式（完整开发流）和 Quick 模式（极速 MVP）
- **YOLO 模式** - 全自动执行，无需逐步确认
- **TDD 工作流** - 内置测试驱动开发流程
- **智能任务管理** - 自动化的项目和任务追踪
- **交互式开发** - AI 代理通过引导式问题与你沟通

## 安装

```bash
# 安装为全局工具
uv tool install git+https://github.com/DPamK/aimen.git

# 或克隆后本地安装
git clone https://github.com/DPamK/aimen.git
cd aimen
uv tool install .
```

## 快速开始

### 初始化项目

```bash
aimen init
```

该命令会在项目中创建对应的配置目录。你可以指定 AI 代理和模式：

```bash
aimen init --agent claude   # Claude Code    → .claude/
aimen init --agent opencode # OpenCode       → .opencode/
aimen init --agent cursor   # Cursor         → .cursor/
aimen init --agent copilot  # GitHub Copilot → .github/
```

```bash
aimen init --mode dev    # Dev 模式（默认）
aimen init --mode quick  # Quick 模式
```

> **注意：** Gemini 和 Qwen 支持即将推出。

## 模式

AIMEN 提供两种工作模式，适配不同场景：

### Dev 模式
适合生产级功能开发的完整工作流。
- `/cto` 和 `/aimen` 分开调用，首先由 CTO 进行需求设计，再由 AIMEN 协调开发、测试、调试各子代理执行
- 全程遵循严格的 TDD 原则
- 适合对开发流程有更多昸制的场景

### Quick 模式
适合快速构建 MVP 的极速工作流。
- CTO 作为 AIMEN 的内置子代理运行
- AIMEN 根据需要自动调用 CTO，减少手动切换步骤
- 更少的操作步骤，更快的迭代速度

### YOLO 模式
Dev 和 Quick 模式均支持 **YOLO 模式** —— 全自动、无需确认。
开启 YOLO 后，AIMEN 将不再在每个步骤中待待你的确认，端到端全自动执行整个工作流。选择此模式意味着你完全信任 AI 自主完成任务。

## 代理角色

| 代理 | 角色 |
|------|------|
| **CTO** | 架构设计、需求分析、任务拆解 |
| **AIMEN** | 主协调器，管理工作流和沟通 |
| **Developer** | 按 TDD 原则编写代码 |
| **Tester** | 创建验收脚本 |
| **Debugger** | 修复 Bug 和处理失败 |

## 目录结构

```
.aimen/
├── consituation.md    # 项目上下文和配置
├── memory.md          # 开发记忆和关键笔记
├── identity.md        # 用户身份偏好
├── notebook_CTO.md    # CTO 的工作笔记
└── verify/            # 验收脚本
    └── verify_*.py
```

