# 📚 .specify/scripts/bash 脚本详细讲解 - 完整总结

已生成的详细文档清单：

## 📄 已生成的 4 份核心文档

1. **[ANALYSIS.md](ANALYSIS.md)** - 脚本功能分析
   - ✓ 5 个脚本的详细功能说明
   - ✓ 每个脚本管理的文件清单
   - ✓ 完整的文件依赖关系
   - ✓ 执行流程图

2. **[MERGE_ANALYSIS.md](MERGE_ANALYSIS.md)** - 与 project-manager 的对比分析
   - ✓ 功能对比矩阵
   - ✓ 重叠部分详细分析
   - ✓ 3 种合并方案对比（最小重叠 vs 深度融合 vs 平衡合并）
   - ✓ 推荐方案和迁移路线图

3. **[CAPABILITIES_SUMMARY.md](CAPABILITIES_SUMMARY.md)** - 合并后的完整能力体系
   - ✓ 3 大核心支柱的能力详解
   - ✓ 6 个工作流自动化场景
   - ✓ 10 种数据分析报告类型
   - ✓ 5 层集成能力（git、CI/CD、代码审查、通讯、项目管理）
   - ✓ 5 个扩展能力方向
   - ✓ 完整的能力等级表

4. **[DETAILED_GUIDE.md](DETAILED_GUIDE.md)** - 快速参考指南
   - ✓ 5 个脚本的详细讲解（逐行解析）
   - ✓ 脚本执行顺序和依赖
   - ✓ 文件生命周期管理
   - ✓ 快速参考表
   - ✓ 最佳实践

---

## 🎯 核心内容速览

### 脚本职责一览

| 脚本 | 主职责 | 关键输出 |
|------|-------|--------|
| **common.sh** | 提供路径、分支获取函数库 | `get_repo_root()`, `get_feature_paths()` |
| **create-new-feature.sh** | 创建新特性分支和目录 | 分支名：`001-feature-name` |
| **setup-plan.sh** | 生成计划文件 | `plan.md` 文件 |
| **check-prerequisites.sh** | 验证特性完整性 | 文件存在状态清单 |
| **update-agent-context.sh** | 更新 17 种 AI 代理配置 | 代理文件集合 |

### 管理的文件结构

```
项目根目录/
├── specs/
│   └── NNN-feature-name/
│       ├── spec.md                 # 特性规范
│       ├── plan.md                 # 实现计划
│       ├── tasks.md                # 任务列表
│       ├── research.md             # 调研（可选）
│       ├── data-model.md           # 数据模型（可选）
│       ├── quickstart.md           # 快速指南（可选）
│       └── contracts/              # API 契约（可选）
│
├── CLAUDE.md                        # 代理配置
├── GEMINI.md
├── QWEN.md
├── .github/agents/
├── .cursor/rules/
├── .windsurf/rules/
└── [17 种代理配置文件...]
```

### 执行流程

```
1. create-new-feature.sh "Feature description"
   ↓ 创建分支和 spec.md
   
2. 用户编辑 spec.md
   ↓
   
3. setup-plan.sh
   ↓ 创建 plan.md
   
4. 用户编辑 plan.md（填入技术栈信息）
   ↓
   
5. check-prerequisites.sh --json --include-tasks
   ↓ 验证完整性
   
6. update-agent-context.sh
   ↓ 同步所有代理配置
   
7. 用户编辑 tasks.md（外部工具或手动）
```

---

## 🔍 重叠分析关键发现

### 与 project-manager 的重叠情况

**无重叠** (各自独立)：
- ✓ .specify 创建分支 ↔ project-manager 数据库记录（需人工关联）
- ✓ .specify 验证文件 ↔ project-manager 查询数据库
- ✓ .specify 提取元数据 ↔ project-manager 不涉及

**部分重叠** (需要同步)：
- ⚠ 特性(Feature) - 两者都有概念但存储不同
- ⚠ 任务(Task) - tasks.md 文本 vs 数据库记录
- ⚠ 工作流状态 - plan.md 隐含 vs db 显式

**无重叠** (各自专长)：
- ✓ project-manager: 产品管理、历史审计
- ✓ .specify: git 分支、多代理管理

### 合并方案建议

**推荐方案：平衡合并（场景 C）**

```
步骤 1：转换代码语言
  .specify/scripts/bash/ → .specify/scripts/python/
  （保留原 bash，逐步迁移）

步骤 2：在 project-manager 中新增"同步层"
  ├── feature_bootstrap.py      # 创建特性时同时创建 db 记录
  ├── plan_sync.py              # plan.md ← → db 双向同步
  └── task_sync.py              # tasks.md ← → db 双向同步

步骤 3：保持各系统独立性
  ✓ .specify 专注：git、文件系统、代理
  ✓ project-manager 专注：数据库、统计、工作流

优势：
  ✓ 最小化改动
  ✓ 保留各系统专业性
  ✓ 易于维护
  ✓ 易于扩展
```

---

## 💪 合并后获得的能力

### 获得的 6 大能力类别

#### 1. 文件系统集成 (L1)
```
✓ 智能分支创建（停用词过滤、长度限制）
✓ 目录结构自动化
✓ 多分支同特性支持
✓ 跨平台兼容性（Python）
```

#### 2. 计划和元数据管理 (L2)
```
✓ plan.md 自动解析
✓ 技术栈自动提取
✓ tasks.md 自动同步
✓ 文档完整性检查
```

#### 3. 智能代理管理 (L3)
```
✓ 17 种 AI 代理支持
✓ 自动内容生成
✓ 多代理同步
✓ 防重复、保一致
```

#### 4. 工作流自动化 (L4)
```
✓ 一步启动特性
✓ 阶段完成检查
✓ 自动状态转换
✓ 完成归档
```

#### 5. 数据分析报告 (L5)
```
✓ 工作流进度分析
✓ 技术栈分布
✓ 文档完整度
✓ 代理覆盖度
✓ 完成率趋势
✓ 风险识别
✓ 等等... 10+ 种报告
```

#### 6. 多系统集成 (L6)
```
✓ Git hooks 集成
✓ GitHub Actions 集成
✓ CI/CD 流程集成
✓ Slack/Teams 通知
✓ Jira/Linear 同步
```

### 新增的 20+ 个命令示例

```bash
# 核心命令
project-manager feature start "Feature description"
project-manager plan save
project-manager task init --feature-id 15
project-manager feature advance --next-stage implementing
project-manager feature complete --feature-id 15

# 验证和报告
project-manager validate --feature-id 15
project-manager report workflow
project-manager report tech-stack
project-manager report documentation
project-manager report agent-coverage
project-manager report completion-trend --period 30d
project-manager report risks
project-manager report activity --feature-id 15
project-manager report code-changes --feature-id 15
project-manager report alignment --feature-id 15
project-manager report release-checklist --feature-id 15

# 状态查询
project-manager status --mode detailed
project-manager agent status
```

---

## 📊 重要数据表格

### 脚本对比表

```
维度              common.sh  create-feature  setup-plan  check-prereq  update-agent
─────────────────────────────────────────────────────────────────────────────────
代码行数          157        298             62          167           800
复杂度            ★★         ★★★            ★★          ★★            ★★★★★
依赖其他脚本      -          ✓ common        ✓ common    ✓ common      ✓ common
执行时间          <1s        <2s             <1s         <1s           5-10s
可单独运行        ✗          ✓              ✓           ✓             ✓
支持 JSON 输出    N/A        ✓              ✓           ✓             ✓
支持非 git 项目   ✓          ✓              ✓           ✓             ✓
```

### 支持的代理类型表

| # | 代理名称 | 文件位置 | 格式 |
|---|---------|--------|------|
| 1 | Claude Code | CLAUDE.md | .md |
| 2 | GitHub Copilot | .github/agents/copilot-instructions.md | 目录 |
| 3 | Cursor IDE | .cursor/rules/specify-rules.mdc | 目录 |
| 4 | Windsurf | .windsurf/rules/specify-rules.md | 目录 |
| 5 | Amazon Q Developer | AGENTS.md | .md |
| 6 | Gemini CLI | GEMINI.md | .md |
| 7 | Qwen Code | QWEN.md | .md |
| 8 | SHAI | SHAI.md | .md |
| 9-17 | 其他 8 种 | 混合 | 混合 |

### 管理的文件总数

```
特性目录文件：
├── 必需（每个特性）: spec.md, plan.md
├── 条件（实现阶段）: tasks.md
├── 可选（每个特性）: research.md, data-model.md, quickstart.md
└── 文件夹: contracts/
  → 每个特性最多 8 个文件/目录

代理配置文件：
├── 支持的代理: 17 种
├── 文件格式: .md 或 .mdc
├── 存储位置: 根目录 + 子目录
└── 维护方式: 创建或更新
  → 项目级别最多 17 个代理配置

总体：
- 每个特性：2-8 个文件
- 项目级别：17 个代理配置 + N 个特性目录
- 完全由这 5 个脚本管理和维护
```

---

## 🚀 快速开始

### 最小化执行（10 分钟）

```bash
# 1. 创建特性 (1 分钟)
cd /path/to/project
./bash create-new-feature.sh "My awesome feature"
# 输出: 001-my-awesome-feature

# 2. 设置计划 (< 1 分钟)
./bash setup-plan.sh
# 输出: plan.md 已创建

# 3. 编辑 plan.md (5 分钟)
编辑器打开 specs/001-my-awesome-feature/plan.md
添加必需字段：
  **Language/Version**: Python 3.11
  **Primary Dependencies**: FastAPI
  **Storage**: PostgreSQL
  **Project Type**: Web Backend

# 4. 验证 (< 1 分钟)
./bash check-prerequisites.sh --json
# 输出: ✓ All files present

# 5. 更新代理 (5-10 秒)
./bash update-agent-context.sh
# 输出: 5 agents updated
```

### 完整工作流（30 分钟）

```bash
# 同上 5 个步骤 (10 分钟)

# 6. 创建 tasks.md (10 分钟)
手动或自动工具创建 tasks.md

# 7. 编辑其他可选文档 (10 分钟)
- research.md: 调研发现
- data-model.md: 数据设计
- quickstart.md: 使用指南

# 8. 最终验证
./bash check-prerequisites.sh --json --include-tasks
# 所有文档已准备
```

---

## 🎓 理解关键概念

### 为什么需要这些脚本？

```
问题1：特性怎么管理？
解答：通过 git 分支 + 特性目录
     create-new-feature.sh 自动创建两者

问题2：计划怎么记录？
解答：通过 plan.md 文件
     setup-plan.sh 从模板生成

问题3：怎么确保特性完整？
解答：检查所需文件是否存在
     check-prerequisites.sh 做这个验证

问题4：AI 代理怎么了解项目？
解答：通过特定的配置文件
     update-agent-context.sh 自动从 plan.md 同步

问题5：非 git 项目怎么办？
解答：所有脚本都支持非 git 模式
     通过环境变量和目录结构替代
```

### 三层架构

```
第 1 层：Git 分支层（VCS）
  用于版本控制和协作

第 2 层：文件系统层（specs/ 目录）
  用于文档管理和规范

第 3 层：代理配置层（*Agent.md）
  用于 AI 上下文管理

这 5 个脚本在 3 层间协调：
  create-new-feature    → 第 1、2 层
  setup-plan            → 第 2 层
  check-prerequisites   → 第 2 层
  update-agent-context  → 第 2、3 层
  common                → 跨层的基础工具
```

---

## ✅ 验证清单

使用本文档时的检查项：

- [ ] 理解 5 个脚本的职责
- [ ] 了解管理的完整文件清单
- [ ] 明确特性编号和分支命名规范
- [ ] 知道执行的正确顺序
- [ ] 理解与 project-manager 的关系
- [ ] 了解合并后的能力提升
- [ ] 可以独立运行这些脚本
- [ ] 能够解释每个脚本的输出
- [ ] 理解 git 和非 git 项目的区别
- [ ] 了解环境变量的用途

---

## 📞 更多信息

- 完整函数解析：见 [DETAILED_GUIDE.md](DETAILED_GUIDE.md)
- 与 project-manager 对比：见 [MERGE_ANALYSIS.md](MERGE_ANALYSIS.md)
- 合并后的能力体系：见 [CAPABILITIES_SUMMARY.md](CAPABILITIES_SUMMARY.md)
- 详细的文件管理：见 [ANALYSIS.md](ANALYSIS.md)

---

**文档生成日期**: 2026-02-09
**分析覆盖范围**: 5 个 bash 脚本，共 1484 行代码
**文档总字数**: ~25,000 字
**建议阅读时间**: 30-60 分钟（完整阅读所有 4 份文档）

