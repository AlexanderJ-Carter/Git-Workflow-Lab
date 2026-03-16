# 关卡 03：远程仓库与同步（remote / fetch / pull / push）

**所属阶段**：Git 基础操作实验  
**本关命令关键词**：`git remote`、`git remote -v`、`git fetch`、`git pull`、`git push`、`git log`

---

## 一、本关目标

- 搞清楚「本地仓库」和「远程仓库」的关系。
- 知道 `git remote` 是干嘛的，能看懂 `origin` 等远程名称。
- 会区分 `git fetch` 和 `git pull` 的作用和区别。
- 能在「别人先 push 了」的情况下，把远程更新同步到本地，再继续开发。

学完这一关，你在日常协作中，看到 `failed to push some refs` 之类提示时，就能比较从容地理解发生了什么、该怎么做。

---

## 二、前置条件

- 已完成 **关卡 01：新建仓库并 push 代码** 和 **关卡 02：工作区 / 暂存区 / 提交历史**。
- 本地已经有一个 `playground-hello` 仓库，并能正常 `git status`。
- 推荐在开始前先 `git status` 确认当前工作区是干净的。

---

## 三、边看边做：具体步骤

> 建议：左边打开本文件，右边同时打开 Gitea 网页 + 本地终端，按步骤往下做。

### 步骤 1：认识远程仓库（remote）

先在 `playground-hello` 目录下看看当前配置了哪些远程：

```bash
git remote
git remote -v
```

观察：

- 你应该能看到一个叫 `origin` 的远程。
- `git remote -v` 会显示它对应的 URL，例如：  
  `http://localhost:3000/<你的用户名>/playground-hello.git`

思考：

- `origin` 只是一个**名字**，惯例叫法，用来引用这个远程地址。
- 真正的 “托管平台上的仓库” 就是这个 URL 对应的仓库。

---

### 步骤 2：模拟「别人先 push 了」的场景

为了模拟团队协作，我们直接在 Web 界面上动手：

1. 打开浏览器，进入 Gitea 上的 `playground-hello` 仓库页面。
2. 点击右上角的 `Edit`（或创建一个新文件），比如修改 `README.md`，随便加一行：

   ```markdown
   ## Update from web UI
   ```

3. 在 Web 界面里直接提交（Commit changes），并使用一个醒目的提交信息，例如 `chore: update from web`。

此时：

- 远程仓库（Gitea）上的提交已经**比本地多了一次**。
- 本地仓库还是停留在旧的提交历史。

在本地终端中执行：

```bash
git log --oneline -5
```

注意：你看不到刚才在 Web 上那次提交。

---

### 步骤 3：用 `git fetch` 把远程最新信息拉到本地

执行：

```bash
git fetch origin
```

然后再看日志：

```bash
git log --oneline --all --graph --decorate -10
```

观察：

- 你现在应该能在 `--all` 的视图里看到一个**在前面多出来的提交**，一般标在 `origin/main` 或类似的远程分支上。
- 但是，本地当前所在的 `main` 分支**指向的还是旧的提交**。

总结一下：

- `git fetch`：只更新「远程分支的指针」（如 `origin/main`），**不会自动合并到你当前分支**。

---

### 步骤 4：用 `git pull` 一步完成「fetch + 合并」

常见用法：

```bash
git pull origin main
```

再看状态和日志：

```bash
git status
git log --oneline --graph --decorate -5
```

此时：

- 你的本地 `main` 分支已经包含了刚才 Web 上那次提交。
- `git pull` 默认等价于：`git fetch` + `git merge`（也可以改为 rebase，这是进阶内容，在后续关卡中会再提）。

> 小提示：  
> - 习惯做法是经常 `git fetch` 看一下远程情况，而不仅仅在 push 失败时才去拉。  
> - 当你对「自动 merge」不放心时，可以先 `git fetch` 再手动决定是 `merge` 还是 `rebase`。

---

### 步骤 5：在本地制造新提交并 push

现在，在本地继续开发，制造一个新的提交：

```bash
echo "New line from local dev" >> README.md

git status
git add README.md
git commit -m "feat: add local change after remote update"
```

先看一下本地和远程的关系：

```bash
git log --oneline --graph --decorate -5
```

如果一切顺利，此时你的 `main` 分支**应该领先 `origin/main` 一个提交**（多出刚才这条本地提交）。

现在 push：

```bash
git push origin main
```

回到浏览器刷新仓库页面，确认：

- Git 历史中多了一条你刚才的提交。
- `README.md` 中同时包含 Web 修改的那一行和你刚才本地新增的那一行。

---

### 步骤 6：故意制造一次 push 冲突并解决

这一小节是为了让你亲手体验一次常见报错：“远程有更新，push 被拒绝”。

1. 确保现在本地 `git status` 是干净的。
2. 再次在 Web 上打开 `README.md`，新增一行内容，并直接提交（形成一条远程新提交）。
3. 不要 `pull`，直接在本地修改同一个 `README.md` 文件，再新增一行，比如：

   ```bash
   echo "Another local change without pulling" >> README.md
   git add README.md
   git commit -m "feat: local change without pull"
   ```

4. 现在直接执行：

   ```bash
   git push origin main
   ```

你应该会看到类似提示：

```text
! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'http://localhost:3000/.../playground-hello.git'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. This is usually caused by another repository pushing
hint: to the same ref. You may want to first integrate the remote changes...
```

这就是典型的「别人先 push 了，而你没先同步」场景。

解决方式之一（基于 merge）：

```bash
git pull origin main
```

- 如果没有冲突，会自动完成 merge，然后你再执行一次：

  ```bash
  git push origin main
  ```

- 如果产生了冲突：  
  - Git 会告诉你哪些文件存在冲突。  
  - 你需要打开这些文件，手动解决冲突标记（`<<<<<<<` / `=======` / `>>>>>>>`），然后：

    ```bash
    git add <有冲突的文件>
    git commit   # 完成这次合并提交
    git push origin main
    ```

> 详细的冲突解决，会在后续专门的「合并冲突」关卡里展开，这里主要让你感受一下 push 冲突的来龙去脉。

---

## 四、如何确认自己做对了

- 在终端中：
  - 你能看懂 `git remote -v` 输出的含义，知道 `origin` 对应哪个 URL。
  - 在不同阶段，通过 `git log --oneline --graph --decorate` 观察本地分支和 `origin/main` 之间的领先/落后关系。
  - 在看到 `failed to push some refs` 时，知道可以先 `git pull`（或 `git fetch` + 合并）再 push。
- 在 Gitea Web 界面：
  - 能从 Commit 历史中清晰看到：Web 编辑提交、本地提交、可能的 merge 提交的先后顺序。
  - 能确认最终的 `README.md` 同时包含来自 Web 和本地的修改。

---

## 五、常见错误与排查

- 情况 A：`fatal: not a git repository (or any of the parent directories): .git`
  - 说明：当前目录不是一个 Git 仓库。
  - 解决：确认你在 `playground-hello` 目录内，可以用 `pwd` / `cd` 切换到正确目录。

- 情况 B：`fatal: 'origin' does not appear to be a git repository`
  - 说明：当前项目没有配置名为 `origin` 的远程，或者被误删了。
  - 解决：使用 `git remote -v` 检查，如果没有，可以重新添加：

    ```bash
    git remote add origin http://localhost:3000/<你的用户名>/playground-hello.git
    ```

- 情况 C：`failed to push some refs` / 提示需要先 pull
  - 说明：远程有你本地没有的提交。
  - 解决：先执行 `git fetch origin` 看远程的状态；再选择：
    - `git pull origin main` 让 Git 自动合并，或  
    - 高阶做法：先 `git fetch`，再用 `git rebase origin/main`（会在后续 rebase 关卡详解）。

---

## 六、思考题 / 扩展练习（可选）

- 练习 1：尝试在本地创建一个新的远程名（例如 `backup`），指向同一个 URL，然后用 `git push backup main` 推送一次，观察远程列表的变化。
- 练习 2：试着只用 `git fetch` + `git merge` 的方式，而不是 `git pull`，完成一次“别人先 push 了”的更新同步。
- 练习 3：在你熟悉的真实 GitHub / GitLab 仓库中，找一个分支，观察它的远程配置与这里的实验环境有何异同。

# 关卡 03：远程仓库与同步（pull / fetch / push）

**所属阶段**：Git 基础操作实验  
**本关命令关键词**：`git remote`、`git push`、`git pull`、`git fetch`、`git log --oneline --graph`

---

## 一、本关目标

- 看懂本地仓库绑定了哪些远程地址（remote）。
- 区分 `push`、`pull`、`fetch` 的作用和差异。
- 模拟「别人先 push 了，你再 push 被拒绝」的场景，并学会正确处理。

学完这一关，你就能比较自信地在团队协作中和远程仓库打交道了。

---

## 二、前置条件

- 已完成前两关，且在 Gitea 中有一个仓库（如 `playground-hello`）。
- 本地已经有该仓库的 clone，并且能正常 `git status`。

---

## 三、边看边做：具体步骤

### 步骤 1：查看当前远程配置

在仓库根目录执行：

```bash
git remote -v
```

你应该看到类似：

```text
origin  http://localhost:3000/<用户名>/playground-hello.git (fetch)
origin  http://localhost:3000/<用户名>/playground-hello.git (push)
```

说明：

- `origin` 是远程仓库的默认名字。
- 同一个远程可以有 fetch 和 push 两种用途，一般地址相同。

### 步骤 2：确认当前分支与远程分支的关系

```bash
git status
```

关注其中一行：

- `Your branch is up to date with 'origin/main'.`  
  说明本地 `main` 分支和远程 `origin/main` 内容一致。
- 如果是 `ahead of` 或 `behind`，说明你本地/远程有不同步的提交。

你也可以用：

```bash
git log --oneline --graph --decorate --all
```

来可视化本地和远程分支的提交图。

### 步骤 3：做一次本地提交并 push

随便修改一个文件，例如在 `README.md` 中加入一行：

```markdown
- 练习：理解 push / pull / fetch
```

然后：

```bash
git add README.md
git commit -m "docs: add remote practice note"
git push origin main
```

刷新 Gitea 上的仓库页面，确认最新提交已经出现在网页上。

### 步骤 4：模拟「远程有新提交，你本地落后」的场景

> 这一步可以有两种做法：  
> - 在同一台机器上，用另一个目录 clone 一份仓库作为「同事版本」。  
> - 或者直接在 Gitea Web 上在线编辑文件，生成一条新的提交。  
> 这里我们用**在线编辑**的方式，比较简单。

1. 在 Gitea Web 界面打开仓库中的 `README.md`。
2. 点击编辑按钮（铅笔图标），随便加一行，例如：

   ```markdown
   - 这是一条来自 Web 的修改
   ```

3. 在页面底部填写提交说明，例如：`docs: update from web`，保存提交。

此时，**远程 main 分支比本地 main 多了一次提交**。

### 步骤 5：尝试直接 push，观察被拒绝的情况

回到本地仓库，先不 `pull`，直接修改一个文件并提交：

```bash
echo "local change" >> local.txt
git add local.txt
git commit -m "chore: local commit after web change"

git push origin main
```

你大概率会看到类似报错：

```text
! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'http://localhost:3000/...'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. This is usually caused by another repository pushing
hint: to the same ref. You may want to first integrate the remote changes...
```

这就是典型的「别人先 push 了，你的 push 被拒绝」情况。

### 步骤 6：使用 pull 合并远程修改

现在来正确处理：

```bash
git pull origin main
```

可能出现两种情况：

- **没有冲突**：Git 自动创建一个 merge commit 或 fast-forward。
- **有冲突**：需要你手动解决（可以留给后面的冲突关卡详细讲）。

若无冲突，再次查看日志：

```bash
git log --oneline --graph --decorate --all
```

确认本地 `main` 已经包含了刚刚那条 Web 上的提交，以及你的本地提交。

然后再次 push：

```bash
git push origin main
```

应该就能成功。

### 步骤 7：使用 fetch 只更新远程引用，不合并

再来看 `fetch` 的作用。

```bash
git fetch origin
```

说明：

- `fetch` 会更新本地对于远程分支的引用（如 `origin/main`），但不会自动合并到你的当前分支。
- 你可以通过日志/图形化工具对比「我当前分支」和「远程分支」的差异，然后选择如何合并（`merge`/`rebase`）。

试试：

```bash
git log --oneline --graph --decorate --all
```

观察 `origin/main` 与 `main` 的关系。

---

## 四、如何确认自己做对了

- 你能通过 `git remote -v` 看清楚当前仓库连接到哪个远程。
- 你能用「在 Web 上编辑文件」的方式，制造远程比本地新的提交。
- 在被 `git push` 拒绝后，你知道应该先 `git pull`（或先 `fetch` 再合并），而不是一上来就 `--force`。
- 你弄清楚了：
  - `push`：把本地提交推到远程。
  - `pull`：等于 `fetch + merge`（默认情况）。
  - `fetch`：只更新远程引用，不改动你的当前分支。

---

## 五、练习题

### 练习 1：用两个本地 clone 模拟「你和同事」

1. 在同一台机器上，再 clone 一份 `playground-hello` 到另一个目录，假设这份是「同事」。
2. 在「同事」目录中做一个提交并 push。
3. 回到你自己的目录，尝试 push，观察被拒绝，然后正确地拉取并合并。

### 练习 2：观察 pull 与 fetch+merge 的差异

1. 使用「同事」目录制造远程的新提交。
2. 回到你自己的目录，先执行：

   ```bash
   git fetch origin
   ```

3. 使用 `git log --oneline --graph --decorate --all` 观察 `origin/main` 与 `main` 的差异。
4. 再执行：

   ```bash
   git merge origin/main
   ```

5. 思考：和直接 `git pull` 相比，这种写法有什么好处？

---

## 六、参考答案（仅供对照）

### 练习 1 参考思路

```bash
# 目录 A：你自己
git clone http://localhost:3000/... playground-me

# 目录 B：同事
git clone http://localhost:3000/... playground-teammate

# 在同事目录中
cd playground-teammate
echo "teammate change" >> teammate.txt
git add teammate.txt
git commit -m "feat: teammate change"
git push origin main

# 回到你的目录
cd ../playground-me
echo "my change" >> me.txt
git add me.txt
git commit -m "feat: my change"
git push origin main        # 这里会被拒绝

git pull origin main        # 拉取并合并
git push origin main        # 再次 push 应该成功
```

### 练习 2 参考思路

```bash
git fetch origin
git log --oneline --graph --decorate --all
# 你会看到 origin/main 在更前面，而 main 还停留在旧提交

git merge origin/main
# 或者 git rebase origin/main （视团队策略而定）
```

> 使用 `fetch + merge` 的好处之一是：你可以在合并前先看清楚远程都改了什么，必要时先在本地开新分支、手动处理复杂情况，而不是一上来就自动合并。

