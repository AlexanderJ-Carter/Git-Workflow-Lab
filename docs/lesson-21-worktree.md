# 关卡 21：用 git worktree 同时检出多个分支

**所属阶段**：分支与协作（进阶）  
**难度**：🟡 进阶  
**预估时间**：25 分钟  
**本关命令关键词**：`git worktree add`、`git worktree list`、`git worktree remove`、`git worktree prune`

---

> 💡 **学习提示**：worktree 让你在不 stash、不反复 switch 的情况下，同时在不同目录里工作在不同分支上。

---

## 一、本关目标

- [ ] 理解 worktree 与「多次 clone 同一仓库」的区别
- [ ] 能为同一仓库添加第二个工作目录并检出不同分支
- [ ] 能在两个目录间并行修改、提交，并分别 push
- [ ] 知道如何安全删除 worktree 并清理无效引用

**前置知识：** 当你正在 `feature/A` 上改到一半，突然要修 `main` 上的 hotfix，又不想 stash 或开第二个完整 clone 时，worktree 很合适。

---

## 二、前置条件

- [ ] 已完成关卡 04（分支与 PR）
- [ ] 本地实验环境已启动（`docker compose up -d`）
- [ ] 已 clone 演示仓库：

  ```bash
  cd ~
  git clone http://localhost:3000/playground/playground-hello.git
  cd playground-hello
  ```

---

## 三、边看边做：具体步骤

### 步骤 1：查看当前 worktree

```bash
cd ~/playground-hello
git worktree list
```

**预期输出：**

```text
/home/playground/playground-hello  <hash>  [main]
```

主仓库本身就算第一个 worktree。

---

### 步骤 2：创建功能分支并添加第二个 worktree

在主目录创建并推送一个功能分支（若已存在可跳过创建）：

```bash
git switch main
git pull origin main 2>/dev/null || true
git switch -c feature/worktree-demo 2>/dev/null || git switch feature/worktree-demo
```

在**并列目录**添加 worktree（路径不要放在主仓库 `.git` 里面）：

```bash
git worktree add ../playground-hello-hotfix main
git worktree list
```

**预期输出：** 两行，分别指向 `playground-hello`（feature 分支）和 `playground-hello-hotfix`（main）。

---

### 步骤 3：在两个目录并行工作

在 hotfix worktree 修改 main：

```bash
cd ~/playground-hello-hotfix
echo "hotfix from worktree" >> HOTFIX.md
git add HOTFIX.md
git commit -m "fix: urgent hotfix via worktree"
```

回到功能分支 worktree 继续开发：

```bash
cd ~/playground-hello
echo "feature in progress" >> FEATURE.md
git add FEATURE.md
git commit -m "feat: worktree parallel feature work"
```

分别查看状态，互不影响：

```bash
git -C ~/playground-hello log --oneline -2
git -C ~/playground-hello-hotfix log --oneline -2
```

---

### 步骤 4：推送并合并（可选）

```bash
cd ~/playground-hello
git push -u origin feature/worktree-demo

cd ~/playground-hello-hotfix
git push origin main
```

在 Gitea 上可为 `feature/worktree-demo` 开 PR；hotfix 已直接在 `main` 上（练习环境可接受，团队项目应走 PR）。

---

### 步骤 5：删除 worktree

hotfix 完成后移除额外 worktree：

```bash
cd ~/playground-hello
git worktree remove ../playground-hello-hotfix
git worktree list
```

若目录已被手动删掉，可清理残留记录：

```bash
git worktree prune
```

---

## 四、如何确认自己做对了

```bash
cd ~/playground-hello
git worktree list
git status
ls ../playground-hello-hotfix 2>&1
```

- [ ] ✓ `git worktree list` 只剩主 worktree 一行（或你 intentionally 保留的其他 worktree）
- [ ] ✓ `../playground-hello-hotfix` 目录不存在（或 remove 后已删除）
- [ ] ✓ 两个分支上的提交分别存在于 `git log feature/worktree-demo` 与 `git log main`
- [ ] ✓ 主仓库 `git status` 干净，没有误删 `.git` 或 worktree 元数据报错

---

## 五、常见错误与排查

### ❌ `fatal: 'path' is already a working tree`

**可能原因：** 目标路径已是另一个 worktree 或普通 clone。

**解决方法：**

```bash
git worktree list
# 若路径已注册，先 remove；若是旧 clone，换用新路径名
git worktree add ../playground-hello-wt2 main
```

### ❌ `fatal: 'main' is already checked out`

**可能原因：** 同一分支不能同时在两个 worktree 中 checkout（旧版 Git 限制；Git 2.5+ 通常允许，但部分环境仍报错）。

**解决方法：** 在第二个 worktree 检出**不同分支**，例如新建 `hotfix/worktree`：

```bash
git branch hotfix/worktree main
git worktree add ../playground-hello-hotfix hotfix/worktree
```

### ❌ `git worktree remove` 提示 dirty

**可能原因：** worktree 目录有未提交修改。

**解决方法：**

```bash
cd ../playground-hello-hotfix
git status
git add -A && git commit -m "wip"   # 或 git restore . 丢弃
cd ~/playground-hello
git worktree remove ../playground-hello-hotfix
```

### ❌ 手动 `rm -rf` worktree 目录后 `git worktree list` 仍显示

**解决方法：**

```bash
git worktree prune
```

---

## 六、扩展练习

- [ ] 为 `playground-ci` 添加 worktree，在一份目录改 workflow、另一份目录改 README，互不干扰
- [ ] 对比：`git stash` + `git switch` 与 worktree 各适合什么场景？写三句总结

---

## 七、下一步

| 上一关 | 下一关 |
|--------|--------|
| [关卡 20：bisect](./lesson-20-bisect.md) | [关卡总览](./lessons-overview.md) |

---

> 📝 **更新日志**
> - 2026-07-20: 初始版本
