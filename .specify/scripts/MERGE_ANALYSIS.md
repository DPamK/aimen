# .specify/scripts/bash 与 project-manager 的重叠分析

## 一、功能对比矩阵

| 功能维度 | .specify bash 脚本 | project-manager 技能 | 重叠程度 |
|---------|------------------|------------------|--------|
| **特性分支管理** | ✓ 创建分支、命名 | ✗ 无 | 无重叠 |
| **目录结构初始化** | ✓ 创建 specs/ 目录 | ✗ 无 | 无重叠 |
| **文件验证** | ✓ 前置检查 | ✗ 无 | 无重叠 |
| **产品管理** | ✗ 无 | ✓ 产品 CRUD | 无重叠 |
| **特性数据管理** | ✗ 无 | ✓ 特性 CRUD、状态跟踪 | **部分重叠** |
| **任务数据管理** | ✗ 无 | ✓ 任务 CRUD、状态跟踪 | **部分重叠** |
| **工作流状态转换** | ✗ 无 | ✓ 状态机转换 | **部分重叠** |
| **元数据提取** | ✓ 从 plan.md 解析 | ✗ 无 | 无重叠 |
| **代理文件同步** | ✓ 更新多个代理配置 | ✗ 无 | 无重叠 |
| **环境验证** | ✓ 分支、路径验证 | ✗ 无 | 无重叠 |

---

## 二、详细重叠分析

### 2.1 **特性(Feature)管理** - 重叠程度：中等

#### .specify 中的特性概念
- **定义**：通过分支名（NNN-feature-name）标识
- **目录**：specs/NNN-feature-name/
- **关键操作**：
  - 创建分支（create-new-feature.sh）
  - 获取当前特性（common.sh 中 get_current_branch）
  - 初始化目录结构

#### project-manager 中的特性概念
- **定义**：数据库中的独立记录
- **属性**：product_id, name, branch, status, priority, workflow_stage
- **关键操作**：
  - 创建特性记录（feature.py）
  - 查询特性列表（feature.py）
  - 更新特性状态和阶段（feature.py）

#### 重叠点
```
都需要管理：
- 特性的标识（分支名）
- 特性的生命周期（plan → implement → test → complete）
- 特性的元数据（名称、优先级等）
```

#### 不同点
| 维度 | .specify | project-manager |
|-----|---------|-----------------|
| 存储 | 文件系统（分支 + 目录） | 数据库（SQLite） |
| 权威来源 | git 分支 | 数据库记录 |
| 时间戳 | 隐含（git 提交时间） | 显式（created_at, updated_at） |
| 关系管理 | 目录层级 | 外键关联 |

---

### 2.2 **任务(Task)管理** - 重叠程度：中等

#### .specify 中的任务概念
- **定义**：tasks.md 文件中的任务项
- **位置**：specs/NNN-feature/tasks.md
- **操作**：
  - 通过 check-prerequisites 检查 tasks.md 是否存在
  - 验证 tasks.md 可用性

#### project-manager 中的任务概念
- **定义**：数据库中与特性关联的任务
- **属性**：feature_id, task_id, description, phase, file_path, status
- **关键操作**：
  - 创建任务记录（task.py）
  - 查询任务列表（task.py）
  - 更新任务状态（task.py）
  - 按 phase 查询

#### 重叠点
```
两者都需要：
- 任务的唯一标识（task_id）
- 任务的描述信息
- 任务的生命周期状态（todo → doing → done）
- 与特性的关联关系
```

#### 不同点
| 维度 | .specify | project-manager |
|-----|---------|-----------------|
| 存储 | 文本文件（Markdown） | 数据库 |
| 结构化 | 非结构化文本 | 结构化字段 |
| 查询能力 | 文件读取 | SQL 查询 |
| 人工编辑 | 直接编辑 markdown | 通过脚本/API |
| Phase 字段 | 无 | ✓ 有 |

---

### 2.3 **工作流状态** - 重叠程度：中等

#### .specify 中的状态概念
```bash
# plan.md 中可能的工作流阶段
- Clarification / Planning
- Design / Development  
- Implementation
- Testing
- Deployment
```

#### project-manager 中的状态概念
```
特性状态：
- planning      # 规划中
- implementing  # 实现中
- testing       # 测试中
- completed     # 已完成

工作流阶段：
- spec          # 规范阶段
- plan          # 计划阶段
- implement     # 实现阶段
```

#### 重叠点
```
都需要管理特性的阶段进度
```

---

### 2.4 **环境信息管理** - 无重叠

#### .specify 特有
- plan.md 中的元数据提取（语言、框架、数据库）
- 多代理上下文文件同步（CLAUDE.md、Copilot 等）
- 分支和路径验证

#### project-manager 特有
- 产品维度管理（Project Type）
- 任务细粒度跟踪（phase 字段）
- 历史审计日志
- 状态转换规则（transition.py）

---

## 三、数据流对比

### .specify 数据流
```
git branch 创建
     ↓
create-new-feature.sh 初始化
     ↓
specs/NNN-feature/ 目录结构
     ↓
spec.md (用户编写)
setup-plan.sh 生成 plan.md (用户编写)
     ↓
check-prerequisites 验证
     ↓
update-agent-context 解析 plan.md → 更新代理
     ↓
tasks.md (外部生成/编写)
```

### project-manager 数据流
```
产品创建 (product.py)
     ↓
特性创建 (feature.py) - 关联产品
     ↓
任务创建 (task.py) - 关联特性
     ↓
状态更新 (feature.py, task.py)
     ↓
状态查询 (status.py)
工作流转换 (transition.py)
     ↓
历史审计 (history 表)
```

---

## 四、合并的可能性分析

### 场景 A：最小重叠合并
**方案**：将 .specify 脚本转换为 Python，保留各自独立的功能

```python
# .specify/scripts/python/ (新建)
├── common.py                  # 路径和分支管理
├── check_prerequisites.py     # 验证
├── create_feature.py          # 创建分支
├── setup_plan.py              # 初始化计划
└── update_agent_context.py    # 代理同步

# skills/project-manager/scripts/ (保持)
├── feature.py                 # 数据库特性 CRUD
├── task.py                    # 数据库任务 CRUD
├── product.py                 # 产品管理
├── status.py                  # 查询统计
└── transition.py              # 状态转换
```

**优点**：
- ✓ 清晰的职责分离
- ✓ .specify 专注于文件系统和 git
- ✓ project-manager 专注于数据追踪
- ✓ 最小化改动

**缺点**：
- ✗ 数据重复（分支名在两处）
- ✗ 特性创建时需要两步操作

---

### 场景 B：深度融合合并
**方案**：创建统一的特性生命周期管理系统

```
unified_feature_manager/
├── core.py              # 特性核心模型
├── create.py            # 创建特性（集成 git + db）
├── plan.py              # 计划管理（集成 markdown + db）
├── task.py              # 任务管理（集成 markdown + db）
├── validate.py          # 验证（集成所有检查）
├── update_context.py    # 上下文同步
├── status.py            # 状态查询和转换
└── sync.py              # 双向同步（git ← → db）
```

**执行流程**：
```python
# 创建特性（一步完成）
feature = FeatureManager.create_feature(
    description="Add user authentication",
    product_id=1,
    auto_sync_db=True  # 自动同步到数据库
)
# 返回：
# {
#   "branch": "001-user-auth",
#   "spec_file": "specs/001-user-auth/spec.md",
#   "feature_id": 1,  # 数据库 ID
#   "status": "planning"
# }

# 验证完整性
FeatureManager.validate_feature(branch="001-user-auth")
# 自动检查：分支、spec.md、plan.md、db 记录一致性

# 更新计划
FeatureManager.update_plan(
    feature_id=1,
    plan_content="...",
    auto_update_agents=True,  # 自动更新代理
    auto_update_db=True       # 自动同步数据库
)
```

**优点**：
- ✓ 单一入口点，操作简化
- ✓ 自动保持 git、文件系统、数据库三者一致
- ✓ 强大的验证和同步能力
- ✓ 易于扩展

**缺点**：
- ✗ 大规模重构
- ✗ 需要双向同步逻辑
- ✗ 如果分离的工具独立修改数据，需要处理冲突

---

### 场景 C：平衡合并（推荐）
**方案**：将 .specify 转 Python，在 project-manager 中新增"特性启动"操作

```python
# skills/project-manager/scripts/

# 新增：特性启动（集成 git + db）
feature_bootstrap.py
├── 调用 .specify 的逻辑创建分支和目录
├── 自动在 project-manager 数据库中创建特性记录
├── 返回统一的特性 ID 和 git 信息

# 新增：计划同步（集成 plan.md + db）
plan_sync.py
├── 解析 plan.md 的元数据
├── 同步到 project-manager 的特性记录
├── 调用 update-agent-context 更新代理

# 新增：任务同步（集成 tasks.md + db）
task_sync.py
├── 解析 tasks.md 中的任务
├── 自动创建/更新 project-manager 的任务记录
├── 保持 markdown 和数据库一致
```

**特点**：
- ✓ .specify 逻辑保留，专注文件和 git
- ✓ project-manager 专注数据追踪和统计
- ✓ 新增的"同步层"保持两者一致
- ✓ 渐进式迁移，可逐步整合

---

## 五、如果合并至 project-manager 会获得的能力

### 当前 project-manager 的能力（基础）
```
1. 产品级管理
   - 创建/查询/更新产品
   - 产品生命周期追踪

2. 特性级管理
   - 创建/查询/更新特性
   - 按产品筛选
   - 状态和优先级跟踪

3. 任务级管理
   - 创建/查询/更新任务
   - 按特性筛选
   - 任务状态追踪

4. 工作流管理
   - 特性状态转换规则
   - 工作流阶段跟踪
   - 状态查询统计

5. 历史审计
   - 所有操作的变更日志
   - 时间戳追踪
```

---

### 合并后会新增的能力

#### 第 1 级：文件系统集成
```
6. Git 分支管理
   + 自动创建分支，集成分支编号和特性 ID
   + 分支命名智能化（停用词过滤、长度限制）
   + 多分支支持（多个分支可同一特性）

7. 特性目录结构管理
   + 自动创建和验证 specs/NNN-feature/ 目录
   + 自动生成 spec.md, plan.md
   + 模板管理和占位符替换

8. 前置检查和验证
   + 验证特性完整性（分支、目录、文件）
   + 阶段性验证（规划阶段需要 spec.md、plan.md）
   + 可选文件验证（research.md、data-model.md 等）
```

#### 第 2 级：计划和元数据管理
```
9. Plan.md 解析和同步
   + 自动从 plan.md 提取元数据
     - 编程语言/版本
     - 主要框架
     - 存储/数据库
     - 项目类型
   + 自动同步到数据库记录
   + 验证元数据完整性

10. Tasks.md 解析和同步
    + 自动从 tasks.md 解析任务
    + 自动创建/更新数据库任务记录
    + 保持 Markdown 和数据库双向一致
    + 任务阶段映射（phase 字段）
```

#### 第 3 级：智能代理管理
```
11. 多代理上下文同步
    + 支持 17 种 AI 代理（Claude、Copilot、Cursor 等）
    + 自动从 plan.md 生成代理配置
    + 智能检测代理文件位置（单一 .md 或目录结构）
    + 防止重复更新，保持一致性
    + 基于项目类型和技术栈自动生成内容

12. 智能内容生成
    + 自动生成项目结构建议
    + 自动生成语言特定的构建/测试命令
    + 自动生成技术栈描述
    + 自动维护"最近更新"日志

13. 代理能力查询
    + 查询当前已配置的代理
    + 查询每个代理的最新信息
    + 生成代理配置状态报告
```

#### 第 4 级：工作流自动化
```
14. 特性全生命周期管理
    + 创建特性 = git 分支 + 目录 + db 记录 + 模板 (一步完成)
    + 初始化计划 = 生成模板 + db 记录 (一步完成)
    + 完成特性 = 标记 db + 存档目录 + 更新代理 (一步完成)

15. 阶段性检查和推进
    + "准备实现检查" - 确保 spec.md, plan.md 就绪
    + "准备测试检查" - 确保 tasks.md 就绪
    + "准备发布检查" - 确保所有文档完整

16. 自动化流程触发
    + 创建 plan.md 时，自动更新代理配置
    + 更新 tasks.md 时，自动同步数据库
    + 特性完成时，自动生成总结报告

17. 多分支并行管理
    + 支持多个分支同一特性的同步
    + 汇总多分支的任务和进度
    + 自动合并时的 plan.md 冲突解决提示
```

#### 第 5 级：数据分析和报告
```
18. 增强的统计查询
    + "当前工作" - 显示 git 分支、db 状态、文件完整性
    + "特性进度" - 显示 spec → plan → tasks → completion 进度
    + "技术栈分布" - 按项目类型、语言统计
    + "代理配置覆盖" - 显示哪些代理已配置、哪些遗漏

19. 工作流分析
    + "阶段统计" - 各阶段停留时间
    + "完成率分析" - 按特性、按阶段、按优先级
    + "风险识别" - 长期停留的特性、缺少文档的特性

20. 代理配置报告
    + 生成"代理就绪报告"
    + 生成"特性文档覆盖报告"
    + 生成"技术栈更新日志"
```

#### 第 6 级：环境和工具集成
```
21. 多环境支持
    + 支持 git 项目和非 git 项目
    + 支持 SPECIFY_FEATURE 环境变量
    + 自动检测和适配

22. 跨平台兼容性（Python）
    + 脱离 Bash 依赖
    + Windows/Linux/Mac 原生支持
    + 更好的 IDE 集成和调试

23. 扩展能力
    + 易于添加新的代理类型
    + 易于添加新的验证规则
    + 易于添加新的报告类型
```

---

## 六、合并后的系统架构

```
project-manager/
│
├── core/
│   ├── models.py              # 数据模型（产品、特性、任务、工作流）
│   ├── db.py                  # SQLite 操作
│   └── state_machine.py       # 状态转换规则
│
├── git_integration/
│   ├── branch_manager.py      # 分支创建和验证
│   ├── feature_bootstrap.py   # 特性启动（集成 git + db）
│   └── multi_branch_sync.py   # 多分支同步
│
├── file_management/
│   ├── spec_manager.py        # spec.md 管理
│   ├── plan_manager.py        # plan.md 管理和元数据解析
│   ├── task_parser.py         # tasks.md 解析
│   ├── template_engine.py     # 模板引擎
│   └── validators.py          # 前置检查
│
├── agent_management/
│   ├── context_updater.py     # 代理上下文更新
│   ├── agent_registry.py      # 代理类型注册
│   ├── content_generator.py   # 内容生成器
│   └── multi_agent_sync.py    # 多代理同步
│
├── synchronization/
│   ├── bidirectional_sync.py  # 文件 ← → db 双向同步
│   └── conflict_resolver.py   # 冲突解决
│
├── reporting/
│   ├── status_reporter.py     # 状态报告
│   ├── analytics.py           # 数据分析
│   └── compliance_checker.py  # 完整性检查
│
└── cli/
    ├── feature_commands.py    # 特性相关命令
    ├── plan_commands.py       # 计划相关命令
    ├── task_commands.py       # 任务相关命令
    ├── agent_commands.py      # 代理相关命令
    └── report_commands.py     # 报告相关命令
```

---

## 七、迁移路线图

### Phase 1：准备（第 1 周）
- ✓ 将 .specify bash 脚本改写为 Python
- ✓ 验证功能完全迁移
- ✓ 创建 .specify/scripts/python/ 目录

### Phase 2：集成（第 2-3 周）
- ✓ 在 project-manager 中新增 feature_bootstrap.py
- ✓ 实现 plan_sync.py 和 task_sync.py
- ✓ 添加双向同步逻辑

### Phase 3：增强（第 4-6 周）
- ✓ 添加智能验证和阶段检查
- ✓ 增强代理管理能力
- ✓ 实现自动化工作流

### Phase 4：优化（第 7-8 周）
- ✓ 添加报告和分析功能
- ✓ 性能优化
- ✓ 文档完善

---

## 八、推荐方案：平衡合并（场景 C）

**理由**：
1. ✓ 最小化破坏性修改
2. ✓ 保留各系统的专业性
3. ✓ 易于维护和扩展
4. ✓ 渐进式迁移，可逐步整合
5. ✓ 双赢：.specify 获得跨平台支持，project-manager 获得文件系统集成

**实现步骤**：
1. 将 bash 脚本转为 Python（`/.specify/scripts/python/`）
2. 新增 project-manager 的"同步层"（`/skills/project-manager/scripts/sync/`）
3. 统一 CLI 入口（可选）

**成本**：
- 代码编写：40-60 小时
- 测试验证：20-30 小时
- 文档完善：10-15 小时
- 总计：70-105 小时（2-3 周）

