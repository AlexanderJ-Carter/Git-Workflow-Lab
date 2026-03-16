# 关卡 04：创建分支 & 提交 Pull Request 合并代码

**所属阶段**：分支与协作  
**本关命令关键词**：`git branch`、`git switch` / `git checkout`、`git merge`、`git log --oneline --graph`

---

## 一、本关目标

- 学会在本地创建分支并切换。
- 在新分支上开发新功能（或修改），并推送到远程。
- 在 Web 界面（Gitea）上发起 Pull Request，并合并到主分支。

学完这一关，你就完成了最典型的一次「feature 分支开发 → 提交 PR → 合并」流程。

---

## 二、前置条件

- 已完成基础关卡 01–03。
- Gitea 中已有一个仓库（如 `playground-hello`），主分支为 `main`。
- 本地已经 clone 了该仓库，且 `git status` 显示工作区干净。

---

## 三、边看边做：具体步骤

### 步骤 1：确认当前分支与提交情况

在本地仓库根目录执行：

```bash
git branch
git log --oneline -5
```

你应该看到当前分支是 `main`，并且最近有你之前练习产生的提交。

### 步骤 2：创建 feature 分支并切换

假设我们要开发一个新功能，用分支名 `feature/profile-section`：

```bash
git switch -c feature/profile-section
```

如果你的 Git 版本较老，也可以使用：

```bash
git checkout -b feature/profile-section
```

再次查看分支：

```bash
git branch
```

确认当前分支前有 `*` 标记在 `feature/profile-section` 上。

### 步骤 3：在新分支上做一些修改

例如在 `README.md` 里加一个「个人信息」小节：

```markdown
## 个人信息（示例）

- 昵称：Git 学徒
- 正在练习：分支与 Pull Request
```

然后：

```bash
git status
git diff
git add README.md
git commit -m "feat: add profile section in README"
```

### 步骤 4：把分支推到远程

将当前分支推送到远程，并建立跟踪关系：

```bash
git push -u origin feature/profile-section
```

执行完后，你应该在命令行输出中看到提示，说明远程创建了对应的分支。

### 步骤 5：在 Gitea 上发起 Pull Request

1. 打开浏览器访问 Gitea 仓库页面。
2. 切换到 `feature/profile-section` 分支，确认刚刚的改动已经在 Web 中可见。
3. 在页面中找到「New Pull Request」或类似入口：
   - 选择「从 `feature/profile-section` 合并到 `main`」。
4. 填写 PR 标题和说明，例如：
   - Title：`feat: add profile section in README`
   - Description：简单说明本次改动。
5. 创建 PR。

如果没有冲突，Gitea 一般会显示可以直接合并的按钮。

### 步骤 6：合并 PR 并清理分支

1. 在 PR 页面点击合并按钮（根据 Gitea 配置，可能是「Merge」或「Squash and merge」等）。
2. 合并成功后，你会看到改动已经出现在 `main` 分支中。

回到本地，先切回 `main` 分支并同步远程：

```bash
git switch main
git pull origin main
git log --oneline --graph --decorate -10
```

确认 `main` 上已经包含了刚才在 `feature/profile-section` 中的提交。

可选：在远程和本地删除已经合并的 feature 分支：

```bash
git push origin --delete feature/profile-section
git branch -d feature/profile-section
```

---

## 四、如何确认自己做对了

- 在本地：
  - `git branch` 中可以看到你创建的 feature 分支，并能在 `main` 与该分支之间切换。
  - `git log --oneline --graph --decorate` 显示 `main` 分支已经包含了 feature 分支的提交。
- 在 Gitea Web 界面：
  - 可以看到已经合并完成的 Pull Request。
  - `main` 分支下的文件内容包含你在 feature 分支中添加的修改。

---

## 五、练习题

### 练习 1：再创建一个小功能分支

1. 从最新的 `main` 分支创建一个新的分支：`feature/todo-section`。
2. 修改 README 或新增一个文件（例如 `TODO.md`），写上你下一步想练习的内容。
3. 提交并推送分支。
4. 在 Gitea 上发起 PR 并合并。

### 练习 2：观察分支合并前后的提交图

1. 在合并 PR 之前，使用：

   ```bash
   git log --oneline --graph --decorate --all
   ```

   观察 `main` 与 feature 分支的关系。

2. 合并 PR 并 `git pull` 之后，再次执行上述命令。
3. 比较合并前后 `main` 的提交结构有何变化。

---

## 六、参考答案（仅供对照）

### 练习 1 参考思路

```bash
git switch main
git pull origin main

git switch -c feature/todo-section
echo "- 下一关：练习合并冲突" > TODO.md
git add TODO.md
git commit -m "docs: add TODO for next practice"
git push -u origin feature/todo-section
```

然后在 Gitea 上按本关步骤发起 PR 并合并，最后在本地：

```bash
git switch main
git pull origin main
git branch -d feature/todo-section
git push origin --delete feature/todo-section
```

### 练习 2 参考思路

合并前的 `git log --oneline --graph --decorate --all` 可能类似：

```text
* abc1234 (HEAD -> feature/profile-section, origin/feature/profile-section) feat: add profile section in README
| * 7890abc (origin/main, main) previous commit on main
|/
* 1234567 older commit...
```

合并 PR 并同步后，可能变为（取决于使用的合并策略）：

```text
* def5678 (HEAD -> main, origin/main) Merge branch 'feature/profile-section'
|\
| * abc1234 feat: add profile section in README
* | 7890abc previous commit on main
|/
* 1234567 older commit...
```

通过对比，你可以直观理解「分支」其实就是在提交图上的一条指针，而 PR 合并就是把分支上的提交合入主线。

