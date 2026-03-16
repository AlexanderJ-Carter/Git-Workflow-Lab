# 关卡 06：用 rebase 保持整洁历史

**所属阶段**：分支与协作
**本关命令关键词**：`git rebase`、`git rebase -i`（交互式）、`git rebase --abort`、`git rebase --continue`

---

## 一、本关目标

- 理解 `rebase` 与 `merge` 的本质区别。
- 学会用 `rebase` 让提交历史保持线性、整洁。
- 掌握交互式 rebase（`-i`）的基本操作：压缩、编辑、删除提交。
- 知道什么时候**可以**用 rebase，什么时候**绝对不要**用。

学完这一关，你就能在团队协作中做出更优雅的提交历史，而不是每次合并都产生一堆分叉。

---

## 二、前置条件

- 已完成关卡 04（分支基础）和关卡 05（合并冲突）。
- 熟悉 `git log --oneline --graph` 查看提交历史。
- 本地有一个干净的 `playground-hello` 仓库可用于练习。

> ⚠️ **重要提醒**：rebase 会改写历史。本关的所有练习请在专门的练习仓库中进行，不要在正式项目上实验。

---

## 三、边看边做前先理解的核心概念：rebase vs merge

### merge：保留分叉历史

当你用 `git merge` 合并分支时，Git 会创建一个"合并提交"，历史图上会出现分叉然后合并的形状：

```
*   merge commit
|\
| * feature 分支的提交
| *
* main 分支的提交
```

优点：完整保留了"发生了什么"的历史轨迹。

### rebase：线性历史

`rebase` 会把你的提交"移动"到目标分支的最新位置，让历史变成一条直线：

```
* feature 分支的提交（已变基）
* feature 分支的另一个提交
* main 分支的提交
```

优点：历史干净、易读；`git bisect` 等工具更容易使用。

### ⚠️ 黄金法则：不要对已推送的共享分支使用 rebase

如果其他人已经基于你的分支工作，rebase 会改写历史，导致他们的工作出现问题。**只对自己独有的分支使用 rebase**。

---

## 四、边看边做：具体步骤

### 步骤 1：准备实验环境

在 `playground-hello` 仓库中，确保 `main` 分支有至少一个提交：

```bash
git switch main
git log --oneline -3
```

如果没有，先创建一个：

```bash
echo "# Rebase Demo" >> README.md
git add README.md
git commit -m "docs: add rebase demo section"
```

### 步骤 2：创建一个特性分支并做几次提交

```bash
git switch -c feature/rebase-demo
```

做第一个提交：

```bash
echo "Feature A" >> features.txt
git add features.txt
git commit -m "feat: add feature A"
```

做第二个提交：

```bash
echo "Feature B" >> features.txt
git add features.txt
git commit -m "feat: add feature B"
```

做第三个提交：

```bash
echo "Feature C" >> features.txt
git add features.txt
git commit -m "feat: add feature C"
```

查看当前历史：

```bash
git log --oneline --graph -5
```

你应该看到一条直线的提交历史。

### 步骤 3：模拟 main 分支有新提交

切回 main 并添加一个新提交：

```bash
git switch main
echo "Main update" >> README.md
git add README.md
git commit -m "docs: update README on main"
```

现在查看历史：

```bash
git log --oneline --graph -5
```

此时 main 和 feature 分支已经分叉了。

### 步骤 4：用 merge 合并（对比实验）

先看看用 merge 会发生什么：

```bash
git switch feature/rebase-demo
git merge main
```

查看历史：

```bash
git log --oneline --graph -10
```

你会看到一个合并提交，历史出现分叉。

撤销这次合并，回到合并前：

```bash
git reset --hard HEAD~1
```

### 步骤 5：用 rebase 代替 merge

现在用 rebase 来实现同样的目标——把 main 的更新纳入 feature 分支：

```bash
git rebase main
```

再次查看历史：

```bash
git log --oneline --graph -10
```

你会看到：
- 你的 feature 提交被"移动"到了 main 最新提交之后
- 历史是一条直线，没有合并提交

这就是 rebase 的魔力——让历史保持整洁。

### 步骤 6：交互式 rebase 入门

交互式 rebase 允许你"编辑历史"——压缩、修改、删除提交。

先重置环境，创建几个小提交：

```bash
git switch main
git switch -c feature/interactive-demo

echo "1" >> nums.txt && git add nums.txt && git commit -m "fix: typo"
echo "2" >> nums.txt && git add nums.txt && git commit -m "fix: another typo"
echo "3" >> nums.txt && git add nums.txt && git commit -m "feat: add numbers"
echo "4" >> nums.txt && git add nums.txt && git commit -m "chore: update"
```

查看历史：

```bash
git log --oneline -5
```

现在我们要把这 4 个"小"提交压缩成 1 个有意义的提交。执行交互式 rebase：

```bash
# 4 表示要编辑最近 4 个提交
git rebase -i HEAD~4
```

Git 会打开编辑器，显示类似以下内容：

```text
pick abc1234 fix: typo
pick def5678 fix: another typo
pick ghi9012 feat: add numbers
pick jkl3456 chore: update

# Rebase instructions...
```

修改为：

```text
pick abc1234 fix: typo
squash def5678 fix: another typo
squash ghi9012 feat: add numbers
squash jkl3456 chore: update
```

保存并关闭编辑器。Git 会让你编辑合并后的提交信息，输入：

```text
feat: add numbers feature

- Add number sequence to nums.txt
- Fix typos during development
```

保存后查看结果：

```bash
git log --oneline -3
```

你会看到 4 个提交被压缩成了 1 个！

### 步骤 7：处理 rebase 冲突

有时候 rebase 会遇到冲突，我们模拟一下：

```bash
git switch main
echo "Main content" > conflict-file.txt
git add conflict-file.txt
git commit -m "add conflict-file on main"

git switch -c feature/conflict-demo
echo "Feature content" > conflict-file.txt
git add conflict-file.txt
git commit -m "add conflict-file on feature"

git switch main
echo "Main updated" > conflict-file.txt
git add conflict-file.txt
git commit -m "update conflict-file on main"

git switch feature/conflict-demo
git rebase main
```

你会看到冲突提示：

```text
CONFLICT (add/add): Merge conflict in conflict-file.txt
```

解决冲突：

1. 打开 `conflict-file.txt`，你会看到冲突标记
2. 编辑文件，选择你要保留的内容
3. 保存后执行：

```bash
git add conflict-file.txt
git rebase --continue
```

如果你想放弃这次 rebase：

```bash
git rebase --abort
```

---

## 五、如何确认自己做对了

- 用 `git log --oneline --graph` 查看历史，确认是线性而非分叉。
- 交互式 rebase 后，原来的多个提交被合并为一个。
- 理解了"只对自己的分支使用 rebase"这条黄金法则。

---

## 六、练习题

### 练习 1：用 rebase 修改历史提交信息

1. 创建一个分支，做 2-3 个提交。
2. 使用交互式 rebase（`reword` 命令）修改其中一个提交的信息。

### 练习 2：用 rebase 删除历史中的某个提交

1. 创建一个分支，做 3 个提交。
2. 使用交互式 rebase（`drop` 命令）删除中间那个提交。
3. 观察历史，确认该提交已消失。

### 练习 3：对比 merge 和 rebase 的结果

1. 创建两个分支：`branch-merge` 和 `branch-rebase`。
2. 在 `branch-merge` 上用 `git merge main` 合并 main 的更新。
3. 在 `branch-rebase` 上用 `git rebase main` 变基。
4. 对比两个分支的 `git log --oneline --graph`，体会区别。

---

## 七、参考答案（仅供对照）

### 练习 1 参考思路

```bash
git rebase -i HEAD~2
# 把要修改的提交前面的 pick 改成 reword
# 保存后会让你输入新的提交信息
```

### 练习 2 参考思路

```bash
git rebase -i HEAD~3
# 把要删除的提交前面的 pick 改成 drop（或直接删除那一行）
# 保存后该提交就会从历史中消失
```

### 练习 3 参考思路

merge 后的历史：

```
*   Merge branch 'main' into branch-merge
|\
| * main 的提交
* | feature 的提交
|/
* 共同祖先
```

rebase 后的历史：

```
* feature 的提交（已变基）
* main 的提交
* 共同祖先
```

---

## 八、常见错误与排查

### 问题 1：rebase 过程中想放弃

```bash
git rebase --abort
```

这会让你回到 rebase 开始前的状态。

### 问题 2：误对已推送的分支使用 rebase

如果你已经 `git push` 了分支，rebase 后再 push 会报错：

```text
! [rejected]        feature -> feature (non-fast-forward)
```

**解决方案**：
- 如果只有你一个人用这个分支：`git push --force-with-lease`
- 如果有其他人在用：**不要 force push**，只能用 merge 来补救

### 问题 3：rebase 冲突太多，太麻烦

如果冲突实在太多，可以考虑：
- 先放弃 rebase（`git rebase --abort`）
- 改用 merge，虽然历史不完美，但能完成工作
- 或者逐个提交处理冲突

---

## 九、延伸阅读

- `git rebase --onto`：更高级的变基场景
- `git cherry-pick`：选择性"摘取"提交（关卡 07 会详细讲解）
- Git 官方文档：`git help rebase`
