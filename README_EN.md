# Git Workflow Lab

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub release](https://img.shields.io/github/v/release/AlexanderJ-Carter/Git-Workflow-Lab?include_prereleases)](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/releases)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/AlexanderJ-Carter/Git-Workflow-Lab/docker.yml?label=build)](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/actions)
[![Docker Pulls](https://img.shields.io/badge/ghcr.io-alexanderj--carter%2Fgit--workflow--lab-blue)](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/pkgs/container/git-workflow-lab-gitea)
[![GitHub stars](https://img.shields.io/github/stars/AlexanderJ-Carter/Git-Workflow-Lab?style=social)](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/AlexanderJ-Carter/Git-Workflow-Lab?style=social)](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/network/members)
[![GitHub issues](https://img.shields.io/github/issues/AlexanderJ-Carter/Git-Workflow-Lab)](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/issues)

A hands-on teaching repository for Git learning and collaboration practices, focusing on "learning by doing" course experience. The repository covers a complete learning path from Git basics to team collaboration, history recovery, version releases, and CI/CD scenarios.

**[📖 Online Course](https://alexanderj-carter.github.io/Git-Workflow-Lab/)** | **[🚀 Quick Start](#-quick-start)** | **[📚 Learning Path](docs/learning-path.md)** | **[中文文档](README.md)**

---

## ✨ Features

- 🎯 **Scenario-Based Learning** - Each lesson is designed around real-world development scenarios, not boring command lists
- 🐳 **Complete Lab Environment** - Docker Compose one-click deployment of Gitea + Web Terminal environment
- 📦 **Engineering Practices** - Built-in Release Please, GitHub Actions, container publishing, and complete CI/CD examples
- 🌐 **Dual-Mode Operation** - GitHub Pages for public courses, local environment for complete lab experience
- 🔄 **Continuous Updates** - Active community contributions and continuous content iteration

## 📖 About This Project

The core goal of Git Workflow Lab is to break down common Git learning content into practical lessons. Each lesson revolves around real development scenarios rather than just providing command lists.

You can use it as:

- A systematic Git course repository
- A collection of practice content suitable for teaching and self-learning
- A sustainable open-source learning project

## 🚀 Quick Start

### Online Learning (Recommended for Beginners)

Visit the **[Online Course Website](https://alexanderj-carter.github.io/Git-Workflow-Lab/)** directly to browse course content and documentation.

### Local Lab Environment (Advanced Users)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/AlexanderJ-Carter/Git-Workflow-Lab.git
   cd Git-Workflow-Lab
   ```

2. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env file and modify all REQUIRED variables (passwords, keys, etc.)
   # Generate random password: openssl rand -base64 24
   ```

3. **Start Lab Environment**
   ```bash
   # Using Make (recommended)
   make docker-up

   # Or using Docker Compose directly
   docker-compose up -d
   ```

4. **Access Services**
   - 📚 Tutorial Website: http://localhost:8081
   - 🎓 Learning Workspace: http://localhost:8081/workspace.html
   - 🐙 Gitea Platform: http://localhost:3000
   - 💻 Web Terminal: http://localhost:8080

5. **Stop Environment**
   ```bash
   make docker-down
   # Or
   docker-compose down
   ```

For detailed configuration, refer to [Environment Configuration Documentation](docs/lesson-00-install-and-config.md).

### Build Documentation (Developers)

This project uses [Sphinx](https://www.sphinx-doc.org/) to build technical documentation.

```bash
# Install documentation build dependencies
pip install -r docs-requirements.txt

# Build documentation
make docs
# Or
cd docs-sphinx && make html

# Preview documentation locally
make docs-serve
# Visit http://localhost:8000
```

Sphinx documentation provides:
- Complete API reference
- Detailed architecture documentation
- Developer guides
- Searchable documentation index

---

## 📚 Course Content

- **Stage 0-1**: Installation configuration, terminal basics, repository initialization, remote synchronization
- **Stage 2**: Branch collaboration, Pull Requests, conflict resolution, rebase, SSH and collaboration standards
- **Stage 3**: cherry-pick, revert, reflog, stash and other rescue and recovery scenarios
- **Stage 4**: Tags and releases, project standards, Git hooks, large repository practices
- **Stage 5**: CI basics, pipeline repair, multi-stage processes and release practices

## 📋 Recommended Reading Order

1. [Course Overview](docs/lessons-overview.md)
2. [Learning Path](docs/learning-path.md)
3. [FAQ](docs/faq.md)

## 📁 Repository Navigation

- [docs](docs): Course content and learning documentation
- [site](site): Website pages and course entry points
- [scripts](scripts): Content build and initialization scripts
- [docker](docker): Terminal-related container definitions
- [.github](.github): Collaboration templates and workflow configurations

## 👥 Who Is This For

- Beginners who want to systematically learn Git
- Developers who want to establish team collaboration standards
- Maintainers who want to consolidate Git teaching content into repository courses

## 🤝 Contributing

We welcome all forms of contributions!

### Ways to Contribute

- 📝 Submit course revisions, bug fixes, content enhancements
- 🐛 Report bugs or suggest features
- 📖 Improve documentation and translations
- 🎨 Optimize user experience and interface design

### Development Tools

The project provides a Makefile to simplify common operations:

```bash
# View all available commands
make help

# Common commands
make install        # Install dependencies
make build          # Build static website
make docs           # Build Sphinx documentation
make docs-serve     # Preview documentation locally
make lint           # Code checking
make fix-quotes     # Fix Chinese quotation marks
```

### Contributing Guide

Before submitting a PR, please read the [Contributing Guide](CONTRIBUTING.md) to understand:
- Course format standards
- Commit message standards
- Branch naming conventions
- PR checklist

### Contributors

Thanks to all developers who have contributed to this project!

<a href="https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=AlexanderJ-Carter/Git-Workflow-Lab" alt="Contributor avatars" />
</a>

## 💬 Community & Feedback

- 💡 [Feature Suggestions](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/issues/new?template=feature_request.md)
- 🐛 [Bug Reports](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/issues/new?template=bug_report.md)
- 📧 Contact Maintainers: Check [CODEOWNERS](.github/CODEOWNERS)

---

## 🗺️ Project Roadmap

We plan to add in the future:

- [ ] Course progress tracking functionality
- [ ] Interactive exercises
- [ ] Multi-language support (English)
- [ ] Course completion badges
- [ ] Video tutorial supplements
- [ ] Git advanced topics (submodules, worktrees, etc.)

For detailed planning, see [ROADMAP.md](ROADMAP.md).

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- Thanks to [Gitea](https://gitea.io/) for providing a lightweight Git hosting platform
- Thanks to all contributors for their efforts
- If this project helps you, please give us a ⭐ Star!

---

<p align="center">
  Made with ❤️ by the Git Workflow Lab community
</p>
