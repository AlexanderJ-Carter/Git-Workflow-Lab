# 关卡 15：Git 钩子与自动化

**所属阶段**：进阶操作
**本关关键词**：Git Hooks、pre-commit、pre-push、Husky、commitlint

---

## 一、本关目标

- 理解 Git 钩子的工作原理。
- 学会配置常用的客户端钩子。
- 掌握 Husky 等现代钩子管理工具。
- 了解 commitlint 提交信息规范。

学完这一关，你就能在提交、推送代码时自动执行检查，提高代码质量。

---

## 二、前置条件

- 已完成关卡 01-03（Git 基础操作）。
- 了解基本的 Shell 脚本语法。
- 有 Node.js 环境（用于 Husky 演示）。

---

## 三、边看边做前先理解的核心概念

### 什么是 Git 钩子？

Git 钩子是在特定事件发生时自动执行的脚本。例如：
- 提交前检查代码格式
- 推送前运行测试
- 提交后自动部署

### 钩子位置

```
.git/
└── hooks/
    ├── pre-commit.sample     # 提交前（示例）
    ├── pre-push.sample       # 推送前（示例）
    ├── commit-msg.sample     # 提交信息验证（示例）
    └── ...
```

### 客户端钩子 vs 服务端钩子

| 类型   | 触发时机   | 常见用途               |
| ------ | ---------- | ---------------------- |
| 客户端 | 本地操作   | 代码检查、格式化、测试 |
| 服务端 | 推送到远程 | CI/CD、权限验证        |

### 常用客户端钩子

| 钩子                 | 触发时机          | 用途             |
| -------------------- | ----------------- | ---------------- |
| `pre-commit`         | `git commit` 之前 | 代码检查、格式化 |
| `prepare-commit-msg` | 生成提交信息之前  | 自动生成消息模板 |
| `commit-msg`         | 编辑提交信息之后  | 验证提交信息格式 |
| `pre-push`           | `git push` 之前   | 运行测试         |

---

## 四、边看边做：原生 Git 钩子

### 步骤 1：查看现有钩子

```bash
cd playground-hello

# 查看钩子目录
ls -la .git/hooks/

# 你会看到很多 .sample 文件
```

### 步骤 2：创建简单的 pre-commit 钩子

```bash
# 创建钩子文件
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

echo "🔍 Running pre-commit checks..."

# 检查是否有 console.log
if git diff --cached --name-only | xargs grep -l "console.log" 2>/dev/null; then
    echo "❌ Error: Found console.log in staged files!"
    echo "Please remove them before committing."
    exit 1
fi

# 检查是否有 TODO
if git diff --cached --name-only | xargs grep -l "TODO" 2>/dev/null; then
    echo "⚠️  Warning: Found TODO comments"
fi

echo "✅ Pre-commit checks passed!"
exit 0
EOF

# 添加执行权限
chmod +x .git/hooks/pre-commit
```

### 步骤 3：测试 pre-commit 钩子

```bash
# 创建一个包含 console.log 的文件
echo "console.log('debug');" > debug.js
git add debug.js

# 尝试提交
git commit -m "add debug file"
# 应该会被阻止！

# 移除 console.log
echo "// clean code" > debug.js
git add debug.js
git commit -m "add clean file"
# 现在应该成功
```

### 步骤 4：创建 commit-msg 钩子

验证提交信息格式：

```bash
cat > .git/hooks/commit-msg << 'EOF'
#!/bin/bash

# 读取提交信息
commit_msg=$(cat "$1")

# 检查格式：必须以 feat/fix/docs 等开头
pattern="^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{1,}"

if ! echo "$commit_msg" | grep -qE "$pattern"; then
    echo "❌ Invalid commit message format!"
    echo ""
    echo "Format: <type>(<scope>): <subject>"
    echo ""
    echo "Types: feat, fix, docs, style, refactor, test, chore"
    echo ""
    echo "Examples:"
    echo "  feat: add user login"
    echo "  fix(auth): resolve timeout issue"
    echo "  docs: update README"
    exit 1
fi

exit 0
EOF

chmod +x .git/hooks/commit-msg
```

### 步骤 5：测试 commit-msg 钩子

```bash
# 错误格式
git commit -m "added a feature"
# 应该被拒绝

# 正确格式
git commit -m "feat: add new feature"
# 应该成功
```

---

## 五、使用 Husky 管理钩子（推荐）

原生钩子的问题：
- `.git/hooks/` 不被 Git 跟踪，无法共享
- 团队成员需要手动配置

Husky 解决了这些问题：
- 钩子配置写入 `package.json` 或独立文件
- `npm install` 自动设置钩子

### 步骤 6：初始化 npm 项目

```bash
cd playground-hello
npm init -y
```

### 步骤 7：安装 Husky

```bash
npm install husky --save-dev

# 初始化 Husky
npx husky init
```

这会创建 `.husky/` 目录。

### 步骤 8：配置 pre-commit 钩子

```bash
# 编辑 .husky/pre-commit
echo "npm test" > .husky/pre-commit
```

### 步骤 9：添加 commitlint

```bash
# 安装 commitlint
npm install @commitlint/cli @commitlint/config-conventional --save-dev

# 创建配置文件
echo "export default { extends: ['@commitlint/config-conventional'] }" > commitlint.config.js

# 配置 Husky 使用 commitlint
echo "npx --no -- commitlint --edit \$1" > .husky/commit-msg
```

### 步骤 10：添加 lint-staged

只检查暂存区的文件，提高效率：

```bash
npm install lint-staged --save-dev
```

在 `package.json` 中添加：

```json
{
  "scripts": {
    "prepare": "husky"
  },
  "lint-staged": {
    "*.js": ["eslint --fix", "prettier --write"],
    "*.md": ["prettier --write"]
  }
}
```

更新 `.husky/pre-commit`：

```bash
echo "npx lint-staged" > .husky/pre-commit
```

---

## 六、常用钩子配置示例

### 完整的 package.json 配置

```json
{
  "name": "my-project",
  "scripts": {
    "test": "jest",
    "lint": "eslint .",
    "format": "prettier --write .",
    "prepare": "husky"
  },
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md}": [
      "prettier --write"
    ]
  },
  "devDependencies": {
    "@commitlint/cli": "^18.0.0",
    "@commitlint/config-conventional": "^18.0.0",
    "husky": "^9.0.0",
    "lint-staged": "^15.0.0"
  }
}
```

### 跳过钩子（谨慎使用）

```bash
# 跳过 pre-commit
git commit --no-verify -m "feat: emergency fix"

# 或者使用 -n
git commit -n -m "feat: emergency fix"
```

---

## 七、服务端钩子简介

服务端钩子在远程仓库上执行：

| 钩子           | 触发时机   | 用途           |
| -------------- | ---------- | -------------- |
| `pre-receive`  | 推送接收前 | 验证推送内容   |
| `update`       | 更新引用前 | 细粒度推送控制 |
| `post-receive` | 推送接收后 | 部署、通知     |

在 Gitea 中可以配置：
1. 进入仓库设置
2. 找到 "Git Hooks"
3. 添加钩子脚本

---

## 八、如何确认自己做对了

- pre-commit 钩子能在提交前执行检查。
- commit-msg 钩子能验证提交信息格式。
- 使用 `--no-verify` 能跳过钩子。
- Husky 配置的钩子能被 Git 跟踪。

---

## 九、练习题

### 练习 1：创建代码检查钩子

1. 创建 pre-commit 钩子，检查：
   - 是否有 debugger 语句
   - 是否有 .only 测试
2. 测试钩子是否生效。

### 练习 2：配置 Husky + commitlint

1. 初始化 npm 项目。
2. 安装 Husky 和 commitlint。
3. 配置约定式提交验证。
4. 测试错误和正确的提交格式。

### 练习 3：添加 lint-staged

1. 安装 lint-staged。
2. 配置只检查暂存文件。
3. 提交部分文件，观察行为。

---

## 十、参考答案（仅供对照）

### 练习 1 参考思路

```bash
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# 检查 debugger
if git diff --cached --name-only | xargs grep -l "debugger" 2>/dev/null; then
    echo "❌ Found debugger statements!"
    exit 1
fi

# 检查 .only
if git diff --cached --name-only | xargs grep -l "\.only" 2>/dev/null; then
    echo "❌ Found .only in tests!"
    exit 1
fi

exit 0
EOF
chmod +x .git/hooks/pre-commit
```

### 练习 2 参考思路

```bash
# 安装
npm init -y
npm install husky @commitlint/cli @commitlint/config-conventional --save-dev

# 初始化 Husky
npx husky init

# 配置 commitlint
echo "export default { extends: ['@commitlint/config-conventional'] }" > commitlint.config.js
echo "npx --no -- commitlint --edit \$1" > .husky/commit-msg

# 测试
git add .
git commit -m "bad message"  # 应该失败
git commit -m "feat: add feature"  # 应该成功
```

---

## 十一、常见问题与排查

### 问题 1：钩子没有执行

**检查清单**：
- 文件是否有执行权限？`chmod +x .git/hooks/pre-commit`
- 文件名是否正确（没有 .sample 后缀）？
- 脚本语法是否正确？

### 问题 2：Husky 钩子不生效

```bash
# 重新安装
npm run prepare

# 或者手动初始化
npx husky init
```

### 问题 3：如何在 CI 中使用相同检查

CI 中可以直接运行相同的检查脚本：

```yaml
# .github/workflows/ci.yml
- name: Lint
  run: npm run lint

- name: Test
  run: npm test
```

---

## 十二、延伸阅读

- [Git Hooks 官方文档](https://git-scm.com/docs/githooks)
- [Husky 文档](https://typicode.github.io/husky/)
- [Commitlint](https://commitlint.js.org/)
- [lint-staged](https://github.com/okonet/lint-staged)
- [约定式提交](https://www.conventionalcommits.org/)
