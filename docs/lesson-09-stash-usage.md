# 关卡 09：stash 的正确使用姿势

**所属阶段**：救火与历史修复
**本关命令关键词**：`git stash`、`git stash pop`、`git stash list`、`git stash drop`、`git stash apply`

---

## 一、本关目标

- 学会用 `stash` 临时保存工作进度。
- 理解 `stash` 的适用场景和最佳实践。
- 掌握多个 stash 的管理和选择性恢复。
- 处理 stash 过程中可能遇到的冲突。

学完这一关，当你正在开发功能时突然需要切换分支处理紧急问题，就能从容应对了。

---

## 二、前置条件

- 已完成关卡 02（工作区/暂存区）。
- 熟悉 `git status`、`git add`、`git commit` 的基本操作。
- 理解工作区和暂存区的区别。

---

## 三、核心概念

### 什么是 stash？

`stash` 是 Git 的"临时抽屉"，可以把当前工作区和暂存区的修改暂时存起来，让工作区恢复干净状态。

```bash
git stash
```

这个命令会：
1. 保存工作区和暂存区的修改
2. 把工作区恢复到 HEAD（最后一次提交）的状态
3. 你可以随时把保存的内容"取出来"

### stash 与 commit 的区别

| 对比项 | stash | commit |
|--------|-------|--------|
| 目的 | 临时保存 | 永久记录 |
| 是否创建提交 | 否 | 是 |
| 是否影响历史 | 否 | 是 |
| 适用场景 | 临时中断、切换分支 | 完成一个逻辑单元 |

### stash 的典型场景

1. **紧急切换**：正在开发，突然要切换分支处理紧急 Bug
2. **临时验证**：想在一个干净环境下测试某个改动
3. **暂存探索**：写了一些实验代码，不确定要不要提交

---

## 四、边看边做：具体步骤

### 步骤 1：创建一个"被打断"的场景

```bash
git switch main

# 创建一个新分支进行开发
git switch -c feature/new-ui

# 正在开发中...
echo "New UI component" > ui.html
echo "Some styling" > style.css

# 添加到暂存区
git add ui.html

# style.css 还在工作区，未暂存
git status
```

此时状态：
- `ui.html` 在暂存区
- `style.css` 在工作区（未跟踪）

### 步骤 2：紧急情况来了，需要切换分支

```bash
# 假设老板让你立刻去修一个紧急 Bug
# 你想切换到 main 分支，但当前有未提交的修改

git switch main
# 报错：error: Your local changes would be overwritten by checkout
# Git 不让你切换，因为有未提交的修改
```

### 步骤 3：用 stash 保存当前工作

```bash
# 回到开发分支
git switch feature/new-ui

# 使用 stash 保存当前工作
git stash push -m "WIP: new UI development"

# 或者简写
git stash
```

查看状态：

```bash
git status
# working tree clean

ls
# ui.html 和 style.css 都不见了（被存到 stash 里了）
```

### 步骤 4：处理紧急任务

```bash
# 现在可以自由切换分支了
git switch main

# 创建 hotfix 分支
git switch -c hotfix/urgent-bug

# 修复 Bug
echo "Bug fixed" > bugfix.txt
git add bugfix.txt
git commit -m "fix: urgent bug"

# 合并回 main
git switch main
git merge hotfix/urgent-bug

# 删除 hotfix 分支
git branch -d hotfix/urgent-bug
```

### 步骤 5：恢复之前的工作

```bash
# 回到开发分支
git switch feature/new-ui

# 查看有哪些 stash
git stash list
# 输出类似：stash@{0}: WIP: new UI development

# 恢复最近的 stash
git stash pop

# 验证
git status
ls
# ui.html 和 style.css 都回来了！
```

---

## 五、stash 的高级用法

### 多个 stash 的管理

### 步骤 6：创建多个 stash

```bash
# 继续在 feature/new-ui 分支工作
echo "More UI work" >> ui.html

# 存第一个 stash
git stash push -m "UI work round 1"

# 再做一些修改
echo "Even more work" >> style.css

# 存第二个 stash
git stash push -m "Style updates"

# 查看 stash 列表
git stash list
```

输出类似：

```text
stash@{0}: On feature/new-ui: Style updates
stash@{1}: On feature/new-ui: UI work round 1
```

### 步骤 7：选择性恢复 stash

```bash
# 恢复特定的 stash（不是最近的）
git stash apply stash@{1}

# 或者用 pop（恢复并删除 stash）
git stash pop stash@{1}
```

`apply` vs `pop`：
- `apply`：恢复但不删除 stash 记录
- `pop`：恢复并删除 stash 记录

### 步骤 8：删除 stash

```bash
# 删除特定的 stash
git stash drop stash@{0}

# 删除所有 stash
git stash clear

# 谨慎使用！删除后无法恢复
```

---

## 六、处理 stash 冲突

### 步骤 9：制造 stash 冲突场景

```bash
# 准备环境
git switch main
git switch -c conflict-stash

# 创建并提交一个文件
echo "Original content" > conflict.txt
git add conflict.txt
git commit -m "add conflict.txt"

# 修改文件
echo "Stash content" > conflict.txt
git stash push -m "stashed changes"

# 切回 main，修改同一文件
git switch main
echo "Main content" > conflict.txt
git add conflict.txt
git commit -m "modify conflict.txt on main"

# 切回分支，尝试恢复 stash
git switch conflict-stash
git stash pop
# 冲突！
```

### 步骤 10：解决 stash 冲突

```bash
# 查看状态
git status
# Both modified: conflict.txt

# 查看冲突内容
cat conflict.txt
# <<<<<<< Updated upstream
# Main content
# =======
# Stash content
# >>>>>>> Stashed changes

# 手动解决冲突
echo "Resolved content" > conflict.txt
git add conflict.txt

# stash pop 后冲突解决会自动完成
# 如果用 apply，可能需要手动 drop
git stash drop
```

---

## 七、stash 与未跟踪文件

### 步骤 11：stash 包含未跟踪文件

默认情况下，`git stash` **不会**保存未跟踪的文件（新建的文件）。

```bash
# 创建一个新文件（未跟踪）
echo "New file" > newfile.txt

git status
# Untracked files: newfile.txt

# 普通 stash
git stash
git status
# newfile.txt 还在！没有被 stash

# 恢复刚才的 stash
git stash pop
```

要包含未跟踪文件，使用 `-u` 或 `--include-untracked`：

```bash
# 包含未跟踪文件的 stash
git stash push -u -m "include untracked files"

git status
# working tree clean
# newfile.txt 也不见了

# 恢复
git stash pop
ls newfile.txt  # 文件回来了
```

---

## 八、查看 stash 内容

### 步骤 12：检查 stash 内容

```bash
# 查看某个 stash 的详细信息
git stash show stash@{0}

# 查看详细差异
git stash show -p stash@{0}

# 从 stash 创建分支
git stash branch from-stash stash@{0}
# 这会创建一个新分支并应用 stash
```

---

## 九、如何确认自己做对了

- 用 `git stash` 能成功保存当前修改。
- 用 `git stash list` 能看到保存的 stash 记录。
- 用 `git stash pop` 能恢复之前保存的修改。
- 能处理 stash 冲突。
- 理解了 `apply` 和 `pop` 的区别。

---

## 十、练习题

### 练习 1：完整的 stash 工作流

1. 在 `feature` 分支上做修改（暂存区和工作区都有）。
2. 使用 stash 保存。
3. 切换到 `main`，做一个提交。
4. 切回 `feature`，恢复 stash。
5. 验证所有修改都回来了。

### 练习 2：多个 stash 的管理

1. 创建 3 个不同的 stash（每个带不同消息）。
2. 查看 stash 列表。
3. 选择性恢复中间那个 stash。
4. 删除其他两个 stash。

### 练习 3：处理 stash 冲突

1. 创建文件，stash 修改。
2. 在当前分支继续提交，修改同一文件。
3. 恢复 stash，解决冲突。

---

## 十一、参考答案（仅供对照）

### 练习 1 参考思路

```bash
# 1. 创建修改
git switch -c feature/stash-practice
echo "Staged" > staged.txt && git add staged.txt
echo "Unstaged" >> staged.txt

# 2. stash 保存
git stash push -m "practice stash"

# 3. 切换分支提交
git switch main
echo "Main work" > mainwork.txt && git add mainwork.txt && git commit -m "main work"

# 4. 恢复 stash
git switch feature/stash-practice
git stash pop

# 5. 验证
git status
cat staged.txt  # 两个修改都在
```

### 练习 2 参考思路

```bash
# 1. 创建 3 个 stash
echo "A" > a.txt && git stash push -m "stash A"
echo "B" > b.txt && git stash push -m "stash B"
echo "C" > c.txt && git stash push -m "stash C"

# 2. 查看列表
git stash list
# stash@{0}: stash C
# stash@{1}: stash B
# stash@{2}: stash A

# 3. 恢复中间的
git stash apply stash@{1}
ls b.txt  # 存在

# 4. 删除其他
git stash drop stash@{0}
git stash drop stash@{1}  # 注意：删除后索引会变化
# 或者 git stash clear 一次性清空
```

### 练习 3 参考思路

```bash
# 1. 创建并 stash
echo "Original" > conflict.txt && git add conflict.txt && git commit -m "original"
echo "Stash version" > conflict.txt
git stash push -m "conflict stash"

# 2. 修改同一文件
echo "New version" > conflict.txt
git add conflict.txt && git commit -m "new version"

# 3. 恢复并解决冲突
git stash pop
# 冲突！
cat conflict.txt
# <<<<<<< Updated upstream
# New version
# =======
# Stash version
# >>>>>>> Stashed changes

echo "Resolved" > conflict.txt
git add conflict.txt
git stash drop
```

---

## 十二、常见问题与排查

### 问题 1：stash 后部分文件还在

**原因**：未跟踪的文件默认不会被 stash。

**解决**：使用 `git stash -u` 包含未跟踪文件。

### 问题 2：stash pop 失败，提示冲突

**原因**：stash 的内容与当前分支有冲突。

**解决**：手动解决冲突后 `git add`，必要时 `git stash drop`。

### 问题 3：误删了 stash

**解决**：

```bash
# stash 被删除后，数据可能还在 reflog 中
git fsck --lost-found
# 查找 "dangling commit"

# 找到后可以用 cherry-pick 恢复
```

### 问题 4：想只 stash 某个文件

```bash
# 只 stash 特定文件
git stash push -m "partial stash" -- path/to/file.txt
```

---

## 十三、最佳实践总结

| 场景 | 推荐命令 |
|------|---------|
| 临时保存工作 | `git stash push -m "message"` |
| 恢复并删除 stash | `git stash pop` |
| 恢复但保留 stash | `git stash apply` |
| 包含未跟踪文件 | `git stash -u` |
| 只 stash 部分文件 | `git stash push -- <path>` |
| 查看 stash 详情 | `git stash show -p` |
| 从 stash 创建分支 | `git stash branch <name>` |

### 建议

1. **加消息**：用 `-m` 给 stash 添加描述，方便日后识别。
2. **及时清理**：不用的 stash 及时 `drop`，避免列表混乱。
3. **不要长期依赖**：stash 是临时的，重要工作还是要提交到分支。
4. **注意冲突**：stash 恢复时可能冲突，要有心理准备。

---

## 十四、延伸阅读

- `git stash --keep-index`：只 stash 未暂存的修改
- `git stash -p`：交互式选择要 stash 的内容
- `git stash create`：创建 stash 但不存储（高级用法）
