# 关卡 12：多阶段流水线与敏感信息（Secrets）基础

**所属阶段**：CI/CD 进阶  
**本关关键词**：多 Job / 阶段（测试 → 构建 → 部署模拟）、环境变量、Secrets 基础、安全注意事项

---

## 一、本关目标

- 理解如何把 CI 流水线拆成多个阶段（Job），并设置依赖关系。
- 在不同阶段中传递构建产物的思路（可以用简单方式模拟）。
- 初步了解在 CI 中使用环境变量与 Secrets 的正确方式，避免把敏感信息写进仓库。

---

## 二、前置条件

- 已完成 **关卡 10** 和 **关卡 11**，能编写、调试简单的 Workflow。
- 对项目结构有基本认识（本关可以用非常简单的「伪项目」来模拟）。

---

## 三、边看边做：设计一个三阶段流水线

我们设计一个逻辑上有三步的流程：

1. **test**：快速检查（例如跑一个简单脚本）。
2. **build**：模拟构建步骤（生成某个文件作为「构建产物」）。
3. **deploy**：模拟部署步骤（打印出要部署的版本信息），仅在前两步都成功时执行。

### 步骤 1：新建 / 修改 Workflow 文件

在 `.gitea/workflows/` 下新建或编辑一个 `pipeline.yml`：

```yaml
name: Demo Pipeline

on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: docker
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run tests
        run: |
          echo "Running tests..."
          # 在这里可以替换为真正的测试命令
          echo "All tests passed."

  build:
    runs-on: docker
    needs: test
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Build artifact
        run: |
          echo "Build at $(date)" > build-artifact.txt
          echo "VERSION=1.0.$GITHUB_RUN_NUMBER" >> build-artifact.txt
          echo "Build artifact created:"
          cat build-artifact.txt

  deploy:
    runs-on: docker
    needs: build
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Simulate deploy
        env:
          ENVIRONMENT: "staging"
        run: |
          echo "Deploying to $ENVIRONMENT environment..."
          echo "Here we would upload build-artifact.txt or Docker image."
```

说明：

- `test`、`build`、`deploy` 是三个 Job。
- `build.needs: test` 表示只有在 `test` 成功后才执行 `build`。
- `deploy.needs: build` 表示只有在 `build` 成功后才执行 `deploy`。
- 这里用一个简单的 `build-artifact.txt` 来模拟构建产物。

提交并推送：

```bash
git add .gitea/workflows/pipeline.yml
git commit -m "ci: add demo multi-stage pipeline"
git push origin main
```

然后在 Gitea Web 上观察流水线执行顺序。

---

## 四、引入环境变量和 Secrets 概念

在真实项目中，部署阶段往往需要一些敏感信息，比如：

- 云服务访问密钥
- 数据库连接密码
- Webhook 地址 / Token

这些都 **不能** 直接写死在仓库里的 YAML 或代码中。

### 步骤 2：示意性的 Secrets 使用方式（概念）

不同平台有不同的 Secrets 配置方式，典型思路是：

1. 在 CI 平台的 Web 后台，为仓库或项目配置名为 `DEPLOY_TOKEN` 的 Secret。
2. 在 Workflow 中，以环境变量方式引用它，例如：

   ```yaml
   deploy:
     runs-on: docker
     needs: build
     steps:
       - name: Simulate secure deploy
         env:
           DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
         run: |
           echo "Using a secret token (not printed here) to authenticate deploy."
           # 实际命令中使用 $DEPLOY_TOKEN 调用远程 API
   ```

3. 日志中不会直接显示 Secret 的明文，即使脚本 echo 出来也会被平台屏蔽（视平台实现而定）。

> 具体的 `${{ secrets.* }}` 语法以平台（Gitea / GitHub / GitLab）实际文档为准，本关主要强调「不要把密钥写进仓库，应该通过 Secrets / 环境变量注入」这一原则。

---

## 五、安全与许可证的基本注意事项（概览）

虽然本项目是一个本地练习平台，但在设计你的仓库和 CI 时，仍然建议注意：

- **不要把真实的生产访问密钥放入练习仓库**，即便是私有仓库也不安全。
- 模拟练习时，可以使用假 Token（例如 `DEMO_TOKEN_xxx`），或者使用最低权限的测试账号。
- 使用开源依赖时，留意它们的许可证（MIT / Apache-2.0 / GPL 等），在你后续打算公开发布时：
  - 为你的项目选择一个合适的 LICENSE（例如 MIT 对「教学类仓库」非常友好）。
  - 在 README 中简单说明使用了哪些主要开源组件。

本项目本身也建议放一个开源许可证文件（如 `LICENSE`，MIT 等），方便他人 fork / 二次开发。

---

## 六、练习题

### 练习 1：让部署 Job 只在打 Tag 时运行

1. 修改 Workflow 的 `on` 配置，让：
   - `test` / `build` 仍在 push 到 `main` 时运行；
   - `deploy` 只在打 Tag（例如 `v1.0.0`）时运行。
2. 思考：在真实项目中，你会如何设计「普通 push」与「发布版本」的流水线区别？

### 练习 2：为你的学习平台仓库添加 LICENSE

1. 在仓库根目录新建 `LICENSE` 文件，选择一种开源许可证（比如 MIT）。
2. 在 README 顶部或底部加入一段「许可证」说明。
3. 思考：如果别人 fork 你的仓库并改了一些内容再发布，会有哪些约束 / 权利？

---

## 七、参考答案（仅供对照）

### 练习 1 参考思路

一种可能的写法（思路示例）：

```yaml
on:
  push:
    branches:
      - main
  push:
    tags:
      - "v*.*.*"
```

再结合条件判断（不同平台语法略有差异），让 `deploy` Job 只在 Tag 情况下运行，例如：

```yaml
  deploy:
    if: startsWith(github.ref, 'refs/tags/')
    ...
```

> 具体条件表达式以使用的平台（Gitea / GitHub 等）的文档为准。

### 练习 2 参考思路

MIT 许可证示例（节选）：

```text
MIT License

Copyright (c) 2026 <Your Name>

Permission is hereby granted, free of charge, to any person obtaining a copy
...
```

在 README 中可以简单写：

```markdown
## 许可证

本项目使用 MIT License，详见 `LICENSE` 文件。
```

这样别人就清楚你的代码可以如何被使用、修改和分发。

