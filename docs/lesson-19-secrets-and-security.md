# 关卡 19：Secrets 与安全实践

**所属阶段**：安全与规范
**难度**：🟡 进阶
**预估时间**：35 分钟
**本关命令关键词**：`git secret`、`.gitignore`、`git filter-branch`、GitHub/Gitea Secrets

---

> 💡 **学习提示**：左边打开本文件，右边同时打开浏览器 + 终端，按照步骤逐条执行。完成每步后记得验证结果。

---

## 一、本关目标

- [ ] **目标 1**：理解为什么不能将敏感信息提交到 Git 仓库
- [ ] **目标 2**：学会使用 `.gitignore` 防止敏感文件被跟踪
- [ ] **目标 3**：掌握从 Git 历史中清除敏感信息的方法
- [ ] **目标 4**：学会在 CI/CD 中安全使用 Secrets

**前置知识：** 学完这一关，你将能够在项目中正确管理敏感信息，避免密码和密钥泄露。

---

## 二、前置条件

在开始本关之前，请确保：

- [ ] 已完成关卡 12（多阶段流水线与 Secrets）
- [ ] 本地实验环境已启动（`docker-compose up -d`）
- [ ] 可访问 http://localhost:3000 (Gitea) 和 http://localhost:8080 (终端)

---

## 三、边看边做：具体步骤

### 步骤 1：创建敏感文件（错误示范）

> **为什么要做这个步骤：** 我们先模拟一个常见的错误场景，理解为什么敏感信息不能提交。

```bash
# 进入测试仓库
cd ~/playground-hello

# 创建一个包含敏感信息的文件（错误做法）
echo 'DATABASE_URL=postgres://user:password123@localhost/mydb' > .env
echo 'API_KEY=sk-1234567890abcdef' >> .env
echo 'SECRET_KEY=my-super-secret-key' >> .env
```

---

### 步骤 2：检查 Git 状态

```bash
# 查看工作区状态
git status
```

**输出解读：**
```
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .env        # 这个文件会被跟踪！
```

---

### 步骤 3：创建 .gitignore 防止跟踪

```bash
# 创建 .gitignore 文件
cat > .gitignore << 'EOF'
# 环境变量文件
.env
.env.local
.env.*.local

# 敏感配置文件
config/secrets.yml
credentials.json
*.pem
*.key

# 日志文件
*.log

# 依赖目录
node_modules/
__pycache__/
EOF
```

---

### 步骤 4：验证 .gitignore 生效

```bash
# 再次查看状态
git status
```

**预期输出：**
```
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .gitignore   # 只有 .gitignore，没有 .env
```

**验证：**
```bash
# 检查 .env 是否被忽略
git check-ignore -v .env
# 输出：.gitignore:1:.env
```

---

### 步骤 5：提交 .gitignore

```bash
# 添加并提交 .gitignore
git add .gitignore
git commit -m "chore: 添加 .gitignore 忽略敏感文件"
```

---

### 步骤 6：模拟敏感信息泄露（错误场景）

> **注意：** 这是错误做法的演示，实际项目中绝对不要这样做！

```bash
# 错误：直接添加 .env 文件
git add .env
git commit -m "chore: 添加环境变量"

# 检查提交
git log --oneline -1
```

---

### 步骤 7：从 Git 历史中清除敏感信息

> **为什么要做这个步骤：** 即使提交了敏感信息，我们也可以从历史中清除。

```bash
# 方法 1：使用 git filter-branch（简单但慢）
# 从所有提交中删除 .env 文件
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# 或者使用更现代的 git-filter-repo（推荐）
# pip install git-filter-repo
# git filter-repo --path .env --invert-paths
```

**清理本地引用：**
```bash
# 删除备份引用
git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin

# 清理 reflog
git reflog expire --expire=now --all

# 垃圾回收
git gc --prune=now --aggressive
```

---

### 步骤 8：强制推送清除后的代码

```bash
# 强制推送（警告：这会覆盖远程历史！）
git push origin main --force
```

**⚠️ 警告：** `--force` 会覆盖远程仓库的历史，团队成员需要重新 clone。

---

### 步骤 9：配置 Git 自动忽略敏感文件

```bash
# 全局忽略敏感文件（推荐）
git config --global core.excludesFile ~/.gitignore_global

# 创建全局 gitignore
cat > ~/.gitignore_global << 'EOF'
# 操作系统文件
.DS_Store
Thumbs.db

# 编辑器文件
*.swp
*.swo
*~

# 敏感文件
.env
.env.*
*.pem
*.key
credentials.json
EOF
```

---

### 步骤 10：在 CI/CD 中安全使用 Secrets

> **为什么要做这个步骤：** CI/CD 流程中经常需要使用 API 密钥等敏感信息。

**在 Gitea Actions 中使用 Secrets：**

1. 在仓库设置中添加 Secrets
2. 在 workflow 中引用 Secrets

```yaml
# .github/workflows/ci.yml 示例
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: 使用 Secret
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: |
          echo "API Key is configured"
          # 运行测试或部署脚本
```

**⚠️ 注意事项：**
- Secret 在日志中会被自动掩码为 `***`
- 不要在命令中直接打印 Secret
- 使用环境变量传递 Secret

---

## 四、如何确认自己做对了

运行以下命令验证：

```bash
# 检查 .gitignore 是否生效
git check-ignore -v .env
git check-ignore -v .env.local

# 检查历史中是否还有敏感文件
git log --all --oneline -- .env
# 应该输出为空或只有 "chore: 添加 .gitignore" 相关提交

# 检查全局 gitignore
git config --global core.excludesFile
```

- [ ] ✓ `git check-ignore .env` 返回 .gitignore 路径
- [ ] ✓ Git 历史中没有 `.env` 文件
- [ ] ✓ CI/CD 中的 Secrets 配置正确

---

## 五、常见错误与排查

### ❌ 情况 1：忘记添加 .gitignore 就提交了敏感文件

**解决方法：**
```bash
# 1. 立即从暂存区移除
git rm --cached .env

# 2. 添加到 .gitignore
echo ".env" >> .gitignore

# 3. 提交更改
git add .gitignore
git commit -m "fix: 移除误提交的敏感文件并添加 .gitignore"

# 4. 如果已经推送到远程，使用 filter-branch 清除历史
```

---

### ❌ 情况 2：团队成员本地有敏感文件

**解决方法：**
```bash
# 通知团队成员执行以下操作
git pull
git rm --cached .env
# 他们的本地 .env 文件不会被删除，只是不再被 Git 跟踪
```

---

### ❌ 情况 3：Secrets 在 CI/CD 日志中泄露

**预防措施：**
- 使用环境变量而不是命令行参数
- 避免在 `echo` 或 `print` 中输出 Secret
- 使用官方的 Secret 管理工具

---

## 六、知识扩展（可选）

### 敏感信息管理最佳实践

1. **永不提交**：密码、API 密钥、私钥等
2. **使用 Secrets**：CI/CD 平台的 Secrets 功能
3. **环境变量**：运行时注入，不要硬编码
4. **密钥管理服务**：HashiCorp Vault、AWS Secrets Manager 等
5. **定期轮换**：定期更换密码和密钥

### 常见敏感信息类型

| 类型 | 示例 | 存储位置 |
|------|------|----------|
| 数据库密码 | `postgres://user:pass@host` | 环境变量 |
| API 密钥 | `sk-xxx`、`api_key=xxx` | Secrets |
| 私钥文件 | `*.pem`、`*.key` | 安全存储 |
| 认证令牌 | `Bearer xxx` | 环境变量 |

---

## 七、思考题

1. **问题 1：** 如果有人不小心将 AWS 密钥提交到公开仓库，应该怎么办？
2. **问题 2：** 为什么 `git filter-branch` 需要使用 `--force` 推送？

---

## 八、扩展练习

- [ ] **练习 1：** 创建一个完整的 `.gitignore` 模板，覆盖常见语言和框架
- [ ] **练习 2：** 在 Gitea Actions 中配置 Secrets 并在 workflow 中使用
- [ ] **练习 3：** 研究 `git-secrets` 工具如何防止提交敏感信息

---

## 九、下一步

| 上一关 | 下一关 |
|--------|--------|
| [关卡 18：提交签名与标签签名](./lesson-18-commit-and-tag-signing.md) | [课程总览](./lessons-overview.md) |
