# 课程逻辑优化与实用内容扩展

**日期：** 2026-07-20  
**状态：** 用户授权直接落地（无需逐步确认）

## 问题

现有课程覆盖广，但阶段编号与学习路径不一致（CI 在 10–12、工程化在 13–17），进阶实用主题（submodule、fork、hotfix、conventional commits、PR review、历史考古等）缺口明显。

## 方案

1. **不重编号既有文件**（避免破坏进度 localStorage / 外链），在总览与学习路径中用「逻辑阶段」重新编排推荐顺序。
2. **新增实用关卡 22–29**（可在本仓库终端练习）：
   - 22 conventional commits
   - 23 PR 代码审查实践
   - 24 fork 与 upstream 同步
   - 25 hotfix 应急发布
   - 26 submodule
   - 27 interactive rebase / fixup 进阶
   - 28 blame / log 历史考古
   - 29 sparse-checkout 与部分克隆
3. 同步 `lessons.json`、viewer、quiz、search、learning-path、overview、TOTAL_LESSONS、测试。

## 逻辑阶段（推荐顺序）

| 逻辑阶段 | 关卡 |
|----------|------|
| A 环境 | 00, 00b |
| B Git 基础 | 01–03 |
| C 分支协作 | 04–06b |
| D 救火恢复 | 07–09, 20–21 |
| E 工程化 | 13–17, 22–23 |
| F CI/CD | 10–12 |
| G 安全 | 18–19 |
| H 进阶实用 | 24–29 |
