# 关卡 07：误提交到错误分支的补救

**所属阶段**：救火与历史修复
**本关命令关键词**：`git cherry-pick`、`git revert`、`git log`、`git show`

---

## 一、本关目标

- 学会用 `cherry-pick` 把提交"搬运"到正确的分支。
- 学会用 `revert` 安全撤销已推送的提交。
- 理解 `cherry-pick` 和 `revert` 的使用场景区别。
- 避免在团队协作中造成历史混乱。

学完这一关，当你不小心把代码提交到错误的分支，或者需要撤销已经推送的提交时，就不会手忙脚乱了。

---

## 二、前置条件

- 已完成关卡 04（分支基础）和关卡 05（合并冲突）。
- 熟悉 `git log`、`git branch`、`git switch` 的基本操作。
- 有一个干净的练习仓库。

---

## 三、边看边做前先理解的核心概念

### cherry-pick：选择性"摘取"提交

`git cherry-pick` 可以把某个分支上的特定提交"复制"到当前分支。

```bash
git cherry-pick <commit-hash>
```

**使用场景**：
- 误把功能提交到了错误的分支
- 只需要另一个分支的某个特定修复
- 将 hotfix 应用到多个版本分支

### revert：安全撤销提交

`git revert` 会创建一个新提交，内容是"撤销指定提交的变更"。

```bash
git revert <commit-hash>
```

**使用场景**：
- 撤销已推送到共享分支的提交
- 需要"撤销记录"的场景（审计需求）
- 不想改写历史的情况

### 两者的关键区别

| 操作           | 是否改写历史   | 是否适合共享分支 | 产生新提交 |
| -------------- | -------------- | ---------------- | ---------- |
| `cherry-pick`  | 否（复制提交） | 可谨慎使用       | 是         |
| `revert`       | 否             | 是               | 是         |
| `reset --hard` | 是             | **绝对不行**     | 否         |

---

## 四、边看边做：具体步骤

### 场景 1：用 cherry-pick 拯救误提交

假设你本想在 `feature/login` 分支开发登录功能，但不小心在 `main` 分支上提交了。

### 步骤 1：制造"误提交"场景

```bash
# 确保 main 分支是干净的
git switch main
git pull origin main

# 不小心在 main 上开发了功能（错误操作！）
echo "Login feature" > login.py
git add login.py
git commit -m "feat: add login feature"

# 此时发现问题：应该在 feature 分支提交！
git log --oneline -3
# 记住这个提交的 hash，比如 a1b2c3d
```

### 步骤 2：创建正确的分支并 cherry-pick

```bash
# 创建原本应该用的分支
git switch -c feature/login

# 把刚才的提交"摘"过来
git cherry-pick a1b2c3d
# （a1b2c3d 替换为你实际的提交 hash）

# 验证：登录功能已经在正确分支上了
git log --oneline -3
ls login.py
```

### 步骤 3：清理 main 分支上的误提交

现在 `feature/login` 分支已经有了正确的提交，需要从 `main` 上移除错误的那个：

```bash
git switch main
# 因为误提交还没有推送，可以用 reset 移除
git reset --hard HEAD~1

# 验证：main 上没有 login.py 了
git log --oneline -3
ls login.py  # 应该报错：文件不存在
```

### 步骤 4：推送正确的分支

```bash
git switch feature/login
git push -u origin feature/login
```

---

### 场景 2：用 revert 撤销已推送的提交

假设你已经在 `main` 上推送了一个提交，后来发现有问题需要撤销。

### 步骤 5：模拟"已推送"场景

```bash
git switch main
git pull origin main

# 提交并推送（模拟正常开发）
echo "Some feature" > feature.txt
git add feature.txt
git commit -m "feat: add some feature"
git push origin main

# 此时发现问题：这个功能有 Bug，需要撤销！
```

### 步骤 6：用 revert 撤销

因为已经推送了，不能使用 `reset`（会改写历史），要用 `revert`：

```bash
# 先查看要撤销的提交
git log --oneline -3
# 找到那个提交的 hash，比如 x1y2z3a

# 执行 revert
git revert x1y2z3a
# 会打开编辑器让你编辑 revert 提交信息，保存即可
```

### 步骤 7：观察 revert 的效果

```bash
# 查看历史
git log --oneline -5
# 你会看到一个新的 "revert" 提交

# 查看文件状态
ls feature.txt  # 文件不存在了，因为被撤销了

# 推送这个撤销操作
git push origin main
```

在 Gitea 上查看，你会看到历史中有两条提交：
1. 原来的 `feat: add some feature`
2. 新的 `Revert "feat: add some feature"`

这就是 `revert` 的"留痕"特性——撤销但不抹除历史。

---

### 场景 3：cherry-pick 多个提交

### 步骤 8：批量 cherry-pick

```bash
# 创建一个分支做多个提交
git switch -c feature/multi-commits

echo "A" > a.txt && git add a.txt && git commit -m "feat: add A"
echo "B" > b.txt && git add b.txt && git commit -m "feat: add B"
echo "C" > c.txt && git add c.txt && git commit -m "feat: add C"

# 查看提交历史，记录三个提交的 hash
git log --oneline -3
# 比如：abc1111 (C), abc2222 (B), abc3333 (A)

# 切回 main，只想要 B 和 C
git switch main

# cherry-pick 一个范围（不包含起点，包含终点）
git cherry-pick abc2222..abc1111

# 或者逐个 cherry-pick
# git cherry-pick abc2222
# git cherry-pick abc1111

# 验证
ls  # 应该有 b.txt 和 c.txt，但没有 a.txt
```

---

### 场景 4：处理 cherry-pick 冲突

### 步骤 9：制造 cherry-pick 冲突

```bash
git switch main

# 在 main 上添加内容
echo "Main version" > conflict.txt
git add conflict.txt
git commit -m "add conflict.txt on main"
git push origin main

# 创建分支并修改同一文件
git switch -c feature/conflict-cp
echo "Feature version" > conflict.txt
git add conflict.txt
git commit -m "modify conflict.txt on feature"

# 切回 main，尝试 cherry-pick
git switch main
git cherry-pick <feature分支上的那个提交hash>
# 会报冲突！
```

### 步骤 10：解决 cherry-pick 冲突

```bash
# 查看状态
git status

# 打开冲突文件，会看到冲突标记
# <<<<<<< HEAD
# Main version
# =======
# Feature version
# >>>>>>> ...

# 手动解决冲突
echo "Resolved version" > conflict.txt
git add conflict.txt

# 继续 cherry-pick
git cherry-pick --continue
```

如果想放弃这次 cherry-pick：

```bash
git cherry-pick --abort
```

---

## 五、如何确认自己做对了

### cherry-pick 验证

- 目标分支上有了正确的提交内容。
- 原分支的历史没有被破坏。
- 文件内容符合预期。

### revert 验证

- 历史中保留了原提交和 revert 提交。
- 代码确实被"撤销"了。
- `git push` 成功，没有因为历史问题报错。

---

## 六、练习题

### 练习 1：完整演练 cherry-pick 流程

1. 在 `main` 上创建一个提交（模拟误提交）。
2. 用 `cherry-pick` 把它移到 `feature/fix` 分支。
3. 从 `main` 上移除误提交（用 `reset`）。
4. 验证两个分支的状态都正确。

### 练习 2：revert vs reset 对比

1. 在 `main` 上创建并推送一个提交。
2. 尝试用 `git reset --hard HEAD~1` 撤销，然后 `git push`（观察会发生什么）。
3. 恢复后，改用 `git revert` 撤销并推送。
4. 对比两种方式的区别和后果。

### 练习 3：选择性 cherry-pick

1. 在 `feature` 分支上创建 5 个提交。
2. 只 cherry-pick 其中第 2 和第 4 个到 `main`。
3. 观察 `main` 上的历史和文件状态。

---

## 七、参考答案（仅供对照）

### 练习 1 参考思路

```bash
# 1. 在 main 上误提交
git switch main
echo "Oops" > oops.txt
git add oops.txt
git commit -m "feat: oops commit"
HASH=$(git rev-parse HEAD)

# 2. cherry-pick 到正确分支
git switch -c feature/fix
git cherry-pick $HASH

# 3. 从 main 移除
git switch main
git reset --hard HEAD~1

# 4. 验证
git log --oneline feature/fix  # 应该有那个提交
git log --oneline main          # 应该没有那个提交
```

### 练习 2 参考思路

```bash
# 1. 创建并推送
git switch main
echo "Test" > test.txt
git add test.txt
git commit -m "test commit"
git push origin main
HASH=$(git rev-parse HEAD)

# 2. 用 reset --hard
git reset --hard HEAD~1
git push origin main
# 报错：! [rejected] ... (non-fast-forward)

# 需要用 force push，但这很危险！
# git push --force origin main  # 不推荐

# 3. 恢复：先把 main 弄回来
git reset --hard $HASH
git push origin main

# 4. 用 revert
git revert $HASH
git push origin main
# 成功！且历史中有撤销记录
```

### 练习 3 参考思路

```bash
# 创建 5 个提交
git switch -c feature/multi
for i in {1..5}; do
  echo "File $i" > file$i.txt
  git add file$i.txt
  git commit -m "feat: add file $i"
done

# 查看提交 hash
git log --oneline -5
# 假设是：e1111 (file5), e2222 (file4), e3333 (file3), e4444 (file2), e5555 (file1)

# 只 cherry-pick 第 2 和第 4 个
git switch main
git cherry-pick e4444  # file2
git cherry-pick e2222  # file4

# 验证
ls  # 应该只有 file2.txt 和 file4.txt
```

---

## 八、常见错误与排查

### 问题 1：cherry-pick 时提示"空提交"

```text
The previous cherry-pick is now empty, possibly due to a conflict resolution.
```

**原因**：cherry-pick 的变更已经在当前分支存在了。

**解决**：确认是否真的需要这次 cherry-pick，如果不需要，用 `git cherry-pick --abort` 放弃。

### 问题 2：revert 时遇到冲突

有时候 revert 也会冲突（如果后续提交修改了同一行）。

**解决**：手动解决冲突后 `git revert --continue`，或 `git revert --abort` 放弃。

### 问题 3：cherry-pick 了错误的提交

如果 cherry-pick 完发现选错了提交：

```bash
# 还没 push，用 reset 撤销
git reset --hard HEAD~1

# 已经 push 了，用 revert 撤销
git revert HEAD
```

---

## 九、最佳实践总结

| 场景                       | 推荐操作                | 原因             |
| -------------------------- | ----------------------- | ---------------- |
| 误提交到本地分支，未推送   | `cherry-pick` + `reset` | 可以改写本地历史 |
| 误提交已推送到共享分支     | `revert`                | 不改写历史，安全 |
| 只需要另一个分支的某个修复 | `cherry-pick`           | 选择性应用       |
| hotfix 需要应用到多个版本  | `cherry-pick`           | 逐个版本应用     |
| 需要撤销但保留记录（审计） | `revert`                | 历史可追溯       |

---

## 十、延伸阅读

- `git cherry-pick --no-commit`：只应用变更，不创建提交
- `git revert -n`：撤销变更但不自动提交
- `git revert -m 1`：撤销合并提交时的模式选择
