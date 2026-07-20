# 关卡总览：边看边练的 Git & CI 全流程

本实验平台提供一系列循序渐进的关卡，设计原则是：**左边看指南，右边动手练**。

推荐的打开方式：

- 一边打开 `docs/*.md`（在编辑器 / 浏览器中）
- 一边打开 `http://localhost:8081`（教程站点）、`http://localhost:3000`（Gitea）+ `http://localhost:8080`（Web 终端）

照着每个关卡的步骤，一条命令一条命令地敲，一步步完成练习。

> **编号说明：** 关卡文件编号（00–29）保持不变，便于进度记录与外链。**推荐学习顺序**见下方「逻辑阶段 A–H」，与文件名编号不必一致。

---

## 逻辑阶段 A–H（推荐学习顺序）

| 逻辑阶段 | 主题 | 推荐顺序 | 关卡文件 |
|----------|------|----------|----------|
| **A** 环境与终端 | 安装、配置、命令行基础 | 1 → 2 | [00](./lesson-00-install-and-config.md)、[00b](./lesson-00-terminal-basics.md) |
| **B** Git 基础 | init、工作区、远程同步 | 3 → 5 | [01](./lesson-01-init-push.md)、[02](./lesson-02-workspace-staging-history.md)、[03](./lesson-03-remote-and-sync.md) |
| **C** 分支与协作 | 分支、冲突、rebase、SSH、规范 | 6 → 11 | [04](./lesson-04-branches-and-pr.md)、[05](./lesson-05-merge-conflict.md)、[06](./lesson-06-rebase-clean-history.md)、[06a](./lesson-06a-ssh-setup-and-clone.md)、[06b](./lesson-06b-collaboration-conventions.md) |
| **D** 救火与恢复 | cherry-pick、reflog、stash、bisect、worktree | 12 → 16 | [07](./lesson-07-cherry-pick-and-revert.md)、[08](./lesson-08-reflog-and-recovery.md)、[09](./lesson-09-stash-usage.md)、[20](./lesson-20-bisect.md)、[21](./lesson-21-worktree.md) |
| **E** 工程化与发布 | 标签、项目文件、钩子、大仓库、Release、提交规范、PR 审查 | 17 → 24 | [13](./lesson-13-tags-and-releases.md)、[14](./lesson-14-project-files.md)、[15](./lesson-15-git-hooks.md)、[16](./lesson-16-large-repo.md)、[17](./lesson-17-release-automation.md)、[22](./lesson-22-conventional-commits.md)、[23](./lesson-23-code-review-pr.md) |
| **F** CI/CD | 首个流水线、修复失败、多阶段与 Secrets | 25 → 27 | [10](./lesson-10-first-ci-workflow.md)、[11](./lesson-11-fix-broken-pipeline.md)、[12](./lesson-12-multi-stage-pipeline-and-secrets.md) |
| **G** 安全与合规 | 签名、Secrets 实践 | 28 → 29 | [18](./lesson-18-commit-and-tag-signing.md)、[19](./lesson-19-secrets-and-security.md) |
| **H** 进阶实用 | fork、hotfix、submodule、rebase 进阶、历史考古、sparse checkout | 30 → 35 | [24](./lesson-24-fork-and-upstream.md)、[25](./lesson-25-hotfix-workflow.md)、[26](./lesson-26-submodule.md)、[27](./lesson-27-interactive-rebase-fixup.md)、[28](./lesson-28-blame-and-archaeology.md)、[29](./lesson-29-sparse-checkout.md) |

**完整推荐路径（按阶段）：**

```text
A(00→00b) → B(01→03) → C(04→06b) → D(07→09,20→21) → E(13→17,22→23) → F(10→12) → G(18→19) → H(24→29)
```

---

## 全部关卡索引（00–29）

### 阶段 A：环境与配置

| 关卡 | 文件 | 要点 |
|------|------|------|
| 00 | [lesson-00-install-and-config.md](./lesson-00-install-and-config.md) | 安装 Git、`git config`、`.gitignore` |
| 00b | [lesson-00-terminal-basics.md](./lesson-00-terminal-basics.md) | Web 终端、`pwd`/`ls`/`cd`（可选） |

### 阶段 B：Git 基础操作

| 关卡 | 文件 | 要点 |
|------|------|------|
| 01 | [lesson-01-init-push.md](./lesson-01-init-push.md) | 新建仓库、clone、commit、push |
| 02 | [lesson-02-workspace-staging-history.md](./lesson-02-workspace-staging-history.md) | 工作区/暂存区、`diff`、`restore` |
| 03 | [lesson-03-remote-and-sync.md](./lesson-03-remote-and-sync.md) | `remote`、`fetch`、`pull`、`push` |

### 阶段 C：分支与协作

| 关卡 | 文件 | 要点 |
|------|------|------|
| 04 | [lesson-04-branches-and-pr.md](./lesson-04-branches-and-pr.md) | 分支、Gitea Pull Request |
| 05 | [lesson-05-merge-conflict.md](./lesson-05-merge-conflict.md) | 合并冲突解决 |
| 06 | [lesson-06-rebase-clean-history.md](./lesson-06-rebase-clean-history.md) | rebase、交互式 rebase 入门 |
| 06a | [lesson-06a-ssh-setup-and-clone.md](./lesson-06a-ssh-setup-and-clone.md) | SSH 密钥、`:2222` clone |
| 06b | [lesson-06b-collaboration-conventions.md](./lesson-06b-collaboration-conventions.md) | 分支命名、Review、Git Flow |

### 阶段 D：救火与历史修复

| 关卡 | 文件 | 要点 |
|------|------|------|
| 07 | [lesson-07-cherry-pick-and-revert.md](./lesson-07-cherry-pick-and-revert.md) | cherry-pick、revert |
| 08 | [lesson-08-reflog-and-recovery.md](./lesson-08-reflog-and-recovery.md) | reflog、reset |
| 09 | [lesson-09-stash-usage.md](./lesson-09-stash-usage.md) | stash |
| 20 | [lesson-20-bisect.md](./lesson-20-bisect.md) | 二分定位 Bug |
| 21 | [lesson-21-worktree.md](./lesson-21-worktree.md) | 多工作目录并行 |

### 阶段 E：工程化与发布

| 关卡 | 文件 | 要点 |
|------|------|------|
| 13 | [lesson-13-tags-and-releases.md](./lesson-13-tags-and-releases.md) | tag、Release |
| 14 | [lesson-14-project-files.md](./lesson-14-project-files.md) | README、LICENSE、CONTRIBUTING |
| 15 | [lesson-15-git-hooks.md](./lesson-15-git-hooks.md) | pre-commit、commitlint |
| 16 | [lesson-16-large-repo.md](./lesson-16-large-repo.md) | 浅克隆、LFS |
| 17 | [lesson-17-release-automation.md](./lesson-17-release-automation.md) | Release Please、Changelog |
| 22 | [lesson-22-conventional-commits.md](./lesson-22-conventional-commits.md) | Conventional Commits、`feat`/`fix`/`docs` |
| 23 | [lesson-23-code-review-pr.md](./lesson-23-code-review-pr.md) | PR 审查、diff、评论与合并 |

### 阶段 F：CI/CD

| 关卡 | 文件 | 要点 |
|------|------|------|
| 10 | [lesson-10-first-ci-workflow.md](./lesson-10-first-ci-workflow.md) | 首个 Gitea Actions 工作流 |
| 11 | [lesson-11-fix-broken-pipeline.md](./lesson-11-fix-broken-pipeline.md) | 读日志、修流水线 |
| 12 | [lesson-12-multi-stage-pipeline-and-secrets.md](./lesson-12-multi-stage-pipeline-and-secrets.md) | 多 Job、Secrets |

### 阶段 G：安全与规范

| 关卡 | 文件 | 要点 |
|------|------|------|
| 18 | [lesson-18-commit-and-tag-signing.md](./lesson-18-commit-and-tag-signing.md) | GPG 提交/标签签名 |
| 19 | [lesson-19-secrets-and-security.md](./lesson-19-secrets-and-security.md) | Secrets、历史清除 |

### 阶段 H：进阶实用

| 关卡 | 文件 | 要点 |
|------|------|------|
| 24 | [lesson-24-fork-and-upstream.md](./lesson-24-fork-and-upstream.md) | fork、`upstream` remote、同步 |
| 25 | [lesson-25-hotfix-workflow.md](./lesson-25-hotfix-workflow.md) | 生产 hotfix、tag、回灌 develop |
| 26 | [lesson-26-submodule.md](./lesson-26-submodule.md) | submodule add/update、常见坑 |
| 27 | [lesson-27-interactive-rebase-fixup.md](./lesson-27-interactive-rebase-fixup.md) | fixup、squash、autosquash |
| 28 | [lesson-28-blame-and-archaeology.md](./lesson-28-blame-and-archaeology.md) | blame、log -S/-G、--follow |
| 29 | [lesson-29-sparse-checkout.md](./lesson-29-sparse-checkout.md) | sparse-checkout cone、partial clone |

---

## 演示仓库与端口

| 资源 | 地址 | 用途 |
|------|------|------|
| 教程站点 | http://localhost:8081 | 课程导航、工作台 |
| Web 终端 | http://localhost:8080 | 执行 Git 命令 |
| Gitea | http://localhost:3000 | `playground-hello`、`playground-ci` |
| Gitea SSH | localhost:2222 | SSH clone |

启动环境：`docker compose up -d`

---

## 编写关卡时建议包含的内容

- 场景与目标（为什么要学这一关）
- 本关要掌握的 Git / CI 命令清单
- 具体的「边看边做」步骤（带命令、预期输出）
- 如何确认自己做对了（验证清单）
- 常见错误 & 排查提示
- 扩展练习

欢迎根据你的需要，在 `docs/` 目录中补充或调整关卡。
