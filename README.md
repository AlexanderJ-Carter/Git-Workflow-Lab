# Git Workflow Lab

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Pages](https://img.shields.io/github/actions/workflow/status/AlexanderJ-Carter/Git-Workflow-Lab/pages.yml?label=pages)](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/actions/workflows/pages.yml)
[![Containers](https://img.shields.io/github/actions/workflow/status/AlexanderJ-Carter/Git-Workflow-Lab/docker.yml?label=containers)](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/actions/workflows/docker.yml)

一个在浏览器里边看边练 Git、Gitea 和 CI/CD 的本地教学实验室。

GitHub 仓库地址：https://github.com/AlexanderJ-Carter/Git-Workflow-Lab

## 项目定位

这个项目分成两种使用形态：

- 本地实验环境：通过 Docker Compose 启动完整学习平台，包含教程站点、Gitea 和 Web 终端。
- 公开文档站点：通过 GitHub Pages 发布课程说明和学习路径，不承载本地 Gitea / 终端服务。

这样做的好处是，公开页面负责展示和引流，本地环境负责真正动手练习，两者职责清晰，不会再把 localhost 服务暴露成“线上可用”。

## 核心特性

- 浏览器内完成教程阅读、Git 托管和终端练习。
- 课程结构覆盖 Git 基础、分支协作、历史修复、标签发布和 CI/CD。
- 新增自动发布链路，支持 Release Please 自动维护 changelog、版本号和 GitHub Release。
- 统一的 Linux 学习环境，减少 Windows / macOS / Linux 差异带来的干扰。
- 支持本地 Gitea SSH 练习，默认映射 SSH 端口 2222。
- 内置 GitHub Actions 配置，可发布公开文档和容器镜像。

## 快速开始

### 1. 克隆仓库

```bash
git clone git@github.com:AlexanderJ-Carter/Git-Workflow-Lab.git
cd git-workflow-lab
```

### 2. 准备环境变量

```bash
cp .env.example .env
```

如果你只是本机自用，可以先直接用默认值；如果你要把服务暴露给局域网其他机器，请先把 `.env` 里的密码和密钥改掉。

### 3. 启动本地实验环境

```bash
docker compose up -d --build
```

### 4. 打开学习入口

| 服务       | 地址                                 | 说明                  |
| ---------- | ------------------------------------ | --------------------- |
| 学习工作台 | http://localhost:8081/workspace.html | 左侧教程，右侧终端    |
| 教程首页   | http://localhost:8081                | 本地课程入口          |
| Gitea      | http://localhost:3000                | Git 托管与 PR 练习    |
| Web 终端   | http://localhost:8080                | 浏览器内终端环境      |
| Gitea SSH  | ssh://git@localhost:2222             | SSH clone / push 练习 |

### 5. 本地默认账号

默认管理员账号来自 `.env`：

- 用户名：`playground`
- 密码：`.env` 里的 `GITEA_ADMIN_PASSWORD`

也可以在 Gitea 中自己注册普通学习账号，再按课程流程练习。

## 公开发布建议

### GitHub Pages

Pages 只建议发布公开文档和课程内容，不要把本地实验入口当成线上 SaaS 去暴露。当前仓库已经包含 Pages 工作流，推送到默认分支后即可从 Actions 构建公开站点。

### GHCR 镜像发布

当前仓库已拆分出两类镜像发布目标：

- `ghcr.io/alexanderj-carter/git-workflow-lab-gitea`
- `ghcr.io/alexanderj-carter/git-workflow-lab-terminal`

当你创建 GitHub Release 后，Actions 会按 release tag 生成镜像标签并发布到 GHCR。

### 版本号与修改日志

当前仓库已经接入 Release Please，推荐使用这个流程：

1. 开发分支和日常提交使用约定式提交，例如 `feat:`、`fix:`、`docs:`。
2. Release Please 自动生成 Release PR 和 [CHANGELOG.md](CHANGELOG.md) 变更。
3. 合并 Release PR 后，GitHub 自动创建 Tag 和 Release。
4. Docker 发布工作流基于正式 Release 自动推送镜像。

## 学习内容范围

当前课程已经覆盖这些阶段：

- 阶段 0-1：Git 安装、配置、终端基础、仓库初始化、远程同步。
- 阶段 2：分支、PR、冲突、rebase、SSH 和协作规范。
- 阶段 3：cherry-pick、revert、reflog、stash 等修复场景。
- 阶段 4-5：标签与版本、项目规范、Hooks、CI/CD 工作流、自动发布。

推荐先从 [docs/lessons-overview.md](docs/lessons-overview.md) 和 [docs/learning-path.md](docs/learning-path.md) 开始。

## 环境重置

如果你想彻底清空本地实验数据：

```bash
docker compose down -v
docker compose up -d --build
```

当前 Compose 使用命名卷保存 Gitea、PostgreSQL 和终端数据，因此不会再把运行时数据库文件直接写进仓库目录。

## 项目结构

```text
.
├── docs/                    # 课程文档
├── site/                    # 本地站点入口
├── docker/
│   └── terminal/            # Web 终端与 code-server 镜像
├── scripts/                 # 初始化与构建脚本
├── .github/workflows/       # Pages / 镜像发布 / 内容检查
├── docker-compose.yml       # 本地实验环境编排
├── CHANGELOG.md             # 修改日志
├── .env.example             # 环境变量示例
├── CONTRIBUTING.md          # 贡献指南
├── SECURITY.md              # 安全政策
└── LICENSE                  # MIT 许可证
```

## 仓库后续建议

当前仓库接下来建议优先补这几项：

1. 开启 GitHub Pages，并确认它从 Actions 发布。
2. 开启 Discussions，给课程反馈和提问留入口。
3. 在仓库 About 中补上项目简介和 Topics。
4. 创建首个 Release，验证 GHCR 发布链路。

## 贡献

欢迎补课程、修文档、加案例或完善工作流。规范见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 链接

- 仓库主页：https://github.com/AlexanderJ-Carter/Git-Workflow-Lab
- Issues：https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/issues
- Discussions：https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/discussions

## 许可证

本项目采用 [MIT 许可证](LICENSE)。
