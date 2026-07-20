# 关卡 28：Blame 与历史考古（git blame / log -S / follow）

**所属阶段**：进阶实用  
**难度**：🟡 进阶  
**预估时间**：30 分钟  
**本关命令关键词**：`git blame`、`git log -S`、`-G`、`--follow`、`git show`

---

> 💡 **学习提示**：当线上出问题、需要回答「这行谁写的、哪次引入的」时，用本关命令比翻聊天记录快得多。

---

## 一、本关目标

- [ ] 用 `git blame` 定位某行代码的最后修改者与 commit
- [ ] 用 `git log -S` 查找「引入/删除某字符串」的提交
- [ ] 用 `git log -G` 按正则搜索 diff 内容
- [ ] 用 `git log --follow` 追踪重命名前的文件历史
- [ ] 用 `git show` 查看单次提交的完整 diff

**前置知识：** Code review、Bug 溯源、合规审计都依赖「历史考古」技能。

---

## 二、前置条件

- [ ] 已完成关卡 02（diff、log）
- [ ] 本地实验环境已启动：`docker compose up -d`
- [ ] 已 clone 本教学仓库或 `playground-hello`（本关两种均可；以下以 `playground-hello` 为主）：

  ```bash
  cd ~
  git clone http://localhost:3000/playground/playground-hello.git
  cd playground-hello
  ```

---

## 三、边看边做：具体步骤

### 步骤 1：制造可追踪的历史

```bash
cd ~/playground-hello
git switch main
git pull origin main 2>/dev/null || true

git switch -c feature/archaeology-demo 2>/dev/null || git switch feature/archaeology-demo

cat > app.config << 'EOF'
debug=false
feature_flag=old_value
timeout=30
EOF
git add app.config
git commit -m "feat: add app.config with feature flag"

sed -i 's/feature_flag=old_value/feature_flag=new_value/' app.config
git add app.config
git commit -m "fix: update feature flag value"

sed -i 's/timeout=30/timeout=60/' app.config
git add app.config
git commit -m "perf: increase timeout to 60"
```

---

### 步骤 2：git blame — 谁改了这一行

```bash
git blame app.config
git blame -L 3,3 app.config
```

**预期输出示例：**

```text
abc1234 (You 2026-...) 3) feature_flag=new_value
```

**输出解读：** 左侧 commit SHA、作者、时间；右侧行内容。`-L 3,3` 只看第 3 行。

忽略空白变更：

```bash
git blame -w app.config
```

---

### 步骤 3：git log -S — 何时引入字符串

查找「哪次提交引入或删除 `feature_flag=new_value`」：

```bash
git log -S "feature_flag=new_value" --oneline -- app.config
git log -S "feature_flag=old_value" --oneline -- app.config
```

**解读：** `-S` 即 pickaxe，找 diff 里**新增或删除**该字符串的 commit（不是 merely 出现）。

查看该 commit 详情：

```bash
git show $(git log -S "feature_flag=new_value" --oneline -1 -- app.config | awk '{print $1}')
```

---

### 步骤 4：git log -G — 按正则搜 diff

```bash
git log -G "timeout=[0-9]+" --oneline -- app.config
```

**对比 -S 与 -G：**

| 选项 | 匹配方式 |
|------|----------|
| `-S<string>` | 固定字符串在 diff 中增删 |
| `-G<regex>` | 正则匹配 diff  hunks |

---

### 步骤 5：git log --follow — 追踪重命名

```bash
git mv app.config application.config
git commit -m "refactor: rename app.config to application.config"

git log --oneline -- application.config        # 可能只看到 rename
git log --follow --oneline -- application.config
```

**预期：** `--follow` 能穿过 rename，看到 `app.config` 时代的 `feat:` / `fix:` 提交。

---

### 步骤 6：在本仓库做真实考古（可选）

若已 clone Git Workflow Lab 本体：

```bash
cd /workspace  # 或你的 clone 路径
git blame -L 1,5 docs/lessons-overview.md
git log -S "sparse-checkout" --oneline -- docs/
git log --follow --oneline -- docs/learning-path.md | head -5
```

---

## 四、如何确认自己做对了

```bash
cd ~/playground-hello
git blame -L 1,1 application.config 2>/dev/null || git blame -L 1,1 app.config
git log -S "feature_flag" --oneline
git log --follow --oneline -5 -- application.config 2>/dev/null || true
```

- [ ] ✓ `git blame` 能指出 `feature_flag` 或 `timeout` 行的 commit
- [ ] ✓ `git log -S` 能找到引入/修改 feature flag 的提交
- [ ] ✓ 重命名后 `--follow` 能看到 rename 之前的 history
- [ ] ✓ `git show <sha>` 能展示完整 patch

---

## 五、常见错误与排查

### ❌ 情况 1：blame 显示整文件都是同一人

**可能原因：** 文件来自一次大提交或 `git mv` 未拆 history

**解决方法：** 用 `git log --follow -p -- file` 看详细演进。

---

### ❌ 情况 2：`-S` 搜不到预期 commit

**可能原因：** 该 commit 只是修改上下文，字符串字数未变（如只改相邻行）

**解决方法：** 改用 `-G` 或 `git log -p --grep=`。

---

### ❌ 情况 3：blame 误伤 — 大规模格式化 commit

**可能原因：** 某次 `style: format all` 改写了每行

**解决方法：**

```bash
git blame --ignore-rev <formatting-commit-sha> -- file
# Git 2.23+ 可用 .git-blame-ignore-revs 文件
```

---

## 六、扩展练习

- [ ] **练习 1：** `git log -p -S "timeout" -- app.config` 看完整 patch
- [ ] **练习 2：** 在 `playground-ci` 里用 `-S` 找哪次 commit 添加了 workflow 文件
- [ ] **练习 3：** 用 `git bisect`（关卡 20）配合 `-S` 定位引入 bug 的提交

---

## 七、下一步

| 上一关 | 下一关 |
|--------|--------|
| [关卡 27：交互式 rebase 进阶](./lesson-27-interactive-rebase-fixup.md) | [关卡 29：Sparse checkout](./lesson-29-sparse-checkout.md) |
