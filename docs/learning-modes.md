# 学习模式说明：在线 vs 本地 Docker

Git Workflow Lab 支持 **两种互补的学习方式**。你可以只读在线课程，也可以启动完整 Docker 实验环境「边看边做」。本页说明差异、功能对照与快速上手路径。

---

## 双模式概览

### 🌐 GitHub Pages（在线模式）

- **地址**：部署后的 GitHub Pages 站点（仓库 Settings → Pages 所示 URL；本地构建对应 `_site/` 内容）。
- **适合**：阅读课程文档、使用测验/闪卡/命令练习场、了解概念与流程。
- **无需**：Docker、本地端口、Gitea 实例。
- **限制**：无法打开真实 Web 终端、无法 push 到本地 Gitea、无法运行 `docker compose` 实验。

### 🐳 本地 Docker（实验模式）

- **启动**：在仓库根目录执行 `docker compose up -d`（参见 [快速开始](../site/quick-start.html)）。
- **适合**：完整 Git 操作、Gitea PR、SSH clone、Shell/网络/Docker 动手关（30–38 等）。
- **服务端口**：

| 服务 | URL | 用途 |
|------|-----|------|
| 教程站点 | http://localhost:8081 | 导航、工作台、文档 viewer |
| Web 终端 | http://localhost:8080 | 真实 Shell，执行命令 |
| Gitea | http://localhost:3000 | Git 托管、`playground-hello` |
| Gitea SSH | localhost:2222 | SSH clone |

---

## 功能与模式对照表

| 功能 | 🌐 在线 Pages | 🐳 本地 Docker |
|------|:-------------:|:--------------:|
| 阅读 `docs/` 课程 Markdown | ✓ | ✓（8081/docs 或编辑器） |
| [技能测验](../site/quiz.html) | ✓ | ✓ |
| [闪卡](../site/flashcards.html) | ✓ | ✓ |
| [命令练习场 / 模拟器](../site/playground.html) | ✓ | ✓ |
| [速查表](../site/cheatsheet.html) | ✓ | ✓ |
| [学习路径](./learning-path.md) / [关卡总览](./lessons-overview.md) | ✓ | ✓ |
| [学习工作台](../site/workspace.html) 分屏终端 | — | ✓ |
| Web 终端 ttyd（真实命令） | — | ✓ :8080 |
| Gitea 建库 / push / PR | — | ✓ :3000 |
| SSH clone（:2222） | — | ✓ |
| `playground-hello` / `playground-ci` 演示 | — | ✓ |
| Docker / 进程 / 端口排查（关卡 33–34、37） | 只读概念 | ✓ 动手 |
| Gitea API + curl（关卡 35） | 公网 demo | ✓ 本地 API |
| 修改 `docker-compose.yml` 并验证 | 只读 | ✓ |
| Python / PowerShell 编程入门（关卡 39–41） | ✓ 阅读 + 本机练习 | ✓ 阅读 + 本机练习 |
| 正则 / Git 配置 / .gitattributes（关卡 42–44） | ✓ 阅读 + 测验 | ✓ 阅读 + 终端实验 |

**图例说明（关卡内标记）：**

- **🌐 在线可学**：阅读 + 测验即可掌握概念，不强制 Docker。
- **🐳 建议本地实验**：强烈建议在 localhost:8080 终端或宿主机 Docker 中实操。

详见各课「二、前置条件」中的学习模式一行。

---

## 快速开始

### 路径 A：只想先学概念（🌐）

1. 打开 GitHub Pages 站点首页，或阅读仓库 [docs/lessons-overview.md](./lessons-overview.md)。
2. 从 [关卡 00：安装与配置](./lesson-00-install-and-config.md) 或 [关卡 00b：终端基础](./lesson-00-terminal-basics.md) 读起。
3. 完成 [quiz](../site/quiz.html) 中与当前阶段对应的题目。
4. 需要查命令时用 [cheatsheet](../site/cheatsheet.html)；语法演练用 [playground](../site/playground.html)。
5. 准备动手时，切换到路径 B。

### 路径 B：完整实验环境（🐳）

1. 阅读 [快速开始](../site/quick-start.html)（`site/quick-start.html`）：安装 Docker、复制 `.env`、启动 compose。
2. 在仓库根目录执行：

   ```bash
   cp .env.example .env   # 首次
   docker compose up -d --build
   ```

3. 浏览器打开：
   - http://localhost:8081 — 教程站点
   - http://localhost:8081/workspace.html — 学习工作台（文档 + 终端分屏）
   - http://localhost:8080 — Web 终端
   - http://localhost:3000 — Gitea（默认账号见 `.env`）
4. Clone 演示仓库（组织 `playground` 下）：

   ```bash
   git clone http://localhost:3000/playground/playground-hello.git
   cd playground-hello
   ```

5. 按 [学习路径](./learning-path.md) 或 [关卡总览](./lessons-overview.md) 推荐顺序练习；计算机基础阶段 **I**（关卡 30–38）可与 Git 阶段并行。

### 停止环境

```bash
docker compose down
```

数据卷默认保留 Gitea 与终端 home；详见 [关卡 34：Docker 基础](./lesson-34-docker-basics.md)。

---

## 如何选择模式

| 你的情况 | 建议 |
|----------|------|
| 无 Docker / 学校机房限制 | 🌐 在线阅读 + quiz + playground |
| 准备面试、只复习命令与概念 | 🌐 为主 |
| 要学 Git push、PR、CI、Shell 实操 | 🐳 必开 Docker |
| 关卡标 🐳 且无「只读」说明 | 尽量本地实验 |

---

## 相关链接

- [快速开始（站点）](../site/quick-start.html)
- [关卡总览](./lessons-overview.md)
- [学习路径指南](./learning-path.md)
- [关卡 34：Docker 与本仓库 compose](./lesson-34-docker-basics.md)

---

## 常见问题

**在线站和 localhost:8081 内容一样吗？**  
站点结构一致；本地 8081 额外挂载最新 `docs/`，改文档后刷新即见。GitHub Pages 随仓库发布更新。

**能否只用 8080 终端、不用 Gitea？**  
Shell 类关卡（30–33、36–37）可以；Git 与 API 关卡（01+、35）需要 Gitea。

**GitHub Pages 上能跑 docker compose 吗？**  
不能。Compose 仅在你本机（或云主机）运行。
