# 关卡 22：约定式提交（Conventional Commits）

**所属阶段**：工程化 / 发布规范  
**难度**：🟢 入门  
**预估时间**：30 分钟  
**本关命令关键词**：`git commit -m`、`git log --oneline`、`git commit --amend`

---

> 💡 **学习提示**：左边打开本文件，右边打开 Web 终端（http://localhost:8080）和 Gitea（http://localhost:3000），在 `playground-hello` 仓库中逐条执行。

---

## 一、本关目标

- [ ] 理解 Conventional Commits 的基本格式：`type(scope): subject`
- [ ] 能正确使用 `feat`、`fix`、`docs` 等常见前缀
- [ ] 知道约定式提交如何驱动 Changelog 与 Release Please
- [ ] 能在本地练习中写出 3 条符合规范的提交

**前置知识：** 完成本关后，你的提交信息能被自动化工具读懂，Release PR 和 Changelog 分类会更准确。

---

## 二、前置条件

- [ ] 已完成关卡 01–02（init、commit、log）
- [ ] 本地实验环境已启动：`docker compose up -d`
- [ ] 可访问 http://localhost:3000（Gitea）和 http://localhost:8080（Web 终端）
- [ ] 已 clone 演示仓库：

  ```bash
  cd ~
  git clone http://localhost:3000/playground/playground-hello.git
  cd playground-hello
  ```

---

## 三、边看边做：具体步骤

### 步骤 1：理解格式

约定式提交的核心结构：

```text
<type>(<scope>): <subject>

[可选正文]

[可选 footer: BREAKING CHANGE: ...]
```

常见 `type`：

| type | 含义 | 版本影响（Release Please） |
|------|------|---------------------------|
| `feat` | 新功能 | minor 版本 +1 |
| `fix` | Bug 修复 | patch 版本 +1 |
| `docs` | 仅文档 | 通常不升版本 |
| `chore` | 构建/工具 | 通常不升版本 |
| `refactor` | 重构 | 通常不升版本 |

> **为什么要做这个步骤：** 统一的提交格式让 `git log` 可读，也让 Release Please 自动归类 Changelog、计算 SemVer 版本号。

---

### 步骤 2：写一条 `docs` 提交

```bash
cd ~/playground-hello
git switch main
git pull origin main 2>/dev/null || true

echo "## Conventional Commits 练习" >> README.md
git add README.md
git commit -m "docs: add conventional commits practice section"
git log --oneline -1
```

**预期输出：**

```text
abc1234 docs: add conventional commits practice section
```

---

### 步骤 3：写一条 `feat` 提交

```bash
git switch -c feature/conventional-demo 2>/dev/null || git switch feature/conventional-demo

cat > greeting.txt << 'EOF'
Hello from conventional commits lesson!
EOF
git add greeting.txt
git commit -m "feat(greeting): add welcome message file"
git log --oneline -1
```

**输出解读：** `feat` 表示用户可见的新功能；`(greeting)` 是可选 scope，帮助定位改动模块。

---

### 步骤 4：写一条 `fix` 提交

```bash
echo "Hello from conventional commits lesson! (fixed typo)" > greeting.txt
git add greeting.txt
git commit -m "fix(greeting): correct welcome message text"
git log --oneline -3
```

---

### 步骤 5：对比「坏」提交信息

查看历史里不规范的提交（若有）：

```bash
git log --oneline -10
```

**反面示例（不要这样写）：**

```text
update
fix bug
WIP
```

**正面示例：**

```text
feat(auth): add login form validation
fix(ci): restore missing checkout step
docs(readme): document local docker ports
```

---

### 步骤 6：与 Release Please 的关系

本教学仓库根目录已有 Release Please 配置（关卡 17 会深入）。核心逻辑：

```text
feat/fix 等约定式提交 → Release Please 分析 → 生成 Release PR → 合并后打 Tag + Changelog
```

在 Gitea 打开 `playground-hello`，浏览提交历史，想象每条 `feat`/`fix` 会如何出现在 CHANGELOG 的不同小节里。

---

## 四、如何确认自己做对了

```bash
cd ~/playground-hello
git log --oneline -5
git log --grep="^feat" --oneline
git log --grep="^fix" --oneline
git log --grep="^docs" --oneline
```

- [ ] ✓ 最近 3 条提交分别以 `docs:`、`feat(`、`fix(` 开头
- [ ] ✓ 每条 subject 用英文或中文均可，但 type 必须准确
- [ ] ✓ `git status` 显示工作区干净
- [ ] ✓ 在 Gitea Web 界面（http://localhost:3000）能看到规范提交信息

---

## 五、常见错误与排查

### ❌ 情况 1：提交信息写错，还没 push

**可能原因：** 手滑把 `feat` 写成 `feature`

**解决方法：**

```bash
git commit --amend -m "feat(greeting): add welcome message file"
```

---

### ❌ 情况 2：一次 commit 混了功能 + 文档 + 重构

**可能原因：** 改动范围太大，工具无法正确分类

**解决方法：** 用 `git add -p` 分批暂存，拆成多个原子提交（参考关卡 02）。

---

### ❌ 情况 3：用了 `feat!` 或 footer 但没理解 BREAKING CHANGE

**可能原因：** 破坏性变更应触发 major 版本

**解决方法：** 仅在 API/行为不兼容时使用：

```bash
git commit -m "feat(api)!: remove deprecated endpoint

BREAKING CHANGE: /v1/users removed, use /v2/users"
```

---

## 六、扩展练习

- [ ] **练习 1：** 再写一条 `chore(deps): bump test dependency` 提交，观察 `git log` 与 `feat`/`fix` 的区别
- [ ] **练习 2：** 阅读本仓库 `release-please-config.json`，找出哪些 type 会进入 Changelog
- [ ] **练习 3：** 在 `playground-ci` 仓库里，把最近一次 CI 修复改成 `fix(ci): ...` 格式重新提交（新分支练习）

---

## 七、下一步

| 上一关 | 下一关 |
|--------|--------|
| [关卡 17：自动发布](./lesson-17-release-automation.md) | [关卡 23：PR 代码审查](./lesson-23-code-review-pr.md) |
