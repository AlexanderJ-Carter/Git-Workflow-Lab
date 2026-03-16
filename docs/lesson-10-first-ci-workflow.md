# 关卡 10：为仓库添加第一个 CI 工作流（Gitea Actions 示例）

**所属阶段**：CI/CD 基础  
**本关关键词**：Gitea Actions、工作流（workflow）、Job、Step、触发条件（on: push）

---

## 一、本关目标

- 了解什么是 CI 工作流（Workflow），以及 Job / Step 的基本概念。
- 在本地 Gitea 中为某个仓库添加一个最简单的 CI Workflow。
- 每次 push 时，自动在 CI 中执行一个脚本，并在 Web 上看到运行结果。

学完这一关，你就完成了从「只会写 commit」到「能给项目加上自动检查」的第一步。

> 说明：本关以 Gitea Actions 为例，概念上与 GitHub Actions / GitLab CI 非常相似，后续迁移很容易。

---

## 二、前置条件

- 已完成基础 Git 相关关卡，能正常推送代码到 Gitea 仓库。
- 你的 Gitea 版本已开启 Actions 功能，并且有可用的 Runner。  
  - 如果暂时没有 Actions 环境，也可以先当作「YAML 语法与概念」学习，等之后配置好 Runner 再实际运行。

> 如果你当前的 Gitea 未开启 Actions，可以先只完成本关的「配置文件编写」部分，后续再补充 Runner 与运行效果。

---

## 三、核心概念速览

- **Workflow（工作流）**：一份 YAML 配置，定义「在什么条件下，执行哪些 Job」。
- **Job**：一次在 Runner 上执行的任务，可以包含多个步骤（Step）。
- **Step**：在 Job 中具体执行的命令或 Action。
- **触发条件（on）**：比如 `on: push` 表示每次仓库有 push 时触发。

---

## 四、边看边做：添加第一个 Workflow

> 建议：选择你在本实验中使用的某个仓库（例如 `playground-hello`）作为练习对象。

### 步骤 1：创建工作流目录

在本地仓库根目录下创建 Actions 配置目录（以 Gitea Actions 为例）：

```bash
mkdir -p .gitea/workflows
```

> 若你参考的是 GitHub Actions，则目录为 `.github/workflows`，概念类似。

### 步骤 2：新建一个最简单的 Workflow 文件

在 `.gitea/workflows/` 目录中新建 `hello-ci.yml`（文件名随意），内容示例：

```yaml
name: Hello CI

on:
  push:
    branches:
      - main

jobs:
  say-hello:
    runs-on: docker

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Print greeting
        run: |
          echo "Hello from CI!"
          echo "Repository: $GITHUB_REPOSITORY"
          echo "Commit: $GITHUB_SHA"
```

说明：

- `on.push.branches: main`：每次向 `main` 分支 push 时触发。
- `jobs.say-hello`：定义了一个名为 `say-hello` 的 Job。
- `runs-on: docker`：示例使用 Docker Runner，根据你的 Runner 实际配置调整。
- 第一个 Step 使用 `actions/checkout@v4` 检出代码。
- 第二个 Step 直接运行一段 Shell 脚本，打印一些信息。

### 步骤 3：提交并推送 Workflow

在仓库根目录执行：

```bash
git add .gitea/workflows/hello-ci.yml
git commit -m "ci: add first hello workflow"
git push origin main
```

---

## 五、在 Gitea Web 上查看流水线

> 前提是你的 Gitea 已配置 Actions / Runner，并且当前仓库已启用 Actions。

1. 打开 Gitea 上对应仓库的页面。
2. 找到与 Actions / CI / Workflows 相关的菜单（根据版本 UI 可能略有不同）。
3. 你应该能看到一条因刚才 push 触发的 Workflow 运行记录。
4. 点进去查看详情：
   - 确认 `say-hello` Job 运行成功。
   - 在日志中找到 `Print greeting` 步骤输出的那几行 `echo` 内容。

如果 Runner 尚未配置成功：

- 你可能会看到 Workflow 被创建但处于排队 / 未运行状态。
- 这时可以先跳到练习题部分，把更多 Workflow 场景设计好，等待 Runner 搭建完成后统一测试。

---

## 六、练习题

> 即使暂时没有 Runner，你也可以先把 YAML 写好，模拟思考与本地脚本对应。

### 练习 1：只在特定目录变更时触发

目标：只有当 `src/` 目录下有文件变更时才触发 CI。

思考并尝试修改 `on` 部分的配置，让 Workflow 行为变成：

- `main` 分支上有 push；
- 且变更文件路径匹配 `src/**` 时，才会执行 CI。

### 练习 2：添加一个简单的「测试」步骤

假设你的项目中有一个脚本 `scripts/test.sh`，你希望每次 push 到 `main` 都自动执行它。

在当前 Workflow 的 `steps` 里：

1. 添加一个新的 Step，命名为 `Run tests`。
2. 在 Step 中执行 `bash scripts/test.sh`。
3. 让整个 Workflow 在脚本返回非 0 时标记为失败。

---

## 七、参考答案（仅供对照）

### 练习 1 参考写法

```yaml
on:
  push:
    branches:
      - main
    paths:
      - "src/**"
```

说明：

- `paths` 可以用来限制只有当特定路径下有变更时才触发 Workflow。

### 练习 2 参考写法

在原有 `steps` 后面追加：

```yaml
      - name: Run tests
        run: |
          bash scripts/test.sh
```

只要 `scripts/test.sh` 的最后返回值为非 0（例如 `exit 1`），整个 Job 就会被标记为失败。

> 实际项目中，你可以用同样的方式运行单元测试、Lint、构建脚本等。

