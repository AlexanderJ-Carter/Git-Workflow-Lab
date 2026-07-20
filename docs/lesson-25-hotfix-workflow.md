# 关卡 25：生产 Hotfix 应急发布流程

**所属阶段**：进阶实用 / 救火  
**难度**：🟡 进阶  
**预估时间**：35 分钟  
**本关命令关键词**：`git tag`、`git switch`、`git cherry-pick`、`git merge`

---

> 💡 **学习提示**：Hotfix 的核心是「从稳定线分支出修，再回灌到所有需要该修复的分支」。在 `playground-hello` 中模拟 tag + main + develop 三线。

---

## 一、本关目标

- [ ] 能从 tag 或 `main` 切出 `hotfix/*` 分支
- [ ] 完成修复后打 patch tag 并合并回 `main`
- [ ] 会用 `cherry-pick` 或 `merge` 把同一修复带回 `develop`
- [ ] 理解 hotfix 与日常 feature 分支的区别

**前置知识：** 线上出故障时，不能等 develop 里半成品功能一起发版；hotfix 走快车道。

---

## 二、前置条件

- [ ] 已完成关卡 07（cherry-pick）和关卡 13（tags）
- [ ] 本地实验环境已启动：`docker compose up -d`
- [ ] 已 clone `playground-hello`：

  ```bash
  cd ~
  git clone http://localhost:3000/playground/playground-hello.git
  cd playground-hello
  ```

---

## 三、边看边做：具体步骤

### 步骤 1：准备「生产」与「开发」双线

```bash
cd ~/playground-hello
git switch main
git pull origin main 2>/dev/null || true

# 模拟已发布版本 v1.0.0
echo "version 1.0.0 stable" > VERSION
git add VERSION
git commit -m "chore: set version 1.0.0"
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin main --tags 2>/dev/null || git push origin main

# 创建 develop 并加入未发布功能
git switch -c develop
echo "WIP: big feature in progress" >> FEATURE_WIP.md
git add FEATURE_WIP.md
git commit -m "feat: work in progress on develop"
```

---

### 步骤 2：从 tag 切 hotfix 分支

生产环境跑的是 `v1.0.0`，bug 必须基于该 tag 修：

```bash
git switch -c hotfix/critical-typo v1.0.0
```

确认基于 tag：

```bash
git log --oneline -3
cat VERSION
```

**预期：** 看不到 `FEATURE_WIP.md` 的提交（hotfix 不含 develop 上的 WIP）。

---

### 步骤 3：修复并提交

```bash
echo "version 1.0.1 stable" > VERSION
git add VERSION
git commit -m "fix: correct version display for production"
```

---

### 步骤 4：合并回 main 并打新 tag

```bash
git switch main
git merge hotfix/critical-typo -m "merge hotfix/critical-typo into main"
git tag -a v1.0.1 -m "Hotfix 1.0.1"
git log --oneline --graph -6
```

---

### 步骤 5：把修复带回 develop（cherry-pick）

develop 上有 WIP，不能直接 merge main（会把未发布功能反向污染）。用 cherry-pick 只拿 hotfix commit：

```bash
git switch develop
git log hotfix/critical-typo --oneline -3
# 复制 fix 那条 commit hash，例如 abc1234
HOTFIX_SHA=$(git log hotfix/critical-typo --oneline -1 --grep="fix:" | awk '{print $1}')
git cherry-pick $HOTFIX_SHA
```

验证 develop 同时有 WIP 和 fix：

```bash
git log --oneline -5
test -f FEATURE_WIP.md && cat VERSION
```

**预期：** `VERSION` 为 `1.0.1`，`FEATURE_WIP.md` 仍在。

---

### 步骤 6：推送并清理 hotfix 分支

```bash
git push origin main develop --tags 2>/dev/null || true
git branch -d hotfix/critical-typo
```

---

## 四、如何确认自己做对了

```bash
cd ~/playground-hello
git tag -l "v1.0.*"
git log main --oneline -5
git log develop --oneline -5
git branch -a | grep hotfix
```

- [ ] ✓ 存在 tag `v1.0.0` 与 `v1.0.1`
- [ ] ✓ `main` 上 VERSION 为 1.0.1
- [ ] ✓ `develop` 上有 WIP 提交 **且** 包含 hotfix 的 `fix:` 提交
- [ ] ✓ `hotfix/critical-typo` 本地分支已删除（可选保留远程）

---

## 五、常见错误与排查

### ❌ 情况 1：hotfix 从 develop 切出，带上了 WIP

**可能原因：** 误用 `git switch -c hotfix/xxx develop`

**解决方法：** 始终从 tag 或 `main` 切：`git switch -c hotfix/xxx v1.0.0`

---

### ❌ 情况 2：cherry-pick 冲突

**可能原因：** develop 上同一文件也被改过

**解决方法：**

```bash
git cherry-pick --abort   # 或解决冲突后
git cherry-pick --continue
```

---

### ❌ 情况 3：忘记回灌 develop，下次 release 又出现 bug

**可能原因：** 流程断裂

**解决方法：** 团队 checklist：hotfix → main + tag → develop（cherry-pick/merge）→ 删除 hotfix 分支。

---

## 六、扩展练习

- [ ] **练习 1：** 用 `git merge hotfix/xxx` 代替 cherry-pick 回灌 develop，对比 diff
- [ ] **练习 2：** 配合关卡 21 worktree，在第二个目录做 hotfix 而不打断 develop 上的 WIP
- [ ] **练习 3：** 在 Gitea 为 `v1.0.1` 创建 Release 说明（关卡 13）

---

## 七、下一步

| 上一关 | 下一关 |
|--------|--------|
| [关卡 24：Fork 与 upstream](./lesson-24-fork-and-upstream.md) | [关卡 26：Submodule](./lesson-26-submodule.md) |
