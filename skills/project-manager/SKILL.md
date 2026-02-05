---
name: project-manager
description: 项目状态管理，包括产品需求、功能模块和任务的全生命周期管理。使用Python脚本操作SQLite数据库进行状态追踪。
---

项目管理技能，用于管理开发项目的状态（产品、功能、任务）。

## 核心概念

**三层结构**：
- **Product（产品需求）**：最高层，如"用户管理系统"
- **Feature（功能模块）**：中间层，如"用户注册"、"密码重置"  
- **Task（最小功能单元）**：最小执行单元，对应tasks.md中的任务

## 可用脚本

所有脚本位于 `skills/project-manager/scripts/`：

### 初始化
```bash
python skills/project-manager/scripts/init_db.py
```

### 产品管理
```bash
python skills/project-manager/scripts/product.py create --name "产品名称" --description "描述"
python skills/project-manager/scripts/product.py list
python skills/project-manager/scripts/product.py update --id 1 --status active|paused|completed
```

### 功能管理
```bash
python skills/project-manager/scripts/feature.py create --product-id 1 --name "功能名称" --branch "001-feature"
python skills/project-manager/scripts/feature.py list --product-id 1
python skills/project-manager/scripts/feature.py update --id 1 --status planning|implementing|testing|completed
```

### 任务管理
```bash
python skills/project-manager/scripts/task.py create --feature-id 1 --task-id "T001" --description "任务描述"
python skills/project-manager/scripts/task.py list --feature-id 1
python skills/project-manager/scripts/task.py update --id 1 --status todo|doing|done
```

### 状态查询
```bash
python skills/project-manager/scripts/status.py current    # 查询当前工作
python skills/project-manager/scripts/status.py stats     # 查询统计
python skills/project-manager/scripts/status.py workflow --feature-id 1  # 查询工作流阶段
```

### 状态转换
```bash
python skills/project-manager/scripts/transition.py complete-feature --feature-id 1
python skills/project-manager/scripts/transition.py advance --feature-id 1 --next-stage plan
```

## 使用模式

1. **新项目**：创建产品 → 创建功能 → 创建任务
2. **继续工作**：查询current状态 → 更新任务状态
3. **多功能并行**：为每个功能创建独立分支

所有脚本输出JSON格式，便于解析。
