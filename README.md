# Git Workflow Lab

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub release](https://img.shields.io/github/v/release/AlexanderJ-Carter/Git-Workflow-Lab?include_prereleases)](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/releases)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/AlexanderJ-Carter/Git-Workflow-Lab/docker.yml?label=build)](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/actions)
[![Docker Pulls](https://img.shields.io/badge/ghcr.io-alexanderj--carter%2Fgit--workflow--lab-blue)](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/pkgs/container/git-workflow-lab-gitea)
[![GitHub stars](https://img.shields.io/github/stars/AlexanderJ-Carter/Git-Workflow-Lab?style=social)](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/AlexanderJ-Carter/Git-Workflow-Lab?style=social)](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/network/members)
[![GitHub issues](https://img.shields.io/github/issues/AlexanderJ-Carter/Git-Workflow-Lab)](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/issues)

一个面向 Git 学习与协作实践的教学仓库，聚焦”边看边做”的课程体验。仓库内容覆盖从 Git 基础到团队协作、历史修复、版本发布与 CI 场景的完整学习路径。

**[📖 在线课程](https://alexanderj-carter.github.io/Git-Workflow-Lab/)** | **[🚀 快速开始](#-快速开始)** | **[📚 学习路径](docs/learning-path.md)** | **[🇺🇸 English](README_EN.md)**

---

## ✨ 项目特点

- 🎯 **场景化学习** - 每个关卡都围绕真实开发场景设计，而非枯燥的命令列表
- 🐳 **完整实验环境** - 提供 Docker Compose 一键部署的 Gitea + Web 终端环境
- 📦 **工程化实践** - 内置 Release Please、GitHub Actions、容器发布等完整 CI/CD 示例
- 🌐 **双模式运行** - GitHub Pages 展示公开课程，本地环境提供完整实验体验
- 🔄 **持续更新** - 活跃的社区贡献和持续的内容迭代

## 项目简介

Git Workflow Lab 的核心目标是把常见 Git 学习内容拆成可实践的关卡，每一关都围绕真实开发场景展开，而不是只给命令列表。

你可以把它当作：

- 一套系统化的 Git 课程仓库
- 一个适合教学与自学的练习内容集合
- 一个可持续扩展的开源学习项目

## 🚀 快速开始

### 在线学习（推荐新手）

直接访问 **[在线课程网站](https://alexanderj-carter.github.io/Git-Workflow-Lab/)** 浏览课程内容和文档。

### 本地实验环境（进阶用户）

1. **克隆仓库**
   ```bash
   git clone https://github.com/AlexanderJ-Carter/Git-Workflow-Lab.git
   cd Git-Workflow-Lab
   ```

2. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，修改所有 REQUIRED 变量（密码、密钥等）
   # 生成随机密码: openssl rand -base64 24
   ```

3. **启动实验环境**
   ```bash
   # 使用 Make（推荐）
   make docker-up

   # 或直接使用 Docker Compose
   docker-compose up -d
   ```

4. **访问服务**
   - 📚 教程网站: http://localhost:8081
   - 🎓 学习工作台: http://localhost:8081/workspace.html
   - 🐙 Gitea 平台: http://localhost:3000
   - 💻 Web 终端: http://localhost:8080

5. **停止环境**
   ```bash
   make docker-down
   # 或
   docker-compose down
   ```

详细配置请参考 [环境配置文档](docs/lesson-00-install-and-config.md)。

### 构建文档（开发者）

本项目使用 [Sphinx](https://www.sphinx-doc.org/) 构建技术文档。

```bash
# 安装文档构建依赖
pip install -r docs-requirements.txt

# 构建文档
make docs
# 或
cd docs-sphinx && make html

# 本地预览文档
make docs-serve
# 访问 http://localhost:8000
```

Sphinx 文档提供：
- 完整的 API 参考
- 详细的架构说明
- 开发者指南
- 可搜索的文档索引

---

## 📚 课程内容

- 阶段 0-1：安装配置、终端基础、仓库初始化、远程同步
- 阶段 2：分支协作、Pull Request、冲突处理、rebase、SSH 与协作规范
- 阶段 3：cherry-pick、revert、reflog、stash 等救火与恢复场景
- 阶段 4：标签与版本、项目规范、Git hooks、大仓库实践
- 阶段 5：CI 基础、流水线修复、多阶段流程与发布实践

## 📋 推荐阅读顺序

1. [课程总览](docs/lessons-overview.md)
2. [学习路径](docs/learning-path.md)
3. [常见问题](docs/faq.md)

## 📁 仓库导航

- [docs](docs): 课程正文与学习文档
- [site](site): 站点页面与课程入口
- [scripts](scripts): 内容构建与初始化脚本
- [docker](docker): 终端相关容器定义
- [.github](.github): 协作模板与工作流配置

## 👥 适合人群

- 想系统学习 Git 的新手
- 想建立团队协作规范的开发者
- 想把 Git 教学内容沉淀为仓库课程的维护者

## 🤝 参与贡献

我们欢迎各种形式的贡献！

### 贡献方式

- 📝 提交课程修订、错漏修复、内容增强
- 🐛 报告 Bug 或提出功能建议
- 📖 改进文档和翻译
- 🎨 优化用户体验和界面设计

### 开发工具

项目提供 Makefile 简化常用操作：

```bash
# 查看所有可用命令
make help

# 常用命令
make install        # 安装依赖
make build          # 构建静态网站
make docs           # 构建 Sphinx 文档
make docs-serve     # 本地预览文档
make lint           # 代码检查
make fix-quotes     # 修复中文引号
```

### 贡献指南

提交 PR 前请阅读 [贡献指南](CONTRIBUTING.md)，了解：
- 课程格式规范
- 提交信息规范
- 分支命名规范
- PR 检查清单

### 贡献者

感谢所有为这个项目做出贡献的开发者！

<!-- 可以使用 all-contributors 自动生成 -->
<a href="https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=AlexanderJ-Carter/Git-Workflow-Lab" alt="贡献者头像" />
</a>

## 💬 社区与反馈

- 💡 [功能建议](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/issues/new?template=feature_request.md)
- 🐛 [问题反馈](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/issues/new?template=bug_report.md)
- 📧 联系维护者: 查看 [CODEOWNERS](.github/CODEOWNERS)

---

## 🗺️ 项目路线图

我们计划在未来添加：

- [x] 课程进度跟踪功能
- [x] 互动式练习题
- [x] 多语言支持（English）
- [ ] 课程完成徽章
- [ ] 视频教程补充
- [ ] Git 进阶主题（子模块、工作树等）

详细规划请查看 [ROADMAP.md](ROADMAP.md)。

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 致谢

- 感谢 [Gitea](https://gitea.io/) 提供轻量级的 Git 托管平台
- 感谢所有贡献者的付出
- 如果这个项目对你有帮助，请给我们一个 ⭐ Star！

---

<p align="center">
  Made with ❤️ by the Git Workflow Lab community
</p>
