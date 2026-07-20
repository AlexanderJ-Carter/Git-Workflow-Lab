# 关卡 27：交互式 Rebase 进阶（fixup / squash / autosquash）

**所属阶段**：进阶实用 / 分支协作  
**难度**：🔴 高级  
**预估时间**：40 分钟  
**本关命令关键词**：`git rebase -i`、`fixup`、`squash`、`autosquash`、`reword`

---

> 💡 **学习提示**：本关建立在关卡 06 之上，专注「提交落地前的历史整理」。**切勿对已 push 到共享分支的历史做 rebase。**

---

## 一、本关目标

- [ ] 熟练使用 `git rebase -i HEAD~N` 整理最近 N 个提交
- [ ] 区分 `pick`、`squash`、`fixup`、`reword` 的用途
- [ ] 会用 `fixup!` / `squash!` 前缀 + `--autosquash` 自动排序
- [ ] 牢记：改写已推送历史需 force push，团队协作中要谨慎

**前置知识：** PR 合并前把「fix typo × 5」压成一条清晰 commit，审查者更轻松。

---

## 二、前置条件

- [ ] 已完成关卡 06（rebase 基础）
- [ ] 本地实验环境已启动：`docker compose up -d`
- [ ] 在 `playground-hello` 上练习，且分支**尚未 push** 或仅自己使用：

  ```bash
  cd ~
  git clone http://localhost:3000/playground/playground-hello.git
  cd playground-hello
  git switch -c feature/rebase-fixup-demo
  ```

---

## 三、边看边做：具体步骤

### 步骤 1：制造「 messy 」提交历史

```bash
cd ~/playground-hello
git switch -c feature/rebase-fixup-demo 2>/dev/null || git switch feature/rebase-fixup-demo

echo "step 1" >> REBASE_DEMO.txt && git add REBASE_DEMO.txt && git commit -m "feat(demo): add rebase demo file"
echo "step 2" >> REBASE_DEMO.txt && git add REBASE_DEMO.txt && git commit -m "fix: typo in demo"
echo "step 3" >> REBASE_DEMO.txt && git add REBASE_DEMO.txt && git commit -m "fix: another typo"
echo "step 4" >> REBASE_DEMO.txt && git add REBASE_DEMO.txt && git commit -m "fix: oops again"
git log --oneline -5
```

**预期：** 1 个 feat + 3 个 fix typo，共 4 条提交。

---

### 步骤 2：交互式 rebase — squash 合并

```bash
GIT_SEQUENCE_EDITOR="sed -i '2,4s/^pick/squash/'" git rebase -i HEAD~4
```

若环境不支持上述非交互方式，手动执行：

```bash
git rebase -i HEAD~4
```

在编辑器中将第 2–4 行 `pick` 改为 `squash`（或 `s`），保存退出，在后续编辑器中合并 commit message。

查看结果：

```bash
git log --oneline -3
```

**预期：** 多条 fix 被合并进 feat，历史变短。

---

### 步骤 3：reset 后练习 fixup（保留第一条 message）

重新制造提交：

```bash
git reset --hard HEAD~1 2>/dev/null || git switch main && git branch -D feature/rebase-fixup-demo && git switch -c feature/rebase-fixup-demo

echo "base" >> FIXUP_DEMO.txt && git add FIXUP_DEMO.txt && git commit -m "feat(demo): add fixup demo base"
echo "tweak" >> FIXUP_DEMO.txt && git add FIXUP_DEMO.txt && git commit -m "fixup! feat(demo): add fixup demo base"
echo "tweak2" >> FIXUP_DEMO.txt && git add FIXUP_DEMO.txt && git commit -m "fixup! feat(demo): add fixup demo base"
git log --oneline -4
```

使用 autosquash：

```bash
git rebase -i --autosquash HEAD~3
```

**预期：** 编辑器里 fixup 提交已自动排到目标 feat 下方并标记为 `fixup`。

保存退出后：

```bash
git log --oneline -2
```

**对比 squash：** `fixup` 会丢弃 fixup 提交的 message，只保留目标提交标题。

---

### 步骤 4：reword 修改提交说明

```bash
echo "final" >> FIXUP_DEMO.txt && git add FIXUP_DEMO.txt && git commit -m "chore: tmp bad message"
git rebase -i HEAD~2
```

在编辑器里把最后一行改为 `reword`（或 `r`），保存后在下一个编辑器把 message 改成：

```text
docs(demo): finalize fixup demo with clear message
```

验证：

```bash
git log --oneline -2
```

---

### 步骤 5：已 push 历史的警告（只读演示）

```bash
# 切勿在生产共享分支执行！
# git push --force-with-lease
```

**规则：**

| 场景 | 是否可 rebase -i |
|------|------------------|
| 本地未 push 的 feature | ✅ 推荐 |
| 已 push，仅自己用的分支 | ⚠️ 可以，需 `--force-with-lease` |
| 已 merge 到 main 的提交 | ❌ 不要改 |
| 多人协作的远程分支 | ❌ 禁止 |

---

## 四、如何确认自己做对了

```bash
cd ~/playground-hello
git log --oneline -6
git status
```

- [ ] ✓ 成功用 squash 或 fixup 把多个 typo commit 合并
- [ ] ✓ 使用过 `fixup!` + `--autosquash` 或理解其等价手动操作
- [ ] ✓ 用 `reword` 改过至少一条 commit message
- [ ] ✓ 工作区干净，`git status` 无未提交改动

---

## 五、常见错误与排查

### ❌ 情况 1：rebase 冲突中途卡住

**解决方法：**

```bash
# 解决冲突文件后
git add .
git rebase --continue
# 或放弃
git rebase --abort
```

---

### ❌ 情况 2：`fixup!` 没有自动合并

**可能原因：** 目标标题与 `fixup!` 后缀不完全匹配

**解决方法：** 确保 `fixup! <exact subject of target commit>` 一字不差，或不用 autosquash 手动排序。

---

### ❌ 情况 3：rebase 后 push 被拒绝

**可能原因：** 远程仍有旧历史

**解决方法：** 仅个人分支：`git push --force-with-lease`；共享分支应 `git rebase --abort` 并改用 revert。

---

## 六、扩展练习

- [ ] **练习 1：** 配置 `git config rebase.autoSquash true` 后默认开启 autosquash
- [ ] **练习 2：** 用 `git commit --fixup=<hash>` 代替手写 `fixup!` 标题
- [ ] **练习 3：** 在 PR 合并前 squash 成 1 commit，对比 Gitea 上的 diff 与 commit 列表

---

## 七、下一步

| 上一关 | 下一关 |
|--------|--------|
| [关卡 06：Rebase 基础](./lesson-06-rebase-clean-history.md) | [关卡 28：Blame 与历史考古](./lesson-28-blame-and-archaeology.md) |
