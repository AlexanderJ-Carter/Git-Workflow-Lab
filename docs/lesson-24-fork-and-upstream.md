# 关卡 24：Fork 与 upstream 同步

**所属阶段**：进阶实用 / 开源协作  
**难度**：🟡 进阶  
**预估时间**：40 分钟  
**本关命令关键词**：`git remote`、`git fetch`、`git merge`、`git rebase`

---

> 💡 **学习提示**：本实验环境没有真实 GitHub Fork，我们用两个本地 remote 模拟 `origin`（你的 fork）与 `upstream`（上游仓库）。

---

## 一、本关目标

- [ ] 理解 Fork 工作流：`upstream` 是源仓库，`origin` 是你的副本
- [ ] 能添加第二个 remote 并 `git fetch upstream`
- [ ] 能把 upstream 的 `main` 同步到本地（merge 或 rebase）
- [ ] 知道同步后再 push 到自己的 `origin`

**前置知识：** 参与开源项目时，你改的是 fork，但要定期从 upstream 拉更新，避免 PR 冲突爆炸。

---

## 二、前置条件

- [ ] 已完成关卡 03（remote 与 sync）和关卡 04（分支）
- [ ] 本地实验环境已启动：`docker compose up -d`
- [ ] Gitea 上有 `playground-hello` 与 `playground-ci` 两个演示仓库
- [ ] 已 clone `playground-hello` 作为「你的 fork」：

  ```bash
  cd ~
  git clone http://localhost:3000/playground/playground-hello.git playground-hello-fork
  cd playground-hello-fork
  ```

---

## 三、边看边做：具体步骤

### 步骤 1：理解 remote 角色

| Remote 名 | 在本练习中代表 | URL |
|-----------|----------------|-----|
| `origin` | 你的 fork / 可写远程 | `playground-hello` |
| `upstream` | 上游源仓库 | `playground-ci`（模拟不同项目源） |

> 真实开源场景：`upstream` = 原项目 GitHub 地址，`origin` = 你 fork 后的地址。

查看当前 remote：

```bash
cd ~/playground-hello-fork
git remote -v
```

**预期：** 只有 `origin` 指向 `playground-hello`。

---

### 步骤 2：添加上游 remote

把 `playground-ci` 当作「上游项目」模拟（两个仓库内容不同，便于观察 fetch 结果）：

```bash
git remote add upstream http://localhost:3000/playground/playground-ci.git
git remote -v
```

**预期输出：**

```text
origin    http://localhost:3000/playground/playground-hello.git (fetch)
origin    http://localhost:3000/playground/playground-hello.git (push)
upstream  http://localhost:3000/playground/playground-ci.git (fetch)
upstream  http://localhost:3000/playground/playground-ci.git (push)
```

---

### 步骤 3：fetch upstream，不自动合并

```bash
git fetch upstream
git branch -r
```

**预期：** 看到 `upstream/main`（或 upstream 的默认分支名）。

查看 upstream 最近提交：

```bash
git log upstream/main --oneline -5
git log origin/main --oneline -5
```

两条历史通常不同——这正是 fork 需要定期同步的原因。

---

### 步骤 4：在本地功能分支上开发

```bash
git switch main
git switch -c feature/upstream-sync-demo
echo "my fork contribution" >> FORK.md
git add FORK.md
git commit -m "feat: add fork contribution marker"
```

---

### 步骤 5：同步 upstream 到本地 main（merge 方式）

```bash
git switch main
git fetch upstream
git merge upstream/main -m "merge upstream/main into main"
```

若有无关历史冲突，本练习可接受；重点是走完 merge 流程。查看图：

```bash
git log --oneline --graph -8
```

---

### 步骤 6：用 rebase 方式同步（可选对比）

若你想保持线性历史，在新分支上练习 rebase：

```bash
git switch -c feature/rebase-sync-demo
# 假设 main 已 merge 过 upstream，此处演示在功能分支上变基
git switch main
git reset --hard origin/main   # 回到 fork 远程状态（练习用）
git fetch upstream

git switch -c feature/clean-sync
echo "rebase demo" >> FORK.md
git add FORK.md
git commit -m "docs: rebase sync demo"

git fetch upstream
git rebase upstream/main
```

**注意：** 若 upstream 与 origin 历史 unrelated，rebase 可能失败——真实 fork 场景里 upstream 与 origin 通常共享祖先。

---

### 步骤 7：push 到你的 origin

```bash
git switch main
git push origin main
git push -u origin feature/upstream-sync-demo 2>/dev/null || true
```

**原则：** 只 push 到 `origin`，不要 push 到 `upstream`（你没有 upstream 写权限）。

---

## 四、如何确认自己做对了

```bash
cd ~/playground-hello-fork
git remote -v
git branch -vv
git log --oneline --graph -10
```

- [ ] ✓ `git remote -v` 显示 `origin` 与 `upstream` 两个地址
- [ ] ✓ `git fetch upstream` 无报错
- [ ] ✓ 本地 `main` 已包含 upstream 的更新（merge 或 rebase 其一）
- [ ] ✓ `git push origin main` 成功

---

## 五、常见错误与排查

### ❌ 情况 1：`fatal: 'upstream' does not appear to be a git repository`

**可能原因：** URL 错误或 Gitea 未启动

**解决方法：**

```bash
docker compose ps
git remote set-url upstream http://localhost:3000/playground/playground-ci.git
```

---

### ❌ 情况 2：merge upstream 时大量 unrelated histories 冲突

**可能原因：** 本练习用两个不同仓库模拟，历史不共享

**解决方法：** 真实 fork 不会有此问题；练习时可 `git merge upstream/main --allow-unrelated-histories` 或改用同一仓库的两个 remote 指向同一 URL 练习纯流程。

---

### ❌ 情况 3：误 push 到 upstream

**可能原因：** remote 配置错误或权限误解

**解决方法：** 始终 `git push origin <branch>`；upstream 对你是只读的。

---

## 六、扩展练习

- [ ] **练习 1：** 删除 upstream 后重新添加：`git remote remove upstream`
- [ ] **练习 2：** 画一张图说明「fork → 改代码 → fetch upstream → 同步 → push origin → 开 PR 到 upstream」
- [ ] **练习 3：** 在 Gitea 上真实 fork `playground-hello` 到自己的命名空间（若环境支持），重复 remote 配置

---

## 七、下一步

| 上一关 | 下一关 |
|--------|--------|
| [关卡 23：PR 代码审查](./lesson-23-code-review-pr.md) | [关卡 25：Hotfix 工作流](./lesson-25-hotfix-workflow.md) |
