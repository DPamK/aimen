# AIMEN System Configuration

## 系统概述

AIMEN是基于Claude Code的智能开发工作流系统，使用agent-based架构管理项目生命周期。

## 核心组件

### 1. Main Command
- **aimen** (`commands/aimen-workflow.md`) - 猫娘女仆协调器，调度所有agents

### 2. Sub Agents
位于 `agents/` 目录：
- **constitution** - 项目宪法管理
- **specify** - 功能规范生成
- **clarify** - 需求澄清
- **plan** - 技术规划
- **tasks** - 任务分解
- **analyze** - 质量分析
- **implement** - 实现执行

### 3. Project Manager Skill
- **project-manager** (`skills/project-manager/SKILL.md`) - 项目状态管理
- **Scripts** (`skills/project-manager/scripts/`) - Python脚本集
  - `init_db.py` - 初始化SQLite数据库
  - `product.py` - 产品管理
  - `feature.py` - 功能管理
  - `task.py` - 任务管理
  - `status.py` - 状态查询
  - `transition.py` - 状态转换
  - `test_system.py` - 系统测试

## 数据模型

### 三层结构
```
Product (产品需求)
  └── Feature (功能模块)
       └── Task (最小功能单元)
```

### 状态流转
- **Product**: active → paused → completed
- **Feature**: planning → implementing → testing → completed
- **Task**: todo → doing → done

### 工作流阶段
specify → clarify → plan → tasks → analyze → implement

## 使用指南

### 首次使用
1. 初始化数据库：
   ```bash
   python skills/project-manager/scripts/init_db.py
   ```

2. 调用主command：
   ```
   @aimen 我想创建一个用户管理系统
   ```

### 日常使用
1. 检查当前状态：
   ```bash
   python skills/project-manager/scripts/status.py current
   ```

2. 继续工作：
   ```
   @aimen 继续
   ```

### 手动管理
```bash
# 创建产品
python skills/project-manager/scripts/product.py create --name "产品名"

# 创建功能
python skills/project-manager/scripts/feature.py create --product-id 1 --name "功能名" --branch "001-feature"

# 更新任务
python skills/project-manager/scripts/task.py update --id 1 --status doing

# 查看统计
python skills/project-manager/scripts/status.py stats
```

## 配置选项

### Agent Models
- **opus** - 最强能力（主command推荐）
- **sonnet** - 平衡性能（agents推荐）
- **haiku** - 快速响应
- **inherit** - 继承上层模型

### Available Tools
- Bash - 命令执行
- Read - 文件读取
- Write - 文件写入
- Edit - 文件编辑
- Glob - 文件匹配
- Grep - 文本搜索
- Skill - 调用skill
- WebFetch - 网页抓取
- WebSearch - 网络搜索
- NotebookEdit - Notebook编辑
- TaskCreate/Get/Update/List - 任务管理

## 工作流模式

### Fast模式（5步）
constitution → specify → tasks → implement

### Standard模式（7步）
constitution → specify → clarify → plan → tasks → implement

### Quality模式（9步）
constitution → specify → clarify → plan → tasks → analyze → implement → analyze → 迭代

## 最佳实践

1. **善用AskUserQuestion**
   - 所有用户选择必须用此方法
   - 提供2-5个清晰选项
   - 避免开放式问题

2. **状态同步**
   - 每次开始前检查current状态
   - 任务状态及时更新
   - 定期查看统计信息

3. **分支管理**
   - 每个功能独立分支
   - 分支名格式：`###-feature-name`
   - 保持feature与branch一一对应

4. **增量开发**
   - 从MVP开始
   - 每个Phase独立验证
   - 及时运行analyze检查

## 技术栈支持

### 编程语言
JavaScript, TypeScript, Python, Java, C#, Go, Ruby, PHP, Rust, Kotlin, C++, Swift, R, Dart, Scala

### 框架
React, Vue, Angular, Next.js, Express, Django, Flask, FastAPI, Spring Boot, .NET Core, Rails, Laravel, Gin等

## 故障排除

### 数据库锁定
```bash
# 关闭所有Python进程后重试
```

### 找不到feature
```bash
# 检查分支是否匹配
python .aimen/scripts/feature.py list
```

### Agent调用失败
```bash
# 检查agent文件格式
# 确保frontmatter包含name/description/tools/model
```

## 版本信息

- **Version**: 1.0.0
- **Database**: SQLite 3
- **Python**: 3.7+
- **Claude Code**: Latest

## 文件结构

```
aimen/
├── agents/              # Sub agents
├── commands/            # Main command
├── skills/              # Project manager skill
│   └── project-manager/
│       ├── SKILL.md
│       └── scripts/     # Python管理脚本
│           └── project.db   # SQLite数据库（运行时生成）
└── doc/                 # 文档
```
