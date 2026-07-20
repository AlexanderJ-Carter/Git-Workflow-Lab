# 关卡总览：边看边练的 Git & CI 全流程

本实验平台提供一系列循序渐进的关卡，设计原则是：**左边看指南，右边动手练**。

推荐的打开方式：

- 一边打开 `docs/*.md`（在编辑器 / 浏览器中）
- 一边打开 `http://localhost:3000` + 本地终端

照着每个关卡的步骤，一条命令一条命令地敲，一步步完成练习。

---

## 阶段规划（确保尽量全面）

- **阶段 0：环境与配置**
  - 覆盖：Git 安装、`git config` 基础配置、全局 `.gitignore`、帮助文档
- **阶段 1：Git 基础操作实验**
  - 覆盖：`git init`、`clone`、`status`、`add`、`commit`、`log`、`diff`、`remote`、`push`、`pull`
- **阶段 2：分支与协作**
  - 覆盖：`branch`、`switch/checkout`、`merge`、`rebase`、`cherry-pick`、`tag`，以及在 Web 上发起 PR/MR
- **阶段 3：救火与历史修复**
  - 覆盖：`reflog`、`reset`、`revert`、`stash`，以及误删分支/误强推等场景的恢复
- **阶段 4：CI/CD 基础**
  - 覆盖：在 Gitea 中配置 Actions 或外部 CI，编写最简单的流水线，理解「触发条件 → Job → Step」
- **阶段 5：CI/CD 进阶（可选）**
  - 覆盖：多阶段流水线（测试 → 构建 → 发布）、环境变量/密钥、缓存、部署模拟等
- **阶段 6：安全与规范（进阶）**
  - 覆盖：SSH、提交与 Tag 签名、Secrets 使用原则、常见安全坑、LICENSE 与合规

在编写关卡时，尽量让**每条命令都配上一个实际小任务**，而不是只给出干巴巴的命令说明。

---

## 已实现

### 阶段 0：环境与配置 + 终端基础

1. **关卡 00：安装 Git 并完成基础配置**
   - 位置：`docs/lesson-00-install-and-config.md`
   - 目标：安装 Git、配置用户信息、全局 .gitignore、换行符设置
2. **关卡 00b：命令行与工作目录基础（可选）**
   - 位置：`docs/lesson-00-terminal-basics.md`
   - 目标：熟悉 Web 终端，掌握 `pwd` / `ls` / `cd` / `clear` 等基础命令

### 阶段 1：Git 基础操作

1. **关卡 01：从 0 开始，新建仓库并 push 代码**
   - 位置：`docs/lesson-01-init-push.md`
   - 目标：学会在 Web 上创建仓库、本地 clone、commit 与 push
2. **关卡 02：搞懂工作区 / 暂存区 / 本地历史**
   - 位置：`docs/lesson-02-workspace-staging-history.md`
   - 命令：`status`、`diff`、`restore`、`add -p`
3. **关卡 03：远程仓库与同步**
   - 位置：`docs/lesson-03-remote-and-sync.md`
   - 命令：`remote`、`pull`、`fetch`、`push`

### 阶段 2：分支与协作

1. **关卡 04：创建分支 & 提交 PR 合并代码**
   - 位置：`docs/lesson-04-branches-and-pr.md`
   - 命令：`branch`、`switch`、`merge`
2. **关卡 05：制造并解决一次合并冲突**
   - 位置：`docs/lesson-05-merge-conflict.md`
   - 命令：`merge`、手动解决冲突
3. **关卡 06：用 rebase 保持整洁历史**
   - 位置：`docs/lesson-06-rebase-clean-history.md`
   - 命令：`rebase`、交互式 rebase
4. **关卡 06a：配置 SSH 密钥并通过 SSH 访问仓库**
   - 位置：`docs/lesson-06a-ssh-setup-and-clone.md`
   - 命令：`ssh-keygen`、`ssh -T`、`git remote set-url`
5. **关卡 06b：远程协作规则与常见约定**
   - 位置：`docs/lesson-06b-collaboration-conventions.md`
   - 内容：分支命名规范、PR 流程、Code Review、Git Flow / GitHub Flow

### 阶段 3：救火与历史修复

1. **关卡 07：误提交到错误分支的补救**
   - 位置：`docs/lesson-07-cherry-pick-and-revert.md`
   - 命令：`cherry-pick`、`revert`
2. **关卡 08：用 reflog 从「看似没救」的历史中恢复**
   - 位置：`docs/lesson-08-reflog-and-recovery.md`
   - 命令：`reflog`、`reset --soft/--mixed/--hard`
3. **关卡 09：stash 的正确使用姿势**
   - 位置：`docs/lesson-09-stash-usage.md`
   - 命令：`stash push/pop/list/drop/apply`
4. **关卡 20：用 git bisect 定位引入 Bug 的提交**
   - 位置：`docs/lesson-20-bisect.md`
   - 命令：`bisect start/good/bad/reset/run`
5. **关卡 21：用 git worktree 同时检出多个分支**
   - 位置：`docs/lesson-21-worktree.md`
   - 命令：`worktree add/list/remove/prune`

### 阶段 4：进阶操作

1. **关卡 13：Git 标签与版本发布**
    - 位置：`docs/lesson-13-tags-and-releases.md`
    - 命令：`tag`、语义化版本、GitHub Release
2. **关卡 14：GitHub/Gitea 项目文件规范**
    - 位置：`docs/lesson-14-project-files.md`
    - 内容：README、CONTRIBUTING、LICENSE、SECURITY
3. **关卡 15：Git 钩子与自动化**
    - 位置：`docs/lesson-15-git-hooks.md`
    - 内容：pre-commit、Husky、commitlint
4. **关卡 16：Git 性能优化与大仓库**
    - 位置：`docs/lesson-16-large-repo.md`
    - 内容：浅克隆、Git LFS、性能调优
5. **关卡 17：自动维护版本与 Changelog**
   - 位置：`docs/lesson-17-release-automation.md`
   - 内容：Release Please、自动版本号、GitHub Release、Changelog 自动化

### 阶段 5：CI/CD

1. **关卡 10：为仓库添加第一个 CI 工作流**
    - 位置：`docs/lesson-10-first-ci-workflow.md`
    - 内容：Gitea Actions 基础、Workflow / Job / Step
2. **关卡 11：修复一个失败的 CI 流水线**
    - 位置：`docs/lesson-11-fix-broken-pipeline.md`
    - 内容：阅读日志、定位问题、修复流水线
3. **关卡 12：多阶段流水线与敏感信息基础**
    - 位置：`docs/lesson-12-multi-stage-pipeline-and-secrets.md`
    - 内容：多 Job 依赖、Secrets 使用

### 阶段 6：安全与规范

1. **关卡 18：提交签名与标签签名**
    - 位置：`docs/lesson-18-commit-and-tag-signing.md`
    - 内容：GPG 密钥生成、提交签名、标签签名、签名验证
2. **关卡 19：Secrets 与安全实践**
    - 位置：`docs/lesson-19-secrets-and-security.md`
    - 内容：敏感信息管理、.gitignore、历史清除、CI/CD Secrets

---

## 后续可扩展主题（可选）

以下方向尚未单独成课，欢迎贡献 PR：

- 子模块（submodule）与 subtree
- `git filter-repo` 历史改写
-  monorepo 下的多包发布策略

---

## 编写关卡时建议包含的内容

- 场景与目标（为什么要学这一关）
- 本关要掌握的 Git / CI 命令清单
- 具体的「边看边做」步骤（带命令、截图提示）
- 如何确认自己做对了（在 Web / 终端看什么信息）
- 常见错误 & 排查提示
- 思考题 / 扩展练习（可选）

欢迎根据你的需要，在 `docs/` 目录中补充或调整关卡。


