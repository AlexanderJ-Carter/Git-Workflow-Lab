# 关卡 05：制造并解决一次合并冲突

**所属阶段**：分支与协作  
**本关命令关键词**：`git merge`、合并冲突解决、`git status`、`git diff`、`git add`、`git commit`

---

## 一、本关目标

- 亲手「制造」一次可控的合并冲突。
- 学会从 `git status`、文件中的冲突标记来理解哪里冲突了。
- 正确编辑文件解决冲突，并完成合并提交。

学完这一关，你以后在真实项目里遇到冲突就不会慌了。

---

## 二、前置条件

- 已完成分支关卡（建议至少完成 04）。
- 当前本地仓库 `main` 分支是干净的，并已同步远程。

在开始前，建议先备份一份仓库或确认这是练习仓库，以便随时重来。

---

## 三、边看边做：具体步骤

### 步骤 1：准备一个基础文件

在 `main` 分支上，创建或编辑一个简单的文本文件，例如 `conflict-demo.txt`：

```text
line 1: base
line 2: will be changed on branch A
line 3: will be changed on branch B
```

保存后：

```bash
git add conflict-demo.txt
git commit -m "chore: add conflict demo base file"
git push origin main
```

### 步骤 2：从 main 创建两个分支

我们创建两个分支，分别在其中修改同一行，制造冲突：

```bash
git switch main
git pull origin main

git switch -c feature/branch-a
```

在 `feature/branch-a` 上，把 `conflict-demo.txt` 的第 2 行改成：

```text
line 2: change from branch A
```

然后：

```bash
git add conflict-demo.txt
git commit -m "feat: change line 2 from branch A"
git push -u origin feature/branch-a
```

切回 `main`，再创建 B 分支：

```bash
git switch main
git switch -c feature/branch-b
```

在 `feature/branch-b` 上，把 **同一行** 改成：

```text
line 2: change from branch B
```

然后：

```bash
git add conflict-demo.txt
git commit -m "feat: change line 2 from branch B"
git push -u origin feature/branch-b
```

此时：

- `feature/branch-a` 和 `feature/branch-b` 都基于同一个 `main` 创建。
- 它们分别改了同一行内容，具备产生冲突的条件。

### 步骤 3：尝试在 main 上合并分支，触发冲突

回到 `main`：

```bash
git switch main
git pull origin main
```

先把 A 分支合进来（此时不会冲突）：

```bash
git merge feature/branch-a
git push origin main
```

再尝试把 B 分支也合进来：

```bash
git merge feature/branch-b
```

你应该会看到提示有冲突，类似：

```text
Auto-merging conflict-demo.txt
CONFLICT (content): Merge conflict in conflict-demo.txt
Automatic merge failed; fix conflicts and then commit the result.
```

### 步骤 4：查看冲突状态与冲突标记

先看状态：

```bash
git status
```

会提示有未合并的路径（unmerged paths），例如：

```text
both modified:   conflict-demo.txt
```

打开 `conflict-demo.txt`，你会看到 Git 自动插入了冲突标记：

```text
line 1: base
<<<<<<< HEAD
line 2: change from branch A
=======
line 2: change from branch B
>>>>>>> feature/branch-b
line 3: will be changed on branch B
```

含义：

- `<<<<<<< HEAD` 到 `=======` 之间，是当前分支（main，已包含 branch-a 的改动）的内容。
- `=======` 到 `>>>>>>> feature/branch-b` 之间，是你要合并进来的分支（branch-b）的内容。

### 步骤 5：编辑文件解决冲突

现在根据业务需求决定「最终版本」应该是什么。这里我们随便举例，比如想保留两者的内容：

```text
line 1: base
line 2: change from branch A and branch B
line 3: will be changed on branch B
```

**关键：记得删除所有冲突标记行**（`<<<<<<<`、`=======`、`>>>>>>>`）。

保存文件后：

```bash
git status
```

可以看到 `conflict-demo.txt` 仍然在「未合并的更改」列表中。

### 步骤 6：标记冲突已解决并完成合并提交

当你确认文件内容已经是想要的最终版本后，执行：

```bash
git add conflict-demo.txt
git status
```

此时应显示「All conflicts fixed but you are still merging.」或类似提示。

最后创建合并提交：

```bash
git commit -m "merge: resolve conflict between branch-a and branch-b"
git log --oneline --graph --decorate -5
git push origin main
```

在 Gitea 上刷新 `main` 分支页面，确认：

- 提交历史中有这次「解决冲突」的 merge commit。
- `conflict-demo.txt` 内容是你期望的最终版本。

---

## 四、如何确认自己做对了

- 没有残留任何 `<<<<<<<` / `=======` / `>>>>>>>` 冲突标记在文件中。
- `git status` 显示工作区干净。
- `git log --oneline --graph --decorate` 中可以看到 `feature/branch-a` 和 `feature/branch-b` 的提交都被包含在 `main` 里，并出现了一个合并提交。
- 在 Gitea Web 上，`main` 分支下的 `conflict-demo.txt` 内容为你编辑后的最终版本。

---

## 五、练习题

### 练习 1：尝试不同的解决策略

1. 重新制造一次类似的冲突（可以新建文件或改行）。
2. 尝试只保留 A 分支的改动（相当于丢弃 B 的内容）。
3. 再次练习，尝试只保留 B 分支的改动。

思考：在什么场景下你会需要「只保留一边」？

### 练习 2：在图形化工具中解决冲突（可选）

如果你习惯使用 VS Code 或其他 IDE：

1. 在出现冲突后，用编辑器打开项目。
2. 使用编辑器提供的「接受当前变更 / 接受传入变更 / 接受双方变更」按钮解决冲突。
3. 观察编辑器底部的 Git 状态变化。

---

## 六、参考答案（仅供对照）

### 练习 1 参考思路

只保留 A 分支内容时，`conflict-demo.txt` 中相关区域可改为：

```text
line 1: base
line 2: change from branch A
line 3: will be changed on branch B
```

然后：

```bash
git add conflict-demo.txt
git commit -m "merge: resolve conflict keep branch A"
```

只保留 B 分支内容时则类似，只是将该行改为 B 的版本。

> 实际项目中，也常见「先保留一方，然后后续再补丁合并另一方需要的部分」的做法。

