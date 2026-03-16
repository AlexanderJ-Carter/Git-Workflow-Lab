# 关卡 08：用 reflog 从「看似没救」的历史中恢复

**所属阶段**：救火与历史修复
**本关命令关键词**：`git reflog`、`git reset`、`git branch`、`git cherry-pick`

---

## 一、本关目标

- 理解 `reflog` 是 Git 的"时光机"和"后悔药"。
- 学会用 `reflog` 找回"丢失"的提交、分支。
- 掌握 `reset` 的三种模式（`--soft`、`--mixed`、`--hard`）的区别。
- 知道 reflog 的局限性和过期机制。

学完这一关，即使你误删了分支、误执行了 `reset --hard`，也能从容恢复。

---

## 二、前置条件

- 已完成关卡 07（cherry-pick 和 revert）。
- 熟悉 Git 的基本概念：提交、分支、HEAD。
- 有一个可以"随意折腾"的练习仓库。

---

## 三、边看边做前先理解的核心概念

### 什么是 reflog？

`reflog`（Reference Log）记录了 HEAD 指针的所有移动历史。即使你删除了分支、重置了提交，reflog 仍然保留着"曾经发生过什么"的记录。

```bash
git reflog
```

输出类似：

```text
a1b2c3d HEAD@{0}: reset: moving to HEAD~1
x1y2z3a HEAD@{1}: commit: feat: add new feature
abc1234 HEAD@{2}: checkout: moving from main to feature
...
```

每一条记录都代表 HEAD 的一次移动，你可以随时"回到"那个状态。

### reflog vs log 的区别

| 命令         | 记录内容           | 是否包含"丢失"的提交 |
| ------------ | ------------------ | -------------------- |
| `git log`    | 当前分支的提交历史 | 否                   |
| `git reflog` | HEAD 的移动历史    | **是**               |

### reset 的三种模式

| 模式              | 工作区 | 暂存区 | 提交历史 |
| ----------------- | ------ | ------ | -------- |
| `--soft`          | 保留   | 保留   | 回退     |
| `--mixed`（默认） | 保留   | 清空   | 回退     |
| `--hard`          | 清空   | 清空   | 回退     |

---

## 四、边看边做：具体步骤

### 场景 1：误执行 reset --hard 后恢复

这是最经典的 reflog 救援场景。

### 步骤 1：制造"灾难"

```bash
git switch main

# 创建一些提交
echo "Feature A" > feature-a.txt
git add feature-a.txt
git commit -m "feat: add feature A"

echo "Feature B" > feature-b.txt
git add feature-b.txt
git commit -m "feat: add feature B"

echo "Feature C" > feature-c.txt
git add feature-c.txt
git commit -m "feat: add feature C"

# 记住当前的 commit hash
CURRENT=$(git rev-parse HEAD)
echo "当前提交: $CURRENT"

# 查看当前状态
git log --oneline -5
```

### 步骤 2：模拟误操作

```bash
# 假设你不小心执行了 reset --hard，回退了 3 个提交
git reset --hard HEAD~3

# 此时你的提交"消失"了
git log --oneline -5
# feature A、B、C 都不见了！

ls
# feature-a.txt、feature-b.txt、feature-c.txt 都不见了！
```

### 步骤 3：用 reflog 查找丢失的提交

```bash
git reflog
```

你会看到类似：

```text
abc1234 HEAD@{0}: reset: moving to HEAD~3
def5678 HEAD@{1}: commit: feat: add feature C
ghi9012 HEAD@{2}: commit: feat: add feature B
jkl3456 HEAD@{3}: commit: feat: add feature A
...
```

找到 reset 之前的那个提交（`HEAD@{1}`），记下 hash。

### 步骤 4：恢复丢失的内容

```bash
# 方法 1：直接 reset 回去
git reset --hard def5678  # 替换为你的 hash

# 验证
git log --oneline -5
ls
# 一切都回来了！
```

或者用 reflog 的相对引用：

```bash
git reset --hard HEAD@{1}
```

---

### 场景 2：误删分支后恢复

### 步骤 5：创建并删除分支

```bash
# 创建一个分支
git switch -c feature/important

echo "Important work" > important.txt
git add important.txt
git commit -m "feat: important work"

# 记住这个提交
IMPORTANT_HASH=$(git rev-parse HEAD)
echo "重要提交: $IMPORTANT_HASH"

# 切回 main
git switch main

# 不小心删除了分支！
git branch -D feature/important

# 尝试切换，发现分支已不存在
git switch feature/important
# 报错：pathspec ... did not match any file(s) known to git
```

### 步骤 6：用 reflog 找回分支

```bash
git reflog
```

找到之前在 `feature/important` 分支时的提交：

```text
abc9999 HEAD@{2}: checkout: moving from main to feature/important
def8888 HEAD@{3}: commit: feat: important work
```

### 步骤 7：重建分支

```bash
# 用之前记录的 hash 创建分支
git branch feature/important $IMPORTANT_HASH

# 或者用 reflog 引用
git branch feature/important HEAD@{3}

# 验证
git switch feature/important
ls important.txt
# 找回来了！
```

---

### 场景 3：理解 reset 的三种模式

### 步骤 8：准备实验环境

```bash
git switch main

# 创建一个干净的实验分支
git switch -c experiment-reset

# 做一些修改
echo "Line 1" > test.txt
echo "Line 2" >> test.txt
git add test.txt
git commit -m "initial commit"

# 继续修改
echo "Line 3" >> test.txt
git add test.txt
git commit -m "second commit"

# 再做修改（在暂存区）
echo "Line 4" >> test.txt
git add test.txt

# 再做修改（在工作区，未暂存）
echo "Line 5" >> test.txt
```

### 步骤 9：对比三种 reset 模式

先看当前状态：

```bash
git status
# Changes to be committed: Line 4
# Changes not staged for commit: Line 5

cat test.txt
# Line 1-5 都在
```

**测试 --soft**（保留工作区和暂存区）：

```bash
git reset --soft HEAD~1

git status
# Changes to be committed: Line 3, Line 4（都在暂存区）
# Changes not staged for commit: Line 5

cat test.txt
# Line 1-5 都还在

git log --oneline -2
# second commit 不见了，但内容都保留
```

恢复环境，重新测试 **--mixed**（默认模式，清空暂存区）：

```bash
# 先恢复
git reset --hard HEAD@{1}

# 测试 --mixed
git reset --mixed HEAD~1
# 或简写为
git reset HEAD~1

git status
# Changes not staged for commit: Line 3, Line 4, Line 5（都在工作区）
# 暂存区被清空了

cat test.txt
# Line 1-5 都还在

git log --oneline -2
# second commit 不见了
```

恢复环境，测试 **--hard**（最危险，全部清空）：

```bash
# 先恢复
git reset --hard HEAD@{1}

# 测试 --hard
git reset --hard HEAD~1

git status
# nothing to commit, working tree clean

cat test.txt
# 只有 Line 1, Line 2
# Line 3, 4, 5 都没了！

git log --oneline -2
# second commit 不见了
```

---

### 场景 4：reflog 的过期机制

### 步骤 10：了解 reflog 的保留时间

```bash
# 查看默认配置
git config --get gc.reflogExpire
# 默认 90 天

git config --get gc.reflogExpireUnreachable
# 默认 30 天
```

这意味着：
- 所有 reflog 记录默认保留 90 天
- 不可达的提交默认保留 30 天

当 `git gc`（垃圾回收）运行时，过期的记录会被清理。

### 步骤 11：手动清理 reflog（谨慎操作）

```bash
# 查看所有 reflog
git reflog

# 清理过期的 reflog
git reflog expire --expire=now --all

# 执行垃圾回收
git gc --prune=now

# 再看 reflog
git reflog
# 过期记录已被清理
```

> ⚠️ **警告**：这会永久删除不可达的提交。只在确认不再需要恢复时执行。

---

## 五、如何确认自己做对了

### reflog 使用验证

- 能通过 `git reflog` 看到历史操作记录。
- 能通过 `git reset --hard HEAD@{n}` 恢复到之前的状态。
- 能恢复误删的分支。

### reset 模式理解验证

- `--soft`：提交没了，暂存区和工作区保留。
- `--mixed`：提交和暂存区没了，工作区保留。
- `--hard`：提交、暂存区、工作区都没了。

---

## 六、练习题

### 练习 1：模拟真实灾难恢复

1. 在一个分支上做 3 个提交。
2. 执行 `git reset --hard HEAD~3`。
3. 用 reflog 恢复所有提交。

### 练习 2：对比 reset 模式

1. 创建一个文件，分 3 次提交 3 行内容。
2. 在工作区添加第 4 行，暂存区添加第 5 行。
3. 分别测试 `--soft`、`--mixed`、`--hard`，观察每种模式后文件内容和状态。

### 练习 3：恢复删除的分支

1. 创建分支 `feature/test`，做一个提交。
2. 切换到 main，删除 `feature/test`。
3. 用 reflog 找回并重建该分支。

---

## 七、参考答案（仅供对照）

### 练习 1 参考思路

```bash
# 1. 创建 3 个提交
git switch -c practice/recovery
echo "1" > num.txt && git add num.txt && git commit -m "add 1"
echo "2" >> num.txt && git add num.txt && git commit -m "add 2"
echo "3" >> num.txt && git add num.txt && git commit -m "add 3"

# 2. 制造灾难
git reset --hard HEAD~3
cat num.txt  # 只有 1（或文件不存在）

# 3. 恢复
git reflog
# 找到 "add 3" 的 hash
git reset --hard <hash>
cat num.txt  # 1, 2, 3 都回来了
```

### 练习 2 参考思路

```bash
# 准备
git switch -c practice/reset-modes
echo -e "line1\nline2\nline3" > test.txt
git add test.txt && git commit -m "initial"
echo "line4" >> test.txt
git add test.txt && git commit -m "second"
echo "line5" >> test.txt
git add test.txt
echo "line6" >> test.txt

# 测试 --soft
git reset --soft HEAD~1
git status  # line5 在暂存区，line6 在工作区
cat test.txt  # line1-6 都在

# 重置再测试 --mixed
git reset --hard HEAD@{1}
git reset --mixed HEAD~1
git status  # line5 和 line6 都在工作区
cat test.txt  # line1-6 都在

# 重置再测试 --hard
git reset --hard HEAD@{1}
git reset --hard HEAD~1
git status  # 干净
cat test.txt  # 只有 line1-4
```

### 练习 3 参考思路

```bash
# 1. 创建分支
git switch -c feature/test
echo "test" > test.txt
git add test.txt && git commit -m "test commit"

# 2. 删除分支
git switch main
git branch -D feature/test

# 3. 恢复
git reflog
# 找到 "test commit" 的 hash 或 HEAD@{n}
git branch feature/test <hash>
git switch feature/test
cat test.txt  # 内容恢复
```

---

## 八、常见问题与排查

### 问题 1：reflog 里找不到我想要的提交

**可能原因**：
- 时间太久，已经被 gc 清理。
- 提交从未被任何分支或 HEAD 引用过（如 `git add` 后直接 `git reset --hard`）。

**预防**：养成经常 `git commit` 的习惯，即使是不完整的工作。

### 问题 2：reset --hard 后 reflog 也没了

不太可能发生，除非你手动执行了 `git reflog expire` 和 `git gc`。

**检查**：

```bash
git reflog
# 如果真的没了，那就真的没了...
```

### 问题 3：恢复的分支缺少某些提交

可能是找到了错误的 reflog 记录。用 `git log` 检查恢复后的分支，必要时再次从 reflog 中查找。

---

## 九、最佳实践

1. **提交频率**：经常提交，即使是小改动，这样 reflog 能记录更多。
2. **分支命名**：给重要分支起有意义的名字，方便确认 reflog 记录。
3. **定期备份**：极其重要的工作，考虑推送到远程或创建备份分支。
4. **了解 gc**：知道垃圾回收会影响 reflog，需要恢复时尽快操作。

---

## 十、延伸阅读

- `git fsck --lost-found`：查找"悬空"的提交对象
- `git stash`：临时保存工作进度（关卡 09 详解）
- Git 对象模型：理解 Git 如何存储数据有助于理解恢复原理
