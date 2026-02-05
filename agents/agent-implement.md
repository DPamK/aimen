---
description: 执行实现计划的所有任务
---

# Agent Implement - 实现执行

## 职责

执行任务清单中定义的所有任务，包括：
- 验证检查清单完成度 (如有)
- 创建/验证ignore文件
- 按Phase顺序执行任务
- 生成进度报告

## 输入规范

```text
$ARGUMENTS = [可选的用户上下文]
```

必需文件：
- `specs/[###-feature-name]/tasks.md` (来自agent-tasks)
- `specs/[###-feature-name]/plan.md` (技术栈和结构)

可选文件：
- `specs/[###-feature-name]/data-model.md`
- `specs/[###-feature-name]/contracts/`
- `specs/[###-feature-name]/research.md`
- `specs/[###-feature-name]/quickstart.md`
- `specs/[###-feature-name]/checklists/` (检查清单)

## 执行流程

### Step 1: 初始化和先决条件

1. 运行先决条件检查: `.specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks`
2. 验证所有必需文件存在
3. 如果缺少tasks.md或plan.md，报告ERROR

### Step 2: 检查清单验证 (可选)

如果 `specs/[###-feature-name]/checklists/` 目录存在：

1. **扫描清单文件**:
   ```powershell
   Get-ChildItem specs/[###-feature-name]/checklists/*.md
   ```

2. **计算完成度** (对于每个清单):
   - 总项: 所有行匹配 `- [ ]` 或 `- [X]` 或 `- [x]`
   - 完成项: 匹配 `- [X]` 或 `- [x]`
   - 未完成项: 匹配 `- [ ]`

3. **创建状态表**:
   ```
   | Checklist   | Total | Completed | Incomplete | Status |
   |-------------|-------|-----------|------------|--------|
   | ux.md       | 12    | 12        | 0          | ✓ PASS |
   | test.md     | 8     | 5         | 3          | ✗ FAIL |
   | security.md | 6     | 6         | 0          | ✓ PASS |
   ```

4. **检查整体状态**:
   - **PASS**: 所有清单未完成项 = 0
   - **FAIL**: 任何清单有未完成项

5. **如果FAIL** - 询问用户:
   ```
   [表格显示]
   
   Some checklists are incomplete.
   Do you want to proceed with implementation anyway?
   
   (A) Yes, proceed with implementation
   (B) No, wait until checklists are complete
   ```
   
   - 用户说"A"或"yes"或"proceed" → 继续实现
   - 用户说"B"或"no"或"wait" → 停止执行

6. **如果PASS** - 自动继续

### Step 3: 项目设置和验证

#### 3.1 加载实现上下文

从tasks.md、plan.md及可选文档：
- 技术栈 (语言、框架、依赖)
- 项目结构 (源目录、测试目录等)
- 数据模型 (如有)
- API合约 (如有)
- 技术决策 (如有)

#### 3.2 创建/验证Ignore文件

**检测和创建逻辑**:

1. **Git Repository Detection**:
   ```bash
   git rev-parse --git-dir 2>/dev/null
   ```
   - 成功 → 创建/验证 `.gitignore`
   - 失败 → 跳过git相关

2. **Docker Detection**:
   - 检查: `Dockerfile*` 文件 或 plan.md中有"Docker"
   - 如果有 → 创建/验证 `.dockerignore`

3. **ESLint Detection**:
   - 检查: `.eslintrc*` 文件存在
   - 如果有 → 创建/验证 `.eslintignore`

4. **Prettier Detection**:
   - 检查: `.prettierrc*` 文件存在
   - 如果有 → 创建/验证 `.prettierignore`

5. **Package Managers**:
   - 检查: `package.json` 或 `.npmrc` 或 `.yarnrc`
   - 如果发布: 创建/验证 `.npmignore`

6. **其他工具**:
   - Terraform: 检查 `*.tf` → `.terraformignore`
   - Helm: 检查Helm图表 → `.helmignore`

#### 3.3 Ignore文件内容

**如果文件已存在**:
- 验证包含基本模式
- 仅追加缺失的关键模式
- 不覆盖现有内容

**如果文件不存在**:
- 从plan.md检测的技术创建完整模式集
- 使用下列按技术的通用模式：

**Node.js/JavaScript/TypeScript**:
```
node_modules/
dist/
build/
*.log
.env*
coverage/
```

**Python**:
```
__pycache__/
*.pyc
.venv/
venv/
dist/
*.egg-info/
.pytest_cache/
```

**Java**:
```
target/
*.class
*.jar
.gradle/
build/
.idea/
```

**C#/.NET**:
```
bin/
obj/
*.user
*.suo
packages/
```

**Go**:
```
*.exe
*.test
vendor/
*.out
```

**Ruby**:
```
.bundle/
log/
tmp/
*.gem
vendor/bundle/
```

**PHP**:
```
vendor/
*.log
*.cache
.env
```

**Rust**:
```
target/
debug/
release/
*.rs.bk
*.rlib
Cargo.lock
```

**C++/C**:
```
build/
bin/
obj/
out/
*.o
*.so
*.a
*.exe
*.dll
```

**通用**:
```
.DS_Store
Thumbs.db
*.tmp
*.swp
.vscode/
.idea/
```

**工具特定**:
- Docker: `node_modules/`, `.git/`, `*.log*`, `.env*`, `coverage/`
- ESLint: `node_modules/`, `dist/`, `build/`, `coverage/`, `*.min.js`
- Prettier: `node_modules/`, `dist/`, `build/`, `coverage/`, `package-lock.json`, `yarn.lock`
- Terraform: `.terraform/`, `*.tfstate*`, `*.tfvars`, `.terraform.lock.hcl`
- Kubernetes: `*.secret.yaml`, `secrets/`, `.kube/`, `kubeconfig*`

### Step 4: 任务执行

#### 4.1 解析任务

从tasks.md中：
1. 提取所有任务 (T001, T002, ...)
2. 识别Phase分组
3. 建立依赖关系

#### 4.2 按Phase顺序执行

```
Phase 1 (Setup) → Phase 2 (Foundation) → Phase 3 (US1) → Phase 3.2 (US2) → ... → Phase Final (Polish)
```

#### 4.3 对每个任务

1. **标记进行中**:
   ```
   ⏱️ Executing T001 Create project structure per implementation plan
   ```

2. **执行任务**:
   - 为代理调用或代码执行分发任务
   - 访问之前的阶段输出 (如data-model, contracts等)
   - 生成任务输出 (代码文件、配置等)

3. **验证输出**:
   - 检查预期的文件是否创建
   - 验证代码语法 (如适用)
   - 验证与计划中的结构对齐

4. **标记完成**:
   ```
   ✓ T001 Complete
   ```

5. **处理失败** (如果任务失败):
   ```
   ✗ T001 Failed: [错误信息]
   
   Do you want to:
   (A) Retry the task
   (B) Skip and continue
   (C) Stop implementation
   ```

#### 4.4 进度跟踪

维护实时进度计数器：
```
Progress: [完成数] / [总数] tasks
Phase: [当前Phase]
Current Task: [TaskID - 描述]
Elapsed Time: [时间]
```

### Step 5: Phase完成总结

每完成一个Phase，输出：
```markdown
## Phase 1: Setup - Complete ✓

**Completed Tasks**:
- T001: Create project structure ✓
- T002: Initialize npm ✓
- T003: Configure testing ✓

**Time**: [elapsed]
**Artifacts Created**:
- src/ directory structure
- package.json
- jest.config.js

**Next**: Proceeding to Phase 2...
```

### Step 6: 实现完成和报告

#### 6.1 最终验证

1. 验证所有Phase都已执行
2. 验证所有任务都标记为完成 (✓) 或跳过 (⊘)
3. 检查所有ignore文件是否已创建
4. 生成最终清单

#### 6.2 生成进度报告

```markdown
# Implementation Complete ✓

## Summary

**Feature**: [###-feature-name]
**Branch**: [branch-name]
**Start Time**: [time]
**End Time**: [time]
**Total Duration**: [duration]

## Task Completion

**Overall Progress**: [完成] / [总] tasks (X%)

### By Phase

| Phase | Tasks | Completed | Skipped | Failed | Status |
|-------|-------|-----------|---------|--------|--------|
| Setup | 5 | 5 | 0 | 0 | ✓ |
| Foundation | 6 | 6 | 0 | 0 | ✓ |
| US1 | 8 | 8 | 0 | 0 | ✓ |
| Polish | 4 | 4 | 0 | 0 | ✓ |
| **TOTAL** | **23** | **23** | **0** | **0** | ✓ |

### Ignore Files Created

- ✓ .gitignore
- ✓ .dockerignore (if applicable)
- ✓ .eslintignore (if applicable)

## Artifacts Generated

**Source Code**:
- `src/` directory with complete structure
- All required modules and services
- Tests for critical paths

**Configuration Files**:
- `package.json` (or language equivalent)
- `.gitignore`, `.dockerignore`, etc.

**Documentation**:
- API documentation (if generated)
- Deployment guides (if created)

## Final Checklist

- [X] All Phase 1 (Setup) tasks complete
- [X] All Phase 2 (Foundation) tasks complete
- [X] All Phase 3 (User Story) tasks complete
- [X] All Phase 4 (Polish) tasks complete
- [X] Ignore files created/verified
- [X] Code structure aligns with plan.md
- [X] All tests passing

## Next Steps

1. **Local Testing**: 
   - Run full test suite
   - Test critical user flows

2. **Code Review**:
   - Run linters/formatters
   - Peer review key components

3. **Deployment**:
   - Build and package
   - Deploy to staging/production

4. **Monitoring**:
   - Set up monitoring/logging
   - Verify observability signals

## Recommended Commits

\`\`\`bash
git add .
git commit -m "feat: implement [feature-name] (all tasks complete)"
git push origin [branch-name]
\`\`\`

## Success Metrics

Based on plan.md and spec.md:
- [检查spec中的成功标准]
- [检查plan中的性能目标]
- [检查任何特定的质量指标]
```

## 输出规范

### 实现的文件

根据plan.md中定义的项目结构生成的所有源代码文件和配置文件。

### 创建/更新的Ignore文件

- `.gitignore` (如git仓库)
- `.dockerignore` (如Docker)
- `.eslintignore` (如ESLint)
- `.prettierignore` (如Prettier)
- 其他工具特定ignore文件

### 进度报告

完整的实现摘要，包含：
- 按Phase的任务完成
- 创建的工件
- 最终检查清单
- 后续步骤

## 成功标准

- ✓ 所有Phase执行完成
- ✓ 所有任务标记为完成或显式跳过
- ✓ Ignore文件已创建/验证
- ✓ 代码结构符合plan.md
- ✓ 无critical错误
- ✓ 进度报告清晰完整

## 约束和限制

- 必须按Phase顺序执行（不能跳过阶段）
- 每个任务必须完成验证或显式跳过
- Ignore文件必须基于检测的技术栈
- 不能修改已完成的早期阶段

## 错误处理

| 错误 | 处理 |
|------|------|
| 找不到tasks.md | 错误: 运行 `/aimen.tasks` 先 |
| 找不到plan.md | 错误: 运行 `/aimen.plan` 先 |
| 检查清单未完成 | 询问: 是否继续？ |
| 任务执行失败 | 询问: 重试/跳过/停止？ |
| 技术栈不明确 | 使用: 合理默认值或跳过该ignore文件 |

## 可选步骤

- **迭代**: 可多次运行实现，补充遗漏的任务
- **部分实现**: 可跳过Polish任务进行快速发布

## 下一步指导

实现完成后：

1. **本地测试**: 运行完整测试套件
2. **代码审查**: 执行linting和peer review
3. **部署**: 打包并部署到staging/production
4. **监控**: 验证可观测性信号

