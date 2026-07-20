# 关卡 20：用 git bisect 定位引入 Bug 的提交

**所属阶段**：救火与历史修复（进阶）  
**难度**：🟡 进阶  
**预估时间**：30 分钟  
**本关命令关键词**：`git bisect start`、`git bisect good`、`git bisect bad`、`git bisect reset`、`git bisect run`

---

> 💡 **学习提示**：左边打开本文件，右边同时打开 Web 终端，按照步骤逐条执行。

---

## 一、本关目标

- [ ] 理解「二分查找」在 Git 历史中的应用场景
- [ ] 能手动用 `git bisect` 在若干次提交中定位引入问题的 commit
- [ ] 知道如何用 `git bisect run` 配合脚本自动二分
- [ ] 完成后正确 `git bisect reset` 回到正常工作状态

**前置知识：** 当团队说「以前还好好的，某次提交之后坏了」，而你面对几十次 commit 不知道从哪查起时，可以用 bisect 把范围快速缩小到 1 次提交。

---

## 二、前置条件

- [ ] 已完成关卡 07（cherry-pick / revert）或熟悉 `git log`
- [ ] 本地实验环境已启动（`docker compose up -d`）
- [ ] 可访问 <http://localhost:8080>（Web 终端）
- [ ] 已 clone 演示仓库（任选其一）：

  ```bash
  cd ~
  git clone http://localhost:3000/playground/playground-hello.git
  cd playground-hello
  ```

---

## 三、边看边做：具体步骤

### 步骤 1：准备一段「有 good 和 bad」的历史

> **为什么要做这个步骤：** bisect 需要你知道「哪一次提交是好的、哪一次是坏的」，才能在中间不断缩小范围。

在 `playground-hello` 仓库中创建 5 次提交，并在最后一次故意引入「坏版本」：

```bash
cd ~/playground-hello
git switch main
git pull origin main 2>/dev/null || true

# 标记当前为已知 good 版本
git tag bisect-good-base 2>/dev/null || git tag -f bisect-good-base

for i in 1 2 3 4; do
  echo "step $i" >> bisect-demo.txt
  git add bisect-demo.txt
  git commit -m "chore: bisect demo step $i"
done

# 第 5 次提交：引入「坏」版本（文件里出现 BUG 字样）
echo "BUG: broken feature" >> bisect-demo.txt
git add bisect-demo.txt
git commit -m "feat: introduce regression (bad)"
```

**预期：** `git log --oneline -6` 能看到 5 条新提交，最新一条 message 含 `regression`。

---

### 步骤 2：启动 bisect 并标记 good / bad

```bash
git bisect start
git bisect bad HEAD          # 当前最新提交是坏的
git bisect good bisect-good-base   # 起始基线是好的
```

Git 会自动 checkout 到中间某次提交，终端可能提示：

```text
Bisecting: 2 revisions left to test after this (roughly 1 step)
```

**输出解读：** 表示大约还需要 1 步就能定位问题提交。

---

### 步骤 3：在中间提交上测试并标记

用 `grep` 模拟「测试是否还有 BUG」：

```bash
if grep -q "BUG:" bisect-demo.txt 2>/dev/null; then
  echo "当前版本：bad"
  git bisect bad
else
  echo "当前版本：good"
  git bisect good
fi
```

根据输出，Git 会继续 checkout 其他中间 commit，直到找到**第一个 bad 提交**。

当 bisect 结束时，你会看到类似：

```text
abc1234... is the first bad commit
commit abc1234...
    feat: introduce regression (bad)
```

记下这个 commit hash。

---

### 步骤 4：结束 bisect，恢复工作区

```bash
git bisect reset
git switch main
```

**预期：** 回到 `main` 分支，不再处于 detached HEAD 的 bisect 状态。

---

### 步骤 5（可选）：用脚本自动 bisect

```bash
git bisect start HEAD bisect-good-base

git bisect run bash -c '
  if grep -q "BUG:" bisect-demo.txt 2>/dev/null; then
    exit 1
  else
    exit 0
  fi
'

git bisect reset
```

`git bisect run` 要求：测试脚本 exit 0 表示 good，非 0 表示 bad。

---

## 四、如何确认自己做对了

```bash
cd ~/playground-hello
git status
git branch --show-current
git bisect log 2>&1 | head -1
```

- [ ] ✓ `git status` 不在 bisect 进行中（无 "You are currently bisecting" 提示）
- [ ] ✓ 当前在 `main` 分支（或你习惯的工作分支）
- [ ] ✓ 手动 bisect 时，Git 指出的 first bad commit 对应含 `BUG:` 的那次提交
- [ ] ✓ 已执行 `git bisect reset`，没有遗留在 detached HEAD

---

## 五、常见错误与排查

### ❌ `You need to start by "git bisect start"`

**可能原因：** 尚未执行 `git bisect start` 就标记 good/bad。

**解决方法：**

```bash
git bisect reset
git bisect start
git bisect bad HEAD
git bisect good <已知好的commit或tag>
```

### ❌ 标记 good/bad 后一直在 detached HEAD，不知如何退出

**可能原因：** 忘记 `git bisect reset`。

**解决方法：**

```bash
git bisect reset
git switch main
```

### ❌ `git bisect run` 脚本始终失败

**可能原因：** 脚本 exit 码与 good/bad 约定相反（0=good，非0=bad）。

**解决方法：** 本地先手动运行脚本，确认 good 提交 exit 0、bad 提交 exit 1。

### ❌ 找不到 `bisect-good-base` tag

**可能原因：** 步骤 1 未成功打 tag，或在新 clone 的仓库中练习。

**解决方法：** 用 `git log --oneline` 找 bisect 开始前的 commit hash，代替 tag 使用：

```bash
git bisect good <commit-hash>
```

---

## 六、扩展练习

- [ ] 在 `playground-ci` 仓库中，对某次 CI 配置变更做 bisect（配合 `grep workflow` 判断）
- [ ] 阅读 `git help bisect`，了解 `skip` 跳过无法测试的 commit 的用法

---

## 七、下一步

| 上一关 | 下一关 |
|--------|--------|
| [关卡 09：stash](./lesson-09-stash-usage.md) | [关卡 21：worktree](./lesson-21-worktree.md) |

---

> 📝 **更新日志**
> - 2026-07-20: 初始版本
