# CLAUDE.md

Project: Git Workflow Lab - Git 与 CI/CD 教学仓库

## 项目概述

这是一个面向 Git 学习与协作实践的教学仓库，聚焦"边看边做"的课程体验。包含：
- 系统化的 Git 课程（17+ 课时）
- Docker Compose 一键部署的 Gitea + Web 终端实验环境
- 完整的 CI/CD 示例（GitHub Actions、Release Please）
- 双模式运行：GitHub Pages 展示 + 本地实验环境

## 技术栈

- **前端**: 纯 HTML/CSS/JavaScript（无框架）
- **后端服务**: Docker Compose
  - Nginx（静态网站）
  - Gitea（Git 托管）
  - PostgreSQL（数据库）
  - ttyd（Web 终端）
- **CI/CD**: GitHub Actions

## 目录结构

```
.
├── site/                    # 网站源码（展示页面）
│   ├── index.html          # 首页
│   ├── workspace.html      # 学习工作台
│   └── assets/             # CSS/JS 资源
├── docs/                   # 课程文档（Markdown）
│   ├── lesson-*.md         # 各课时内容
│   ├── lessons-overview.md # 课程总览
│   └── learning-path.md    # 学习路径
├── _site/                  # GitHub Pages 构建输出
├── docker/                 # Docker 配置
│   └── terminal/           # Web 终端容器
├── scripts/                # 脚本
│   └── init-gitea.sh       # Gitea 初始化脚本
├── .github/                # GitHub 配置
│   ├── workflows/          # Actions 工作流
│   └── ISSUE_TEMPLATE/     # Issue 模板
└── docker-compose.yml      # 本地实验环境
```


### 本地开发命令

### 启动实验环境
```bash
docker-compose up -d
```

### 停止环境
```bash
docker-compose down
```

### 查看日志
```bash
docker-compose logs -f
```

## 服务端口

| 服务 | 端口 | 说明 |
|------|------|------|
| 教程网站 | 8081 | Nginx 静态网站 |
| Web 终端 | 8080 | ttyd 终端 |
| Gitea | 3000 | Git 托管平台 |
| Gitea SSH | 2222 | SSH 访问 |

## 工作流

### GitHub Actions
- `pages.yml` - GitHub Pages 部署
- `check-lessons.yml` - 课程内容检查
- `release-please.yml` - 自动版本发布
- `docker.yml` - Docker 镜像构建
- `code-quality.yml` - 代码质量检查
- `security-scan.yml` - 安全扫描

### 构建网站

静态网站使用 GitHub Pages 部署，构建源在 `_site/` 目录。

## 课程体系

### 阶段 0-1: 基础与同步

- 安装配置、终端基础、commit、push、pull

### 阶段 2: 分支与协作

- 分支、PR、冲突处理、rebase、SSH

### 阶段 3: 救火与恢复

- cherry-pick、revert、reflog、stash

### 阶段 4-5: 发布与自动化

- 标签、Release、CI/CD、Secrets

## 站点功能页面

### 学习辅助

- `ai-assistant.html` - AI 问答助手（需用户自己提供 API Key）
- `flashcards.html` - 记忆闪卡系统（间隔重复学习）
- `quiz.html` - 技能测验（含 17+ 课程题目）
- `cheatsheet.html` - Git 命令速查表（支持搜索和点击复制）
- `best-practices.html` - 最佳实践指南

### 实践练习

- `playground.html` - 命令练习场
- `challenges.html` - 场景挑战
- `workspace.html` - 学习工作台（需本地 Docker 环境）

### 其他页面

- `interview.html` - 面试题库
- `gamification.html` - 游戏化系统
- `skill-tree.html` - 技能树
- `learning-path.html` - 学习路径可视化

## 注意事项

1. 本地环境依赖 Docker 和 Docker Compose
2. 首次启动需要配置 `.env` 文件（参考 `.env.example`）
3. Gitea 初始化数据在 `scripts/init-gitea.sh`
4. 课程文档使用 Markdown 格式，保存在 `docs/` 目录
