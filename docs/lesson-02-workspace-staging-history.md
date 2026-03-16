# 关卡 02：搞懂工作区 / 暂存区 / 提交历史

**所属阶段**：Git 基础操作实验  
**本关命令关键词**：`git status`、`git diff`、`git add`、`git restore`、`git log`

---

## 一、本关目标与场景

- 分清楚「工作区」「暂存区」「本地提交历史」分别是什么。
- 看得懂 `git status` 的输出，知道当前处于什么状态。
- 会用 `git diff` 对比修改，会把想提交的内容精确地放进暂存区。
- 懂得如何在提交前撤销/恢复修改。

**典型真实场景**：

- 你在一个功能分支上改了半天，结果发现同一个文件里既有「想提交」的改动，也有「只是实验一下」的改动；
- 或者你改着改着发现方向不对了，想整体回到上一次 commit 的状态，却又不确定会不会丢东西。

学完这一关，你在日常开发时，遇到「改乱了」「不知道该不该 commit」时就不会慌。

---

## 二、前置条件

- 已完成 **关卡 01：新建仓库并 push 代码**。
- 本地已经 clone 了 `playground-hello` 仓库，并能正常 `git status`。

建议在本关前，先确保工作区是干净的（`git status` 提示 `nothing to commit, working tree clean`）。

---

## 三、边看边做：具体步骤

> 建议：左边打开本文件，右边同时打开 Gitea 网页 + 本地终端，按照步骤逐条执行。

### 步骤 1：制造一些修改

在 `playground-hello` 目录下，编辑 `README.md`，随便加几行内容，例如：

```markdown
## 今日练习

- 理解工作区 / 暂存区 / 提交历史
```

然后在终端查看状态：

```bash
git status
```

观察输出，注意：

- 哪些文件被标记为「modified」？
- 它们现在属于哪一块：工作区 / 暂存区 / 提交历史？

### 步骤 2：查看修改内容

使用 `git diff` 查看当前修改：

```bash
git diff
```

你应该能看到刚才在 `README.md` 中增加的几行内容。

### 步骤 3：把修改加入暂存区

把修改加入暂存区：

```bash
git add README.md
git status
```

思考：

- 此时 `git status` 中，`README.md` 出现在了哪个区域？
- 再执行 `git diff` / `git diff --cached` 分别看到的是什么？

> 小提示：  
> - `git diff` 默认对比「工作区 vs 暂存区」。  
> - `git diff --cached` 对比「暂存区 vs 最近一次提交」。

### 步骤 4：撤回暂存区 / 工作区的修改

先模拟一个「暂存错了文件」的场景：

```bash
echo "temp line" >> README.md
git add README.md
git status
```

现在我们既有想要的改动，也有不想要的改动，都在暂存区里了。

试试撤回暂存区中的文件：

```bash
git restore --staged README.md
git status
```

观察：

- 文件又回到了「工作区已修改」状态。

如果你想**完全丢弃工作区的修改**（危险操作，慎用，但在练习环境里可以多试）：

```bash
git restore README.md
git status
```

确认修改确实回到了之前的提交版本。

### 步骤 5：完成一次干净的提交

再次往 `README.md` 中加入你真正想要的内容，然后：

```bash
git add README.md
git commit -m "docs: add practice notes"
git log --oneline -5
```

你应该能在 `git log` 中看到刚刚这条新的提交。

---

## 四、如何确认自己做对了

- 在终端中：
  - 你能通过 `git status` 清楚知道当前是「干净」「有修改未暂存」「有修改已暂存」中的哪一种状态。
  - 你能用 `git diff` / `git diff --cached` 分别查看「工作区 vs 暂存区」「暂存区 vs 最近提交」的差异。
  - 你知道如何用 `git restore` / `git restore --staged` 撤销不小心的操作。
- 在 Gitea Web 界面：
  - 刷新仓库页面，确认最新的提交已经同步（如果你 `git push` 了）。

---

## 五、练习题

> 建议自己先尝试完成，下面有参考答案。也可以当成小测验来做。

### 练习 1：只提交文件的一部分修改

1. 在同一个文件中做两处不相关的修改。
2. 使用 `git add -p`，只把其中一处改动加入暂存区，另一处保持在工作区。
3. 提交后，观察：
   - 提交记录中包含了哪一部分修改？
   - 另外一部分修改还在工作区吗？

### 练习 2：恢复到某次提交时的文件状态（不改动历史）

1. 找到之前某次提交的哈希（使用 `git log --oneline`）。
2. 把当前工作区的某个文件内容恢复成那次提交的版本，但**不改动提交历史**。
3. 提交这次修改。

### 练习 3（选择题）：判断当前修改在哪一块

假设你在某个仓库里执行了下面一系列命令：

```bash
echo "line A" >> demo.txt
git add demo.txt
echo "line B" >> demo.txt
```

此时，关于 `line A` 和 `line B` 的状态，下列哪一项描述是正确的？

A. `line A` 在工作区，`line B` 在暂存区  
B. `line A` 在暂存区，`line B` 在工作区  
C. `line A` 和 `line B` 都在暂存区  
D. `line A` 和 `line B` 都在工作区  

> 可以先自己画一张「三层结构」小草图，再对照 `git diff` / `git diff --cached` 的输出来判断。

---

## 六、参考答案（仅供对照）

### 练习 1 参考思路

```bash
# 在同一个文件里做两处修改
git add -p README.md           # 按提示选择要加入暂存区的 hunk
git status                     # 确认部分修改在暂存区，部分还在工作区
git commit -m "partial change"
git diff                       # 看看剩余修改是否还在工作区
```

### 练习 2 参考思路

```bash
git log --oneline              # 找到目标提交，例如 abc1234
git restore --source=abc1234 README.md
git status                     # README.md 显示为修改状态
git commit -am "chore: restore README to abc1234 version"
```

> 注意：这里我们没有用 `git reset` 去改动历史，而是通过 `restore --source` 把旧版本的内容「拷贝」到当前工作区，形成一次新的提交。

### 练习 3 参考答案

- 正确选项：**B**  
  - `line A` 在执行 `git add demo.txt` 时已经进入了暂存区；  
  - 之后追加的 `line B` 还停留在工作区，没有被加入暂存区。  
  - 可以通过：

```bash
git diff            # 只看到 line B 相关的改动
git diff --cached   # 只看到 line A 相关的改动
```

来验证自己的判断。

