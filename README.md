# Git Workflow Lab

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Pages](https://img.shields.io/github/actions/workflow/status/AlexanderJ-Carter/Git-Workflow-Lab/pages.yml?label=pages)](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/actions/workflows/pages.yml)
[![Containers](https://img.shields.io/github/actions/workflow/status/AlexanderJ-Carter/Git-Workflow-Lab/docker.yml?label=containers)](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/actions/workflows/docker.yml)
[![Release Please](https://img.shields.io/github/actions/workflow/status/AlexanderJ-Carter/Git-Workflow-Lab/release-please.yml?label=release-please)](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/actions/workflows/release-please.yml)

一个围绕 Git、Gitea、协作流程和 CI/CD 的教学型仓库。它既是一套系统课程，也是一套可本地运行的浏览器实验环境，同时还是一个演示如何用 GitHub Actions、GitHub Pages、Release Please 和 GHCR 组织开源项目发布流程的真实示例。

## 这个仓库有什么

- 一套循序渐进的课程，从 Git 基础一路覆盖到分支协作、历史修复、标签发布和自动发布。
- 一个浏览器实验室设计：教程、Gitea 和终端可以在本地组合成完整练习环境。
- 一套仓库工程化配置：课程校验、文档站构建、自动发布、容器镜像发布。
- 一份对外展示用的文档站点，适合把课程内容公开发布到 GitHub Pages。

## 仓库亮点

- 课程不是命令清单，而是按场景组织的“边看边做”练习。
- 课程内容和仓库本身互相呼应，学到的 Tag、Release、Hooks、CI/CD 都能在本仓库里看到真实用法。
- 支持 Release Please 自动维护版本和 changelog，减少手工维护发布说明的成本。
- 支持多组件容器发布，面向 GHCR 输出 Gitea 与 terminal 两类镜像。

## 课程地图

- 阶段 0-1：Git 安装、配置、终端基础、仓库初始化、远程同步。
- 阶段 2：分支、PR、冲突、rebase、SSH 和协作规范。
- 阶段 3：cherry-pick、revert、reflog、stash 等修复场景。
- 阶段 4：标签与版本、项目规范、Hooks、大仓库与性能。
- 阶段 5：CI 工作流、多阶段流水线、Secrets、自动发布。

推荐从 [docs/lessons-overview.md](docs/lessons-overview.md) 和 [docs/learning-path.md](docs/learning-path.md) 开始。

## 仓库结构

```text
.
├── docs/                    # 课程内容与本地文档查看器
├── site/                    # 对外展示首页与本地工作台入口
├── docker/                  # Web 终端与可选 code-server 镜像定义
├── scripts/                 # 构建与初始化脚本
├── .github/workflows/       # 课程检查、Pages、Release Please、容器发布
├── docker-compose.yml       # 本地浏览器实验环境编排
├── release-please-config.json
├── CHANGELOG.md
└── .env.example
```

## 自动化能力

本仓库当前包含这些自动化能力：

- `check-lessons.yml`：检查课程标题、章节结构和基础格式。
- `pages.yml`：把课程和项目介绍构建成 GitHub Pages 可用的静态站点。
- `release-please.yml`：自动维护 Release PR、版本号和 changelog。
- `docker.yml`：在正式 Release 后构建并发布 GHCR 镜像。

## 适合谁

- 想系统学习 Git 和协作流程的人。
- 想搭一套可演示、可本地练习的教学仓库的人。
- 想把文档站、发布流程、容器发布整合进同一个开源仓库的人。

## 本地实验环境

如果你想把这个仓库当作浏览器实验室来运行，核心入口在这些文件里：

- [docker-compose.yml](docker-compose.yml)
- [site/index.html](site/index.html)
- [site/workspace.html](site/workspace.html)
- [scripts/init-gitea.sh](scripts/init-gitea.sh)

README 不再展开具体部署步骤，保持面向仓库本身；本地运行细节由课程、站点页面和配置文件承担。

## 路线图

- 补齐剩余课程的章节模板一致性。
- 继续增强 GitHub Pages 的公开展示效果。
- 完善 GHCR 发布说明、Issue / PR 模板和仓库社区文件。

## 参与贡献

欢迎补课程、修文档、改工作流、补案例。参与前建议先看 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 仓库链接

- 仓库主页：https://github.com/AlexanderJ-Carter/Git-Workflow-Lab
- Issues：https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/issues
- Discussions：https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/discussions

## 许可证

本项目采用 [MIT 许可证](LICENSE)。
