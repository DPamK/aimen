# .specify/scripts/bash 脚本详细分析

## 一、各脚本详细功能说明

### 1. **common.sh** - 基础函数库
**职责**：为所有脚本提供公共工具函数

**核心功能**：
- `get_repo_root()` - 获取仓库根目录（支持 git 和非 git 项目）
- `get_current_branch()` - 获取当前分支名（支持 SPECIFY_FEATURE 环境变量、git、spec 目录）
- `has_git()` - 检查是否为 git 仓库
- `check_feature_branch()` - 验证分支命名规范（格式：NNN-feature-name）
- `get_feature_dir()` - 获取特性目录
- `find_feature_dir_by_prefix()` - 按数字前缀查找特性目录（支持多分支同一特性）
- `get_feature_paths()` - 获取所有特性相关路径集合
- `check_file()` / `check_dir()` - 文件/目录状态检查

**管理的文件结构**：
```
specs/
  NNN-feature-name/
    spec.md              # 特性规范文档
    plan.md              # 实现计划
    tasks.md             # 任务列表
    research.md          # 研究/调研文档（可选）
    data-model.md        # 数据模型（可选）
    quickstart.md        # 快速开始指南（可选）
    contracts/           # API 契约文件夹（可选）
```

---

### 2. **check-prerequisites.sh** - 前置条件检查
**职责**：验证特性开发环境的完整性

**核心功能**：
- 验证特性目录存在
- 验证必需文件存在（plan.md）
- 可选验证 tasks.md（实现阶段使用）
- 检查可选文档（research.md, data-model.md, contracts/, quickstart.md）
- 支持 JSON 输出和纯文本输出

**输出模式**：
```bash
# JSON 模式（用于自动化）
{
  "FEATURE_DIR": "/path/to/specs/001-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md", "contracts/", "quickstart.md"]
}

# 路径模式（仅返回路径，不验证）
REPO_ROOT: /path
BRANCH: 001-feature
FEATURE_DIR: /path/to/specs/001-feature
```

**命令行选项**：
- `--json` - JSON 输出
- `--require-tasks` - 要求 tasks.md 存在
- `--include-tasks` - 将 tasks.md 加入可用文档列表
- `--paths-only` - 仅返回路径变量（跳过验证）

---

### 3. **create-new-feature.sh** - 创建新特性
**职责**：初始化新特性分支和目录结构

**核心功能**：
- 生成特性分支名（格式：NNN-feature-name）
  - 智能命名：停用词过滤（the, a, to, for 等）
  - 长度限制：符合 GitHub 244 字节限制
  - 支持自定义短名称和分支号
  
- 自动编号逻辑：
  - 检查 git 分支和 specs/ 目录中的最高编号
  - 支持 git fetch 远程分支同步
  - 自动递增编号
  
- 创建分支和目录：
  - 使用 `git checkout -b` 创建分支（git 项目）
  - 创建 specs/NNN-feature-name 目录
  - 从模板复制 spec.md

**参数**：
```bash
./create-new-feature.sh "Feature description" \
  [--short-name "custom-name"] \
  [--number N] \
  [--json]
```

**输出**：
```json
{
  "BRANCH_NAME": "001-feature-name",
  "SPEC_FILE": "/path/to/specs/001-feature-name/spec.md",
  "FEATURE_NUM": "001"
}
```

---

### 4. **setup-plan.sh** - 设置实现计划
**职责**：初始化特性的实现计划文件

**核心功能**：
- 验证当前在有效的特性分支
- 创建特性目录（如不存在）
- 从模板复制 plan.md
- 验证分支命名规范

**输出**：
```json
{
  "FEATURE_SPEC": "/path/to/specs/NNN-feature/spec.md",
  "IMPL_PLAN": "/path/to/specs/NNN-feature/plan.md",
  "SPECS_DIR": "/path/to/specs/NNN-feature",
  "BRANCH": "NNN-feature",
  "HAS_GIT": "true/false"
}
```

---

### 5. **update-agent-context.sh** - 更新 AI 代理上下文
**职责**：根据 plan.md 自动更新多个 AI 代理的配置文件

**核心功能**：

#### 环境验证
- 验证特性分支存在
- 验证 plan.md 存在
- 验证代理模板存在

#### 计划数据解析
从 plan.md 中提取：
- Language/Version（编程语言）
- Primary Dependencies（主要框架）
- Storage（存储/数据库）
- Project Type（项目类型）

#### 代理文件管理
支持 17 种 AI 代理：
- **文件型**：Claude、Gemini、Qwen、SHAI 等（单一 .md 文件）
- **目录型**：Copilot（`.github/agents/`）、Cursor（`.cursor/`）、Windsurf（`.windsurf/`）

#### 内容生成与更新
新建文件时：
- 从模板生成
- 替换占位符：[PROJECT NAME]、[DATE] 等
- 生成项目结构、构建命令、语言约定

更新文件时：
- 添加新的技术栈（保证不重复）
- 更新最近变更（保留最新 2-3 条）
- 更新时间戳

**支持的代理**：
```
claude, gemini, copilot, cursor-agent, qwen, opencode, codex, 
windsurf, kilocode, auggie, roo, codebuddy, shai, q (Amazon Q), 
bob (IBM Bob), qoder
```

**代理文件位置示例**：
```
CLAUDE.md                                    # Claude Code
GEMINI.md                                    # Gemini CLI
.github/agents/copilot-instructions.md      # GitHub Copilot
.cursor/rules/specify-rules.mdc              # Cursor IDE
.windsurf/rules/specify-rules.md             # Windsurf
QWEN.md                                      # Qwen Code
```

**参数**：
```bash
./update-agent-context.sh [agent_type]
# agent_type: claude|gemini|copilot|cursor-agent 等
# 空表示更新所有现有代理文件
```

---

## 二、文件管理映射表

| 脚本 | 创建文件 | 读取文件 | 更新文件 | 验证文件 |
|------|--------|--------|--------|--------|
| **common.sh** | - | - | - | 特性目录结构 |
| **check-prerequisites.sh** | - | spec.md, plan.md, tasks.md, 可选文件 | - | 所有特性文件 |
| **create-new-feature.sh** | spec.md | spec-template.md | - | 分支名称 |
| **setup-plan.sh** | plan.md | plan-template.md | - | 分支验证 |
| **update-agent-context.sh** | 代理文件 | plan.md, agent-template | 代理文件 | plan.md 内容 |

**特性目录文件完整清单**：
```
specs/NNN-feature-name/
├── spec.md                 # 特性规范（必需）- create-new-feature.sh 创建
├── plan.md                 # 实现计划（必需）- setup-plan.sh 创建
├── tasks.md                # 任务列表（可选）- 外部工具创建
├── research.md             # 调研文档（可选）- 手动创建
├── data-model.md           # 数据模型（可选）- 手动创建
├── quickstart.md           # 快速指南（可选）- 手动创建
└── contracts/              # API 契约目录（可选）- 手动创建
    ├── api-contract.md
    └── ...
```

**项目根目录代理文件清单**：
```
repo-root/
├── CLAUDE.md                               # Claude Code
├── GEMINI.md                               # Gemini CLI
├── QWEN.md                                 # Qwen Code
├── SHAI.md                                 # SHAI
├── CODEBUDDY.md                            # CodeBuddy CLI
├── QODER.md                                # Qoder CLI
├── AGENTS.md                               # opencode/Codex/Amazon Q/IBM Bob
├── .github/agents/copilot-instructions.md  # GitHub Copilot
├── .cursor/rules/specify-rules.mdc         # Cursor IDE
├── .windsurf/rules/specify-rules.md        # Windsurf
├── .kilocode/rules/specify-rules.md        # Kilo Code
├── .augment/rules/specify-rules.md         # Auggie CLI
└── .roo/rules/specify-rules.md             # Roo Code
```

---

## 三、执行流程图

```
用户执行流程：
1. create-new-feature "Feature description"
   └─> 创建分支 001-feature-name
   └─> 创建 specs/001-feature-name/ 目录
   └─> 创建 specs/001-feature-name/spec.md

2. setup-plan
   └─> 从模板复制 plan.md

3. 编辑 plan.md 填入项目信息

4. check-prerequisites --json
   └─> 验证 spec.md 和 plan.md 存在
   └─> 检查可选文档

5. update-agent-context [agent_type]
   └─> 解析 plan.md
   └─> 生成或更新代理配置文件
```

---

## 四、模板文件位置

```
.specify/templates/
├── spec-template.md        # 特性规范模板（create-new-feature.sh 使用）
├── plan-template.md        # 实现计划模板（setup-plan.sh 使用）
└── agent-file-template.md  # 代理配置模板（update-agent-context.sh 使用）
```

---

## 五、环境变量支持

| 变量 | 用途 | 优先级 |
|------|------|-------|
| `SPECIFY_FEATURE` | 强制指定当前特性名 | 最高（优先于 git 分支） |
| `GIT_BRANCH` | git 自动获取 | 中等 |
| 文件系统扫描 | 在非 git 项目中自动查找 | 最低 |

---

## 六、关键设计特点

### 1. **非 Git 项目支持**
- 所有脚本都有 git 检测和备用逻辑
- 通过 `SPECIFY_FEATURE` 环境变量指定特性
- 通过 `specs/` 目录扫描编号自动递增

### 2. **灵活的路径解析**
- 支持多分支同一特性（通过前缀查找）
- 编号 (NNN) 作为特性的唯一标识

### 3. **模板驱动**
- 所有文件创建都从模板生成
- 模板占位符自动替换
- 便于修改生成内容

### 4. **多代理支持**
- 自动同步多个 AI 代理的配置
- 支持新增和更新两种模式
- 防止重复条目

### 5. **JSON 支持**
- 所有脚本支持 JSON 输出
- 便于自动化工具集成
- 易于跨平台使用

---

## 七、数据流

```
spec.md (用户编写)
  ↓
plan.md (setup-plan 生成模板 + 用户编写)
  ↓
check-prerequisites (验证完整性)
  ↓
update-agent-context (解析 plan → 更新代理文件)
  ↓
tasks.md (外部工具生成，不在这些脚本管理范围)
  ↓
代理文件 (多个，如 CLAUDE.md、Copilot 等)
```

