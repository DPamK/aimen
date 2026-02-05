---
description: 创建或更新项目治理宪法，验证版本控制和模板一致性
---

# Agent Constitution - 项目治理宪法管理

## 职责

创建和维护项目的治理宪法，包括：
- 定义项目核心原则
- 管理宪法版本（语义化）
- 验证所有依赖模板的一致性
- 生成同步影响报告

## 输入规范

```text
$ARGUMENTS = [用户提供的项目原则描述]
```

可选输入：
- 现有的 `.specify/memory/constitution.md` (用于更新现有宪法)

## 执行流程

### Step 1: 初始化
1. 检查是否是新项目（无constitution.md）或更新现有项目
2. 加载宪法模板 `.specify/memory/constitution.md` 或创建新的
3. 识别所有占位符标记 `[ALL_CAPS_IDENTIFIER]`

### Step 2: 收集值
根据优先级收集占位符值：
1. **用户输入优先**: 从$ARGUMENTS提取
2. **仓库上下文**: 从README、现有文件推导
3. **默认值**: 对于日期、版本等
4. **TODO标记**: 对于真正未知的项

关键占位符：
- `[PROJECT_NAME]` - 项目名称
- `[PRINCIPLE_1_NAME]` - `[PRINCIPLE_N_NAME]` - 原则名称
- `[PRINCIPLE_1_DESCRIPTION]` - `[PRINCIPLE_N_DESCRIPTION]` - 原则描述
- `[CONSTITUTION_VERSION]` - 版本号 (格式: MAJOR.MINOR.PATCH)
- `[RATIFICATION_DATE]` - 初始批准日期 (YYYY-MM-DD)
- `[LAST_AMENDED_DATE]` - 最后修订日期 (YYYY-MM-DD，如有修改)

### Step 3: 版本决策

版本递增规则（语义化版本）：
- **MAJOR**: 向后不兼容的治理/原则移除或重新定义
- **MINOR**: 新增原则/章节或显著扩展指导
- **PATCH**: 澄清、措辞、拼写修复、非语义细化

### Step 4: 填充和验证

1. 替换所有占位符为具体值
2. 验证没有遗留的未定义标记 (括号内的大写)
3. 确保每个原则包含：
   - 简洁的名称行
   - 段落或要点列表（非协商规则）
   - 如不明显，包含原理说明
4. 保留提前完成的治理章节

### Step 5: 一致性传播检查

验证所有依赖文件与新宪法对齐：

1. **plan-template.md**: 
   - ✓ Constitution Check 部分与新原则对齐
   - ✓ 任何"宪法检查"或规则与新原则一致

2. **spec-template.md**:
   - ✓ 范围和需求对齐检查
   - ✓ 任何强制章节仍然需要

3. **tasks-template.md**:
   - ✓ 任务分类反映新增/移除的原则驱动的任务类型
   - ✓ 示例仍然适用

4. **所有command文件** (`.specify/commands/*.md`):
   - ✓ 没有过时的代理特定参考（如只限CLAUDE）
   - ✓ 通用指导保持有效

5. **运行时文档**:
   - ✓ README.md
   - ✓ docs/quickstart.md (如存在)
   - ✓ 代理特定指导文件

### Step 6: 生成同步影响报告

在更新的宪法文件顶部添加HTML注释：

```html
<!-- SYNC IMPACT REPORT
Version Change: X.Y.Z → A.B.C
Modified Principles: 
  - Old Name → New Name (if renamed)
  - [Principle] - Updated definition
Added Sections: [List]
Removed Sections: [List]
Templates Updated:
  - plan-template.md ✓
  - spec-template.md ✓
  - tasks-template.md ✓
  - All command files ✓
Follow-up TODOs:
  - [Any deferred items]
-->
```

### Step 7: 验证前输出

在写入前进行最终验证：
- ✓ 没有遗留的未解释括号标记
- ✓ 版本行与报告匹配
- ✓ 日期格式: YYYY-MM-DD
- ✓ 原则是声明式、可测试、无模糊语言的

### Step 8: 写入和总结

1. 将完成的宪法写入 `.specify/memory/constitution.md`
2. 输出最终摘要给用户：
   - 新版本和递增原因
   - 需要手动跟进的文件
   - 建议的git提交信息

## 输出规范

### 主输出文件
- `.specify/memory/constitution.md` - 更新的宪法文件 (版本: MAJOR.MINOR.PATCH)

### 辅助输出
- 版本变更说明 (文本或markdown)
- 受影响模板清单及更新状态 (✓ 已更新 / ⚠ 待处理)
- 建议的git提交信息，格式: `docs: amend constitution to vX.Y.Z (原因)`

### 执行结果报告

```markdown
## Constitution 更新完成

**新版本**: X.Y.Z (从A.B.C递增，原因: [MAJOR|MINOR|PATCH])

**修改的原则**:
- [列表已更改的原则]

**新增章节**:
- [列表]

**移除章节**:
- [列表]

**模板更新状态**:
- plan-template.md: ✓ 已验证
- spec-template.md: ✓ 已验证
- tasks-template.md: ✓ 已验证
- command files: ✓ 已验证

**待处理**:
- [任何需要手动跟进的项目]

**建议提交**:
\`\`\`bash
git commit -m "docs: amend constitution to vX.Y.Z ([原因])"
\`\`\`
```

## 成功标准

- ✓ 没有遗留的未定义占位符 (除非显式标记为TODO)
- ✓ 版本号正确递增 (MAJOR/MINOR/PATCH)
- ✓ 所有依赖模板都已检查和报告
- ✓ 同步影响报告完整
- ✓ 日期格式: ISO 8601 (YYYY-MM-DD)
- ✓ 原则是可测试的、无模糊语言的

## 约束和限制

- 宪法是非协商的，优先于所有其他做法
- 版本必须严格遵循语义化版本
- 不能在此命令中修改其他文件的内容（仅可验证）
- 任何跨文件修改都应显式列在影响报告中

## 错误处理

| 错误 | 处理 |
|------|------|
| 找不到constitution.md | 创建新的，从模板开始 |
| 占位符无法推导 | 插入`TODO(FIELD_NAME)`并列在报告中 |
| 版本递增不明确 | 提议理由并要求确认 |
| 模板对齐问题 | 报告为⚠需要手动检查，不自动修改 |
| 日期格式错误 | 转换或拒绝并要求用户输入 |

## 可选步骤

如果用户只更新部分项（如只修改一个原则）：
1. 仍执行验证和版本决策步骤
2. 执行完整的一致性检查 (所有依赖文件)
3. 生成完整的同步影响报告

即使只是部分更新，也要确保完整性和一致性。

