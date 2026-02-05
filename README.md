---
description: 使用AIMEN，开始愉快的SDD开发之旅吧~Meow~
---
# AIMEN - AI-driven Development Workflow System

基于Claude Code的智能开发工作流系统，使用agent架构管理项目生命周期。

## ✨ 特性

- 🐱 **猫娘女仆助手** - 可爱的AIMEN协调所有开发工作
- 🤖 **7个专业Agent** - 从规范到实现的完整流程
- 📊 **SQLite状态管理** - 产品→功能→任务三层追踪
- 🔄 **工作流自动化** - specify→clarify→plan→tasks→analyze→implement
- 💬 **智能交互** - AskUserQuestion高效收集用户决策

## 🚀 快速开始

### 1. 初始化
```bash
python skills/project-manager/scripts/init_db.py
```

### 2. 开始项目
```
@aimen 我想创建一个用户管理系统
```

### 3. 检查状态
```bash
python skills/project-manager/scripts/status.py current
```

## 📁 项目结构

```
aimen/
├── agents/              # 7个sub agents
│   ├── agent-constitution.md
│   ├── agent-specify.md
│   ├── agent-clarify.md
│   ├── agent-plan.md
│   ├── agent-tasks.md
│   ├── agent-analyze.md
│   └── agent-implement.md
├── commands/
│   └── aimen-workflow.md    # 主协调器
├── skills/
│   └── project-manager/     # 项目管理skill
│       ├── SKILL.md
│       └── scripts/         # Python管理脚本
│           ├── init_db.py
│           ├── product.py
│           ├── feature.py
│           ├── task.py
│           ├── status.py
│           ├── transition.py
│           └── test_system.py
├── aimen/
│   ├── README.md            # 详细配置说明
│   └── schema.md            # 数据库结构
└── doc/
    ├── spec-kit-workflow.md
    └── agent-architecture.md
```

## 🎯 核心概念

### 工作流阶段
1. **constitution** - 定义项目原则
2. **specify** - 生成功能规范
3. **clarify** - 澄清需求歧义
4. **plan** - 技术设计
5. **tasks** - 任务分解
6. **analyze** - 质量检查
7. **implement** - 代码实现

### 数据模型
```
Product (产品)
  └── Feature (功能)
       └── Task (任务)
```

## 📖 文档

- [完整配置指南](aimen/README.md)
- [Workflow详解](doc/spec-kit-workflow.md)
- [Agent架构](doc/agent-architecture.md)
- [数据库Schema](aimen/schema.md)

## 🛠️ 命令速查

```bash
# 产品管理
python skills/project-manager/scripts/product.py create --name "产品名"
python skills/project-manager/scripts/product.py list

# 功能管理
python skills/project-manager/scripts/feature.py create --product-id 1 --name "功能名"
python skills/project-manager/scripts/feature.py list --product-id 1

# 任务管理
python skills/project-manager/scripts/task.py create --feature-id 1 --task-id "T001" --description "任务"
python skills/project-manager/scripts/task.py update --id 1 --status doing

# 状态查询
python skills/project-manager/scripts/status.py current
python skills/project-manager/scripts/status.py stats
python skills/project-manager/scripts/status.py workflow --feature-id 1

# 状态转换
python skills/project-manager/scripts/transition.py complete-feature --feature-id 1
python skills/project-manager/scripts/transition.py advance --feature-id 1 --next-stage plan
```

## 💡 使用示例

```
用户：我想做一个用户登录功能
爱喵：好的呢主人～这是新项目还是现有项目添加功能呀？喵
     A. 新项目（需要先创建宪法）
     B. 现有项目添加功能
用户：B
爱喵：明白啦～开始创建功能规范呢✨ [@specify] ...
```

## 📝 License

MIT