# .specify/scripts/bash 脚本详细讲解 - 快速参考

## 📋 文件管理矩阵概览

| 脚本 | 主要职责 | 创建文件 | 读取文件 | 修改文件 | 验证内容 |
|------|--------|--------|--------|--------|--------|
| **common.sh** | 提供公共函数库 | - | - | - | ✓ 路径和分支 |
| **check-prerequisites.sh** | 前置条件验证 | - | spec.md, plan.md, tasks.md | - | ✓ 所有特性文件 |
| **create-new-feature.sh** | 创建新特性 | spec.md | spec-template.md | 分支 | ✓ 分支名称 |
| **setup-plan.sh** | 初始化计划 | plan.md | plan-template.md | - | ✓ 分支验证 |
| **update-agent-context.sh** | 更新代理配置 | 代理文件 | plan.md, 代理模板 | 代理文件 | ✓ plan.md 内容 |

---

## 🎯 每个脚本的详细职责

### 1. **common.sh** - 基础工具库

**不是可执行脚本，而是被其他脚本 source 的函数库**

**提供的关键函数**：

```bash
# 获取仓库根目录
get_repo_root() 
  → 返回 git 仓库根目录 或 .specify 文件夹所在目录

# 获取当前分支
get_current_branch()
  → 优先级：SPECIFY_FEATURE 环境变量 > git 分支 > specs/ 目录扫描
  → 返回当前特性分支名（格式：NNN-feature-name）

# 检查 git 可用性
has_git()
  → 返回 true/false

# 验证分支命名规范
check_feature_branch(branch, has_git)
  → 检查分支是否符合 NNN-* 格式
  → 非 git 项目会警告但不报错

# 获取所有特性相关路径
get_feature_paths()
  → 输出一个 bash 代码块，包含所有路径变量：
    REPO_ROOT, CURRENT_BRANCH, HAS_GIT, FEATURE_DIR,
    FEATURE_SPEC, IMPL_PLAN, TASKS, RESEARCH,
    DATA_MODEL, QUICKSTART, CONTRACTS_DIR

# 按前缀查找特性目录
find_feature_dir_by_prefix(repo_root, branch_name)
  → 支持多分支同一特性
  → 如分支为 "001-fix-bug"，查找 specs/001-*

# 文件状态检查
check_file(file_path, display_name)
check_dir(dir_path, display_name)
  → 输出 ✓ 或 ✗ 加文件名
```

**核心能力**：
- ✓ 跨 git 和非 git 项目支持
- ✓ 环境变量降级方案
- ✓ 多分支同特性支持

**管理的文件**：无（仅提供函数）

---

### 2. **check-prerequisites.sh** - 前置条件检查

**职责**：验证特性开发环境的完整性

**执行逻辑**：
```
1. 解析命令行参数
2. Source common.sh，获取所有路径
3. 验证分支命名规范
4. 验证必需文件：
   - feature_dir 必须存在
   - plan.md 必须存在
   - 可选：tasks.md（--require-tasks）
5. 检查可选文档：
   - research.md, data-model.md, contracts/, quickstart.md
6. 输出结果（JSON 或纯文本）
```

**输出模式**：

```bash
# 纯文本输出（默认）
FEATURE_DIR:/path/to/specs/001-feature
AVAILABLE_DOCS:
  ✓ research.md
  ✗ data-model.md
  ✓ contracts/
  ✓ quickstart.md

# JSON 输出（--json）
{
  "FEATURE_DIR": "/path/to/specs/001-feature",
  "AVAILABLE_DOCS": ["research.md", "contracts/", "quickstart.md"]
}

# 仅路径输出（--paths-only）
REPO_ROOT: /path
BRANCH: 001-feature
FEATURE_DIR: /path/to/specs/001-feature
FEATURE_SPEC: /path/to/specs/001-feature/spec.md
...
```

**关键参数**：
- `--json` - JSON 格式输出（便于自动化）
- `--require-tasks` - 要求 tasks.md 存在（实现阶段使用）
- `--include-tasks` - 将 tasks.md 加入可用文档列表
- `--paths-only` - 仅返回路径，跳过验证

**管理的文件**：
- **读取**：spec.md, plan.md, tasks.md（可选）, research.md, data-model.md, contracts/*, quickstart.md
- **不修改任何文件**，仅验证

**使用场景**：
```bash
# 1. 验证是否可以继续工作
check-prerequisites.sh --json

# 2. 实现阶段需要验证 tasks.md
check-prerequisites.sh --json --require-tasks --include-tasks

# 3. 获取路径信息给其他脚本使用
eval $(check-prerequisites.sh --paths-only)
```

---

### 3. **create-new-feature.sh** - 创建新特性

**职责**：初始化新特性分支和目录结构

**执行流程**：

```
1. 解析命令行参数
   - 特性描述
   - 可选：--short-name （自定义短名）
   - 可选：--number N （指定分支号）
   - 可选：--json （JSON 输出）

2. 查找仓库根目录
   - 优先使用 git rev-parse
   - 备选方案：搜索 .git 或 .specify 文件夹

3. 生成分支名
   if short-name 指定:
      用指定名称 clean 后作为后缀
   else:
      从特性描述智能提取：
      - 移除停用词（the, a, to, for, is, are 等）
      - 保留有意义的单词
      - 限制 3-4 个单词
      - 转小写、处理特殊字符

4. 确定分支编号
   if --number 指定:
      使用指定编号
   else:
      扫描 git 分支和 specs/ 目录
      取最高编号 + 1
      支持远程分支同步（git fetch --all）

5. 格式化分支名
   格式：NNN-suffix
   检查长度不超过 244 字节（GitHub 限制）
   如超过，自动截断并警告

6. 创建分支和目录
   if git repo:
      git checkout -b 001-feature-name
   else:
      警告：Git 不可用，跳过分支创建
   
   mkdir -p specs/001-feature-name/

7. 创建 spec.md
   if template 存在:
      cp .specify/templates/spec-template.md specs/.../spec.md
   else:
      touch specs/.../spec.md

8. 输出结果
   文本模式：
      BRANCH_NAME: 001-feature-name
      SPEC_FILE: /path/to/specs/001-feature-name/spec.md
      FEATURE_NUM: 001
      SPECIFY_FEATURE environment variable set to: 001-feature-name
   
   JSON 模式：
      {
        "BRANCH_NAME": "001-feature-name",
        "SPEC_FILE": "/path/to/specs/001-feature-name/spec.md",
        "FEATURE_NUM": "001"
      }
```

**创建的文件**：
```
specs/NNN-feature-name/
└── spec.md              # 从模板复制或创建空文件
```

**创建的 git 对象**：
```
分支：origin/NNN-feature-name
```

**关键参数**：
- `description` - 必需，特性描述
- `--short-name <name>` - 可选，自定义短名
- `--number N` - 可选，手动指定分支号
- `--json` - 可选，JSON 输出

**智能命名特点**：
```
输入："Add comprehensive user authentication system with OAuth2"
停用词过滤：去除 with, and, system 等
输出：user-authentication-oauth2

输入："Create a new feature for payment processing"
停用词过滤：去除 a, new, for, create 等
输出：payment-processing

输入："Fix critical bug in data validation layer"
停用词过滤：去除 in, data 等
输出：fix-critical-bug-validation
```

**编号逻辑**：
```
查询最高编号的来源（优先级）：
1. Git 本地分支中的最高数字
2. Git 远程分支中的最高数字（git fetch 后）
3. specs/ 目录中的最高数字

示例：
  存在：001-auth, 002-payment, 003-reporting
  新建特性 → 004-xxx

多分支同一特性示例：
  004-backend-api
  004-frontend-ui
  第二个分支会复用编号 004，但后缀不同
```

**使用场景**：
```bash
# 1. 基本使用
./create-new-feature.sh "Add user authentication"
# 输出：Branch: 001-user-authentication

# 2. 自定义名称
./create-new-feature.sh "Feature description" --short-name "custom-feature"
# 输出：Branch: 001-custom-feature

# 3. 手动指定编号
./create-new-feature.sh "Feature" --number 5
# 输出：Branch: 005-feature

# 4. JSON 输出（便于自动化）
./create-new-feature.sh "Feature" --json | jq .BRANCH_NAME
```

---

### 4. **setup-plan.sh** - 初始化实现计划

**职责**：为新特性生成 plan.md 计划文件

**执行流程**：

```
1. 解析命令行参数
   - --json （JSON 输出）
   - --help

2. Source common.sh，获取特性路径
   eval $(get_feature_paths)
   获得：REPO_ROOT, CURRENT_BRANCH, FEATURE_DIR 等

3. 验证分支
   check_feature_branch "$CURRENT_BRANCH" "$HAS_GIT"
   确保在有效的特性分支上

4. 创建特性目录（如不存在）
   mkdir -p "$FEATURE_DIR"

5. 从模板复制 plan.md
   if template 存在:
      cp .specify/templates/plan-template.md $FEATURE_DIR/plan.md
   else:
      警告：模板不存在
      touch $FEATURE_DIR/plan.md

6. 输出结果
```

**创建的文件**：
```
specs/NNN-feature-name/
└── plan.md          # 从 plan-template.md 复制
```

**输出格式**：

```bash
# 文本输出
FEATURE_SPEC: /path/to/specs/001-feature/spec.md
IMPL_PLAN: /path/to/specs/001-feature/plan.md
SPECS_DIR: /path/to/specs/001-feature
BRANCH: 001-feature
HAS_GIT: true

# JSON 输出（--json）
{
  "FEATURE_SPEC": "/path/to/specs/001-feature/spec.md",
  "IMPL_PLAN": "/path/to/specs/001-feature/plan.md",
  "SPECS_DIR": "/path/to/specs/001-feature",
  "BRANCH": "001-feature",
  "HAS_GIT": "true"
}
```

**使用场景**：
```bash
# 1. 在创建特性后执行
./create-new-feature.sh "Feature description"
./setup-plan.sh
# 现在特性目录有 spec.md 和 plan.md

# 2. 作为自动化流程的第二步
feature=$(./create-new-feature.sh "Feature" --json | jq -r .BRANCH_NAME)
./setup-plan.sh
# plan.md 已准备好编辑
```

---

### 5. **update-agent-context.sh** - 更新 AI 代理上下文

**职责**：根据 plan.md 更新多个 AI 代理的配置文件

**这是最复杂的脚本（800 行），核心功能如下**：

#### 5.1 环境验证

```bash
validate_environment():
  ✓ 检查 CURRENT_BRANCH 存在
  ✓ 检查 plan.md 文件存在
  ✓ 检查模板文件存在
```

#### 5.2 计划数据提取

从 plan.md 中解析四个关键字段：
```markdown
**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, SQLAlchemy
**Storage**: PostgreSQL
**Project Type**: Web Backend

被提取为：
- NEW_LANG = "Python 3.11"
- NEW_FRAMEWORK = "FastAPI, SQLAlchemy"
- NEW_DB = "PostgreSQL"
- NEW_PROJECT_TYPE = "Web Backend"
```

#### 5.3 代理文件路径管理

支持 17 种代理，存储位置不同：

```bash
# 根目录单一 .md 文件
CLAUDE_FILE = "$REPO_ROOT/CLAUDE.md"
GEMINI_FILE = "$REPO_ROOT/GEMINI.md"
QWEN_FILE = "$REPO_ROOT/QWEN.md"

# 目录结构
COPILOT_FILE = "$REPO_ROOT/.github/agents/copilot-instructions.md"
CURSOR_FILE = "$REPO_ROOT/.cursor/rules/specify-rules.mdc"
WINDSURF_FILE = "$REPO_ROOT/.windsurf/rules/specify-rules.md"

# 还有其他 12 种...
```

#### 5.4 创建新代理文件

```bash
create_new_agent_file(target_file, temp_file, project_name, date):
  1. 验证模板存在
  2. 复制模板到临时文件
  3. 替换占位符：
     [PROJECT NAME]           → aimen
     [DATE]                   → 2024-02-09
     [EXTRACTED FROM ...]     → Python 3.11 + FastAPI
     [ACTUAL STRUCTURE ...]   → backend/\nfrontend/\ntests/
     [ONLY COMMANDS FOR ...]  → cd src && pytest ...
     [LANGUAGE-SPECIFIC ...]  → Python: Follow conventions
     [LAST 3 FEATURES ...]    → - 001-feature: Added Python
  4. 处理 \n 转换为实际换行
  5. 移动临时文件到目标位置
```

#### 5.5 更新现有代理文件

```bash
update_existing_agent_file(target_file, current_date):
  1. 读取现有文件，逐行处理
  
  2. 在 "## Active Technologies" 部分：
     添加新的技术栈条目（防止重复）
     格式：- Python 3.11 + FastAPI (001-feature-name)
  
  3. 在 "## Recent Changes" 部分：
     添加新的变更记录（保留最新 2-3 条）
     格式：- 001-feature: Added Python 3.11
  
  4. 更新时间戳
     找到 **Last updated**: xxxx-xx-xx
     替换为当前日期
  
  5. 原子性替换（避免文件损坏）
     写入临时文件 → 完成后 mv 替换原文件
```

#### 5.6 执行流程

```
调用：./update-agent-context.sh [agent_type]

if agent_type 指定:
   只更新该代理
else:
   扫描所有已配置代理，全部更新
   如没有任何代理，创建默认 Claude.md

执行步骤：
1. validate_environment()
2. parse_plan_data(plan.md)
   → 提取 NEW_LANG, NEW_FRAMEWORK, NEW_DB, NEW_PROJECT_TYPE
3. for each agent:
   if agent_file 不存在:
      create_new_agent_file()
   else:
      update_existing_agent_file()
4. print_summary()
```

#### 5.7 支持的代理

```
16 种代理（完整列表）：
- Claude Code              → CLAUDE.md
- Gemini CLI               → GEMINI.md
- GitHub Copilot           → .github/agents/copilot-instructions.md
- Cursor IDE               → .cursor/rules/specify-rules.mdc
- Qwen Code                → QWEN.md
- opencode                 → AGENTS.md
- Codex CLI                → AGENTS.md
- Windsurf                 → .windsurf/rules/specify-rules.md
- Kilo Code                → .kilocode/rules/specify-rules.md
- Auggie CLI               → .augment/rules/specify-rules.md
- Roo Code                 → .roo/rules/specify-rules.md
- CodeBuddy CLI            → CODEBUDDY.md
- Qoder CLI                → QODER.md
- Amp                      → AGENTS.md
- SHAI                     → SHAI.md
- Amazon Q Developer CLI   → AGENTS.md
- IBM Bob                  → AGENTS.md
```

**使用场景**：

```bash
# 1. 更新所有现有代理
./update-agent-context.sh
# 自动查找并更新 CLAUDE.md, GEMINI.md 等

# 2. 只更新 Claude
./update-agent-context.sh claude

# 3. 仅更新 Copilot
./update-agent-context.sh copilot

# 4. 由 setup-plan 或其他脚本调用
# 完成编辑 plan.md 后自动运行
./update-agent-context.sh  # 无参数，全部更新
```

---

## 📊 脚本执行顺序和依赖

```
用户工作流：

第 1 步：create-new-feature.sh
  ├─ 创建分支：001-feature-name
  ├─ 创建目录：specs/001-feature-name/
  ├─ 生成文件：specs/001-feature-name/spec.md
  └─ 输出：BRANCH_NAME, SPEC_FILE, FEATURE_NUM

第 2 步：用户手动编辑 spec.md
  └─ 描述特性的需求和规范

第 3 步：setup-plan.sh
  ├─ 验证分支命名规范
  ├─ 创建目录（如不存在）
  └─ 生成文件：specs/001-feature-name/plan.md

第 4 步：用户手动编辑 plan.md
  └─ 填入实现细节，包括：
     - Language/Version
     - Primary Dependencies
     - Storage
     - Project Type

第 5 步：check-prerequisites.sh --json --include-tasks
  ├─ 验证 spec.md 存在
  ├─ 验证 plan.md 存在
  ├─ 检查其他可选文档
  └─ 输出所有可用文档列表

第 6 步：update-agent-context.sh
  ├─ 解析 plan.md 提取元数据
  ├─ 查找所有代理文件
  ├─ 更新或创建代理配置
  └─ 同步所有 AI 代理

第 7 步：用户编辑 tasks.md
  └─ 创建任务列表
  └─ （这不在这些脚本的管理范围内）

依赖图：
  common.sh
    ↑
    ├─ create-new-feature.sh
    ├─ setup-plan.sh
    ├─ check-prerequisites.sh
    └─ update-agent-context.sh

注意：update-agent-context.sh 需要 plan.md 已编写完成
```

---

## 🔄 文件生命周期管理

```
特性目录结构的演变：

初始（create-new-feature 后）：
specs/001-feature/
└── spec.md          [空或模板内容]

计划阶段（setup-plan 后）：
specs/001-feature/
├── spec.md          [用户编写]
└── plan.md          [空或模板内容]

实现前准备（更新代理后）：
specs/001-feature/
├── spec.md          [完整]
├── plan.md          [完整]
├── research.md      [可选]
├── data-model.md    [可选]
├── contracts/       [可选，文件夹]
└── quickstart.md    [可选]

实现中（创建 tasks.md）：
specs/001-feature/
├── spec.md          [完整]
├── plan.md          [完整]
├── tasks.md         [用户创建]
├── research.md      [可选]
├── data-model.md    [可选]
├── contracts/       [可选]
└── quickstart.md    [可选]

代理文件（遍布项目根目录）：
project-root/
├── CLAUDE.md
├── GEMINI.md
├── QWEN.md
├── .github/agents/copilot-instructions.md
├── .cursor/rules/specify-rules.mdc
├── .windsurf/rules/specify-rules.md
└── [其他代理配置...]
  ↑
  └─ 所有这些由 update-agent-context.sh 维护
```

---

## ⚡ 快速参考表

| 操作 | 使用脚本 | 关键参数 | 输出 |
|------|--------|--------|------|
| 创建新特性 | create-new-feature.sh | description | BRANCH_NAME |
| 初始化计划 | setup-plan.sh | 无 | IMPL_PLAN 路径 |
| 验证完整性 | check-prerequisites.sh | --json | AVAILABLE_DOCS |
| 获取所有路径 | check-prerequisites.sh | --paths-only | 所有路径变量 |
| 更新代理配置 | update-agent-context.sh | [agent_type] | 更新状态 |
| 获取基础路径 | common.sh (source) | 无 | 函数可用 |

---

## 🎓 理解关键概念

### 特性编号（Feature Number）
- **格式**：3 位数字（001, 002, 003...）
- **作用**：分支的唯一标识，按创建顺序递增
- **用途**：在多分支支持中，不同分支可以共用同一编号
- **示例**：
  ```
  001-auth-backend
  001-auth-frontend  ← 同一个编号，不同的功能分支
  ```

### 分支命名规范
- **格式**：NNN-suffix
- **NNN**：3 位数字编号
- **suffix**：短名称（多单词用 `-` 分隔）
- **示例**：
  ```
  001-user-authentication
  002-payment-integration
  003-reporting-dashboard
  ```

### 模板驱动
- 所有文件都从模板生成
- 模板位置：`.specify/templates/`
- 模板类型：
  - `spec-template.md` - 特性规范模板
  - `plan-template.md` - 实现计划模板
  - `agent-file-template.md` - 代理配置模板

### 双向支持
- **支持 Git 项目**
  - 创建 git 分支
  - 检查远程分支
  - git hooks 集成
  
- **支持非 Git 项目**
  - 通过 `specs/` 目录管理
  - 通过环境变量 `SPECIFY_FEATURE` 指定
  - 功能基本相同，仅无分支操作

---

## 💡 最佳实践

```bash
# 1. 总是按顺序执行
create-new-feature → setup-plan → check-prerequisites → update-agent-context

# 2. 使用 JSON 输出便于脚本集成
./create-new-feature.sh "feature" --json | jq .BRANCH_NAME

# 3. 定期运行验证
check-prerequisites.sh --json --include-tasks

# 4. 修改 plan.md 后自动更新代理
update-agent-context.sh

# 5. 支持环境变量设置（非 git 项目）
export SPECIFY_FEATURE=001-my-feature
./setup-plan.sh
```

