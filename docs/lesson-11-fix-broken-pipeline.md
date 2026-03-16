# 关卡 11：修复一个失败的 CI 流水线

**所属阶段**：CI/CD 基础  
**本关关键词**：流水线失败、构建日志、排查错误、修改代码或配置让 CI 变绿

---

## 一、本关目标

- 学会阅读 CI 流水线的日志，定位失败原因。
- 能根据错误信息，判断是代码问题还是 CI 配置问题。
- 修改相应的代码或 Workflow 配置，让原本失败的流水线通过。

这关的核心不是「写出多高级的 YAML」，而是培养一种习惯：**先看日志，再动手改**。

---

## 二、前置条件

- 已完成 **关卡 10：为仓库添加第一个 CI 工作流**，并能在 push 后看到 Workflow 运行结果。
- 当前实验仓库中已有一个简单 Workflow（例如 `hello-ci.yml`）。

---

## 三、边看边做：故意制造一个失败的流水线

### 步骤 1：在 Workflow 中加入一个会失败的命令

在上一关的 `hello-ci.yml` 基础上，故意加入一个不存在的命令，例如：

```yaml
      - name: This will fail
        run: |
          echo "Step before failure"
          non_existing_command_123
          echo "Step after failure"
```

更新后的 Workflow 大致结构如下（仅示意关键部分）：

```yaml
jobs:
  say-hello:
    runs-on: docker
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Print greeting
        run: echo "Hello from CI!"

      - name: This will fail
        run: |
          echo "Step before failure"
          non_existing_command_123
          echo "Step after failure"
```

保存文件后：

```bash
git add .gitea/workflows/hello-ci.yml
git commit -m "ci: introduce an intentional failure"
git push origin main
```

### 步骤 2：在 Web 上观察失败的流水线

1. 打开 Gitea 上对应仓库的 Actions / Workflows 页面。
2. 找到刚刚触发的 Workflow 运行记录。
3. 进入详情页面，查看 Job / Step 列表：
   - `Print greeting` 应该是绿色通过。
   - `This will fail` 应该显示红色失败。

点击失败的那个 Step，查看控制台输出，应该有类似：

```text
Step before failure
/bin/sh: 1: non_existing_command_123: not found
Error: Process completed with exit code 127.
```

这就是我们故意制造的错误。

---

## 四、修复失败：根据日志改配置

### 步骤 3：改成一个合法但返回非 0 的脚本（代码问题示例）

我们先模拟一种「代码里写了错误逻辑导致失败」的场景。

修改 `This will fail` Step 为：

```yaml
      - name: This will fail
        run: |
          echo "Running tests..."
          exit 1
```

含义：

- 命令本身是合法的，只是故意返回退出码 `1`，表示失败。

提交并推送：

```bash
git add .gitea/workflows/hello-ci.yml
git commit -m "ci: simulate failing tests with exit 1"
git push origin main
```

再次观察 Workflow：

- 你会在日志中看到 `Running tests...`。
- Job 最后仍然是失败状态。

### 步骤 4：修复「失败的测试」

现在假设我们已经修复了代码中的 Bug，测试应该通过，于是只需把退出码改为 0 或删除 `exit 1`：

```yaml
      - name: This will fail
        run: |
          echo "Running tests..."
          echo "All tests passed!"
          # 不再 exit 1
```

再提交并推送：

```bash
git add .gitea/workflows/hello-ci.yml
git commit -m "ci: fix failing tests step"
git push origin main
```

观察新一轮 Workflow 运行记录，确认：

- 所有 Step 为绿色。
- 整个 Workflow 状态为成功。

---

## 五、如何确认自己学会了「看日志修流水线」

- 你能通过 Web 界面的 Workflow 详情：
  - 找到哪个 Job / Step 失败。
  - 打开对应日志，清晰看到错误信息。
- 你可以区分：
  - 命令本身不存在（如 `not found`）→ 大概率是 CI 配置 / 环境问题。
  - 命令执行后返回非 0（如 `exit 1` 或测试失败信息）→ 大概率是代码或测试问题。
- 你能在本地修改相应的 Workflow 或代码，让原本失败的流水线重新变绿。

---

## 六、练习题

### 练习 1：模拟「依赖没安装」导致的失败

1. 在 Workflow 中新增一个 Step：

   ```yaml
   - name: Run linter
     run: |
       eslint src/**/*.ts
   ```

2. 但你并没有在 CI 环境中安装 `eslint`。
3. 观察流水线失败时的错误信息。
4. 思考并尝试修复：
   - 要么在 Workflow 中增加安装步骤；
   - 要么改成使用本项目中已有的脚本，如 `npm run lint`。

### 练习 2：只在 PR 时运行部分检查

1. 修改 Workflow 的 `on` 配置，让某个 Job 只在「pull request 打开 / 更新」时运行。
2. 思考：在真实项目中，你会在 push 时跑什么，在 PR 时再额外跑什么？

---

## 七、参考答案（仅供对照）

### 练习 1 参考思路

错误状态下日志可能类似：

```text
eslint: command not found
Error: Process completed with exit code 127.
```

一种修复方式是在 Step 之前先安装依赖，例如：

```yaml
      - name: Install deps
        run: |
          npm ci

      - name: Run linter
        run: |
          npx eslint src/**/*.ts
```

> 使用 `npx` 可以执行本项目中的本地依赖，而不要求全局安装。

### 练习 2 参考写法

```yaml
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
```

或者你可以为不同 Job 设置不同的触发条件（进阶用法），例如：

- push 时只跑快速检查；
- PR 时跑完整测试和构建。

