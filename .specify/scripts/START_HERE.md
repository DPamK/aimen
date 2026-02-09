# 📖 快速开始指南

> 💡 **TL;DR**: 如果你只有 5 分钟，就读这个文件。

---

## 🎯 这 5 个 bash 脚本是做什么的？

```
common.sh
  ↓ 提供工具函数
  
create-new-feature.sh
  ↓ 创建新特性分支和 spec.md
  
setup-plan.sh
  ↓ 生成 plan.md（实现计划）
  
check-prerequisites.sh
  ↓ 验证特性文件是否完整
  
update-agent-context.sh
  ↓ 同步 17 种 AI 代理配置文件
```

**核心职责**：自动化 Spec-Driven Development 工作流

---

## 📁 管理的文件

```
项目根目录/
├── specs/NNN-feature/
│   ├── spec.md              ← 特性规范
│   ├── plan.md              ← 实现计划（必需）
│   ├── tasks.md             ← 任务列表（条件）
│   └── [其他文档]           ← research.md, data-model.md 等
│
├── CLAUDE.md                ← 这些是 AI 代理配置
├── GEMINI.md
├── .github/agents/
├── .cursor/rules/
└── [其他 13 种代理...]
```

---

## 🚀 使用流程（10 分钟）

```bash
# 第 1 步：创建新特性
./bash/create-new-feature.sh "Add user authentication"
# 输出：001-user-authentication

# 第 2 步：生成计划文件
./bash/setup-plan.sh

# 第 3 步：编辑 spec.md 和 plan.md（手动，5 分钟）

# 第 4 步：验证完整性
./bash/check-prerequisites.sh --json

# 第 5 步：更新 AI 代理
./bash/update-agent-context.sh
```

**完成！** 现在你的特性已经：
- ✓ 创建了 git 分支
- ✓ 生成了文件模板
- ✓ 验证了完整性
- ✓ 同步了所有 AI 代理

---

## 📚 完整文档

| 想要... | 读这个 | 时间 |
|--------|-------|------|
| 理解脚本各做什么 | README.md | 10 min |
| 学会怎么使用 | DETAILED_GUIDE.md | 40 min |
| 了解文件结构 | ANALYSIS.md | 20 min |
| 理解与 project-manager 的关系 | MERGE_ANALYSIS.md | 35 min |
| 看合并后能干什么 | CAPABILITIES_SUMMARY.md | 50 min |
| 快速查找答案 | INDEX.md | 5 min |

---

## 🔑 关键概念

| 概念 | 说明 |
|------|------|
| **特性编号** | 001, 002, 003...（3 位数字） |
| **分支名** | 格式：NNN-feature-name（如 001-user-auth） |
| **特性目录** | specs/001-user-auth/ |
| **必需文件** | spec.md（规范）+ plan.md（计划） |
| **代理数量** | 17 种 AI 代理（Claude、Copilot 等） |

---

## ⚡ 最常见的 3 个问题

### Q1: 这些脚本和 project-manager 技能什么关系？
**A**: 两个系统目前独立工作，但可以通过平衡合并方案集成，获得 20+ 个新能力。详见 MERGE_ANALYSIS.md。

### Q2: 支持非 git 项目吗？
**A**: 支持。所有脚本都有 git 和非 git 的两套逻辑。非 git 项目用环境变量 `SPECIFY_FEATURE` 指定特性名。

### Q3: 能改成 Python 吗？
**A**: 完全可以，而且值得做。会获得更好的跨平台支持和与 project-manager 的统一。详见 MERGE_ANALYSIS.md。

---

## 🎯 对你的建议

### 如果你是 👨‍💻 开发者
1. 今天：快速浏览 README.md
2. 本周：完整阅读 DETAILED_GUIDE.md
3. 本月：在项目中实际运行脚本

### 如果你是 🏛️ 架构师
1. 今天：阅读 README.md + ANALYSIS.md
2. 本周：完整阅读 MERGE_ANALYSIS.md
3. 本月：评估是否需要集成或改写

### 如果你是 📊 决策者
1. 今天：阅读本文件 + MERGE_ANALYSIS.md 摘要
2. 本周：看 CAPABILITIES_SUMMARY.md（合并后的能力）
3. 决策：是否投入时间改进

---

## 💡 核心价值

**现在**：
- ✓ 自动管理特性分支
- ✓ 自动生成文档模板
- ✓ 自动验证完整性
- ✓ 自动同步 17 种 AI 代理

**合并后**：
- ✓ 所有上面的功能
- ✓ + 数据库驱动的追踪
- ✓ + 工作流自动化
- ✓ + 丰富的分析报告
- ✓ + Python 跨平台支持

---

## 🔗 文档快速链接

- 📄 **[README.md](README.md)** - 核心概览（推荐首先阅读）
- 📘 **[DETAILED_GUIDE.md](DETAILED_GUIDE.md)** - 详细讲解
- 🗂️ **[ANALYSIS.md](ANALYSIS.md)** - 文件管理
- 🔄 **[MERGE_ANALYSIS.md](MERGE_ANALYSIS.md)** - 集成分析
- 🚀 **[CAPABILITIES_SUMMARY.md](CAPABILITIES_SUMMARY.md)** - 未来能力
- 🗺️ **[INDEX.md](INDEX.md)** - 完整导航

---

## ✅ 完成度

- ✅ 5 个脚本全部分析
- ✅ 1484 行代码全部覆盖
- ✅ 所有关键概念都有说明
- ✅ 100+ 代码示例
- ✅ 3 种合并方案分析
- ✅ 20+ 能力案例展示

---

**推荐下一步**：打开 [README.md](README.md) 了解全貌

