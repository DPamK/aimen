# AIMEN

一个开箱即用的自托管 Vibe Coding 助理，让 AI 驱动的开发变得简单易用。

## 为什么选择 AIMEN？

与 spec-kit 等复杂工具不同，AIMEN 的设计理念是**零学习门槛**。你只需要掌握两个命令：

- **`cto`** - 架构设计与需求管理
- **`aimen`** - 任务执行与开发工作流

就这么简单。无需复杂配置，无需陡峭的学习曲线。

## 特性

- **自托管** - 完全掌控你的开发环境
- **多代理支持** - 支持 Claude、Cursor、Copilot、Gemini、Qwen（未来支持）
- **TDD 工作流** - 内置测试驱动开发流程
- **智能任务管理** - 自动化的项目和任务追踪
- **交互式开发** - AI 代理通过引导式问题与你沟通

## 安装

```bash
# 使用 uv
uv sync

# 或开发模式安装
uv pip install -e .
```

## 快速开始

### 1. 初始化项目

```bash
aimen init
```

该命令会在项目中创建 `.aimen/` 目录及必要的配置文件。你可以指定 AI 代理：

```bash
aimen init --agent claude  # 可选: claude, cursor, copilot, gemini, qwen
```

### 2. 使用 CTO 定义需求

使用 `cto` 命令与 AI 架构师讨论你的功能需求：

```bash
cto "我想构建一个用户认证系统"
```

CTO 代理会：
- 询问澄清性问题以理解需求
- 设计技术架构
- 创建结构化的 Program 和 Task 定义
- 为每个任务定义验收标准

### 3. 使用 AIMEN 执行开发

需求定义完成后，使用 `aimen` 命令开始开发：

```bash
aimen
```

AIMEN 代理会：
- 协调专业子代理（developer、tester、debugger）
- 遵循 TDD 原则进行实现
- 自动运行验收脚本
- 按需更新文档

## 项目管理

AIMEN 内置项目管理工具：

```bash
# 创建新项目（Program）
aimen program init "我的功能" -t "功能描述"

# 向项目添加任务
aimen program add P-001 -n "用户登录" -t "实现登录功能" -c "用户可以使用有效凭证登录"

# 查看所有项目和任务
aimen program status

# 查看特定项目
aimen program status P-001

# 设置任务编排
aimen program orch P-001 "按顺序执行: T-001 -> T-002 -> T-003"

# 更新任务状态
aimen program update T-001 --status "🟢"
```

## 开发工作流

AIMEN 遵循结构化的开发流程：

1. **CTO 阶段** - 需求收集与架构设计
2. **开发阶段** - Developer 代理按 TDD 原则实现
3. **测试阶段** - Tester 代理创建验收脚本
4. **调试阶段** - Debugger 代理修复问题（如需要）
5. **文档更新** - 自动更新相关文档

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

