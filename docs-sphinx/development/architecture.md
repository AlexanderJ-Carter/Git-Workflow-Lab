# 项目架构

本文档介绍 Git Workflow Lab 的技术架构和设计理念。

## 整体架构

```{mermaid}
graph TB
    subgraph "前端展示层"
        A[静态网站<br/>Nginx]
        B[Web 终端<br/>ttyd]
        C[AI 助手]
    end

    subgraph "后端服务层"
        D[Gitea<br/>Git 托管]
        E[PostgreSQL<br/>数据库]
    end

    subgraph "CI/CD 层"
        F[GitHub Actions]
        G[GitHub Pages]
        H[GHCR<br/>容器镜像]
    end

    subgraph "源代码层"
        I[课程文档<br/>Markdown]
        J[网站源码<br/>HTML/CSS/JS]
        K[构建脚本<br/>Python]
    end

    I --> A
    J --> A
    K --> A
    A --> G
    F --> G
    F --> H
    D --> E
    B -.-> D
    C -.-> D
```

## 技术栈

### 前端

| 技术 | 版本 | 用途 |
|------|------|------|
| HTML5 | - | 页面结构 |
| CSS3 | - | 样式设计 |
| Vanilla JS | ES6+ | 交互逻辑 |
| Noto Sans SC | - | 中文字体 |
| JetBrains Mono | - | 代码字体 |

**特点**：

- 无框架依赖，保持简洁
- 使用 CSS 变量实现主题切换
- 模块化 JavaScript 设计
- 响应式布局支持移动端

### 后端服务

| 服务 | 版本 | 用途 |
|------|------|------|
| Nginx | Alpine | 静态网站服务 |
| Gitea | Latest | Git 托管平台 |
| PostgreSQL | 16-alpine | Gitea 数据库 |
| ttyd | Alpine | Web 终端 |
| Docker Compose | v2 | 服务编排 |

### CI/CD

| 工具 | 用途 |
|------|------|
| GitHub Actions | 自动化工作流 |
| GitHub Pages | 静态网站托管 |
| GHCR | 容器镜像仓库 |
| Release Please | 自动版本发布 |
| Trivy | 安全扫描 |
| CodeQL | 代码分析 |

## 目录结构

```
.
├── .github/
│   ├── workflows/          # GitHub Actions 工作流
│   │   ├── pages.yml       # Pages 部署
│   │   ├── docker.yml      # 镜像构建
│   │   ├── release-please.yml
│   │   ├── code-quality.yml
│   │   └── security-scan.yml
│   └── ISSUE_TEMPLATE/     # Issue 模板
│
├── docs/                   # 课程文档源文件
│   ├── lesson-*.md         # 各课时 Markdown
│   ├── lessons-overview.md
│   └── learning-path.md
│
├── site/                   # 网站源码
│   ├── index.html          # 首页
│   ├── workspace.html      # 学习工作台
│   ├── playground.html     # 命令练习场
│   ├── quiz.html           # 技能测验
│   ├── ai-assistant.html   # AI 助手
│   └── assets/
│       ├── css/style.css
│       └── js/main.js
│
├── _site/                  # 构建输出（Pages）
│
├── docker/                 # Docker 相关
│   └── terminal/           # Web 终端镜像
│       ├── Dockerfile
│       └── welcome.sh
│
├── scripts/                # 工具脚本
│   ├── build-site.py       # 网站构建
│   ├── init-gitea.sh       # Gitea 初始化
│   └── fix-quotes.py       # 引号修复
│
├── docs-sphinx/            # Sphinx 文档
│   ├── conf.py
│   ├── index.md
│   └── getting-started/
│
├── docker-compose.yml      # 本地环境编排
├── Dockerfile              # Gitea 镜像
├── requirements-build.txt  # Python 构建依赖
└── docs-requirements.txt   # Sphinx 依赖
```

## 核心功能模块

### 1. 网站构建系统

**文件**: `scripts/build-site.py`

**功能**：

- Markdown 转 HTML
- 自动生成课程索引
- 链接重写（相对路径）
- 模板渲染

**输入**：`docs/*.md`, `site/`

**输出**：`_site/`

### 2. 学习进度管理

**文件**: `site/assets/js/main.js`

**存储**：浏览器 localStorage

**功能**：

- 记录课程完成状态
- 统计学习进度
- 支持跨页面同步

```javascript
// API 示例
GitWorkflowLab.LearningProgress.saveProgress('lesson-01', true);
GitWorkflowLab.LearningProgress.isCompleted('lesson-01'); // true
```

### 3. AI 问答助手

**文件**: `site/ai-assistant.html`

**功能**：

- 多 API 提供商支持（OpenAI, Anthropic）
- 课程上下文注入
- 对话历史管理
- Markdown 渲染

**安全措施**：

- API Key 仅存储在本地
- 输出内容经过 HTML 转义
- 使用 HTTPS 通信

### 4. 命令练习场

**文件**: `site/playground.html`

**功能**：

- 模拟 Git 命令执行
- 可视化工作区状态
- 支持常用命令

**实现**：

- 纯前端模拟，无后端依赖
- 命令解析与结果生成
- 状态管理（工作区/暂存区/仓库）

## 数据流

### 网站构建流程

```{mermaid}
sequenceDiagram
    participant D as docs/
    participant S as site/
    participant B as build-site.py
    participant O as _site/

    D->>B: 读取 Markdown
    S->>B: 读取模板
    B->>B: Markdown 转换
    B->>B: 链接重写
    B->>B: 模板渲染
    B->>O: 输出 HTML
```

### 本地学习环境

```{mermaid}
sequenceDiagram
    participant U as 用户浏览器
    participant N as Nginx :8081
    participant T as ttyd :8080
    participant G as Gitea :3000
    participant P as PostgreSQL :5432

    U->>N: 访问教程网站
    N->>U: 返回静态页面

    U->>T: 打开 Web 终端
    T->>U: 提供 Shell 环境

    U->>G: 访问 Git 平台
    G->>P: 读写数据
    G->>U: 返回 Git 服务
```

## 设计原则

### 1. 简洁优先

- 最小化依赖
- 使用标准 Web 技术
- 避免过度工程

### 2. 教学导向

- 清晰的代码注释
- 渐进式学习路径
- 丰富的示例

### 3. 可维护性

- 模块化设计
- 清晰的目录结构
- 完整的文档

### 4. 安全性

- 最小权限原则
- 输入验证
- 安全编码实践

## 扩展指南

### 添加新课程

1. 在 `docs/` 创建 `lesson-XX-topic.md`
2. 添加 YAML 元数据：

```markdown
---
title: 课程标题
stage: 2
description: 课程描述
---
```

3. 推送触发自动构建

### 添加新页面

1. 在 `site/` 创建 HTML 文件
2. 引入公共资源：

```html
<link rel="stylesheet" href="assets/css/style.css">
<script src="assets/js/main.js" defer></script>
```

3. 更新 `build-site.py`（如需构建时处理）

### 集成新工具

1. 更新 `requirements-build.txt` 或 `docs-requirements.txt`
2. 修改构建脚本
3. 更新 CI 工作流

## 性能优化

- **静态资源**：CSS/JS 文件使用版本号缓存
- **图片优化**：使用 WebP 格式，懒加载
- **代码分割**：按页面加载必要脚本
- **CDN 加速**：字体使用 Google Fonts CDN

## 监控与日志

- **GitHub Actions**：工作流执行记录
- **Docker 日志**：`docker-compose logs -f`
- **浏览器控制台**：前端错误追踪

## 未来规划

- [ ] 支持多语言（i18n）
- [ ] 添加单元测试
- [ ] 集成更多 Git 托管平台
- [ ] 实现学习数据分析
- [ ] 移动 App 支持
