# 快速开始

本指南帮助你在 5 分钟内开始使用 Git Workflow Lab。

## 前提条件

确保已完成 {doc}`installation`。

## 第一步：访问学习工作台

1. 打开浏览器，访问 http://localhost:8081
2. 点击"课程中心"或"学习路径"
3. 选择感兴趣的课程开始学习

## 第二步：使用 Web 终端练习

### 启动终端

1. 访问 http://localhost:8080
2. 或在工作台页面右侧找到嵌入的终端

### 基础命令练习

```bash
# 配置 Git 用户信息
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 查看配置
git config --list

# 创建练习仓库
mkdir my-first-repo
cd my-first-repo
git init

# 创建文件并提交
echo "# My First Repo" > README.md
git add README.md
git commit -m "Initial commit"

# 查看提交历史
git log --oneline
```

## 第三步：使用 Gitea 进行协作练习

### 登录 Gitea

1. 访问 http://localhost:3000
2. 使用 `.env` 中配置的管理员账号登录
3. 默认用户名：`playground`

### 创建仓库

1. 点击右上角 "+" → "新建仓库"
2. 填写仓库名称（如：`practice-repo`）
3. 选择"初始化仓库"
4. 点击"创建仓库"

### 克隆并推送

```bash
# 在 Web 终端中
git clone http://localhost:3000/playground/practice-repo.git
cd practice-repo

# 创建新分支
git checkout -b feature/hello

# 添加文件
echo "Hello Git!" > hello.txt
git add hello.txt
git commit -m "Add hello.txt"

# 推送到远程
git push origin feature/hello
```

### 创建 Pull Request

1. 返回 Gitea 网页
2. 点击"合并请求" → "新的合并请求"
3. 选择 `feature/hello` → `main`
4. 填写标题和描述
5. 创建并合并 PR

## 学习路径建议

```{mermaid}
graph TD
    A[基础操作] --> B[分支管理]
    B --> C[远程协作]
    C --> D[冲突解决]
    D --> E[高级操作]
    E --> F[CI/CD]

    style A fill:#10b981
    style B fill:#6366f1
    style C fill:#8b5cf6
    style D fill:#f59e0b
    style E fill:#ec4899
    style F fill:#ef4444
```

### 阶段一：基础操作（1-2 天）

- {doc}`../lessons/basic`
- 掌握 `init`, `add`, `commit`, `status`, `log`

### 阶段二：分支管理（2-3 天）

- {doc}`../lessons/branching`
- 学习 `branch`, `checkout`, `merge`, `rebase`

### 阶段三：远程协作（3-4 天）

- {doc}`../lessons/collaboration`
- 练习 `clone`, `push`, `pull`, PR 工作流

### 阶段四：高级操作（4-5 天）

- {doc}`../lessons/advanced`
- 掌握 `reset`, `reflog`, `cherry-pick`, `stash`

### 阶段五：CI/CD（2-3 天）

- 学习 GitHub Actions 基础
- 实践自动化工作流

## 常用功能

### AI 问答助手

访问 `ai-assistant.html` 使用 AI 辅助学习：

- 需要 API Key（OpenAI 或 Anthropic）
- 可选择课程上下文
- 支持快捷提问

### 命令练习场

访问 `playground.html` 进行命令模拟：

- 无需真实 Git 环境
- 可视化工作区状态
- 支持常见 Git 命令

### 技能测验

访问 `quiz.html` 检验学习成果：

- 每课一测
- 即时反馈
- 错题回顾

## 下一步

- {doc}`../lessons/index` - 浏览完整课程
- {doc}`../environment/gitea-usage` - 深入了解 Gitea 功能
- {doc}`../appendix/cheatsheet` - Git 命令速查表
