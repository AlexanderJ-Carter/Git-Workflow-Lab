# 关卡 23：Pull Request 与代码审查实践

**所属阶段**：工程化 / 分支协作  
**难度**：🟡 进阶  
**预估时间**：35 分钟  
**本关命令关键词**：`git switch`、`git push`、`git diff`、`git log`

---

> 💡 **学习提示**：本关在 Gitea Web 界面完成 PR 流程，终端负责推送分支。教程站点：http://localhost:8081

---

## 一、本关目标

- [ ] 能在 Gitea 上从 `playground-hello` 功能分支发起 Pull Request
- [ ] 知道审查时要看的四件事：diff 范围、测试/CI、改动 scope、提交信息
- [ ] 能在 PR 上留下行内评论（ mentally 模拟 approve / request changes）
- [ ] 理解「小 PR、清晰描述、可审查 diff」的协作习惯

**前置知识：** 完成本关后，你能以审查者视角读 diff，而不只是「点合并」。

---

## 二、前置条件

- [ ] 已完成关卡 04（分支与 PR）和关卡 22（约定式提交）
- [ ] 本地实验环境已启动：`docker compose up -d`
- [ ] 可访问 http://localhost:3000（Gitea）、http://localhost:8080（终端）
- [ ] 已 clone `playground-hello`：

  ```bash
  cd ~
  git clone http://localhost:3000/playground/playground-hello.git
  cd playground-hello
  ```

---

## 三、边看边做：具体步骤

### 步骤 1：创建审查友好的功能分支

```bash
cd ~/playground-hello
git switch main
git pull origin main 2>/dev/null || true
git switch -c feature/review-demo
```

---

### 步骤 2：做一小步、可审查的改动

只改 README，保持 diff 小而清晰：

```bash
cat >> README.md << 'EOF'

## Code Review 练习

- 本段由 feature/review-demo 分支添加
- PR 描述应说明「为什么改」而不只是「改了什么」
EOF

git add README.md
git commit -m "docs: add code review practice section"
```

**预期：** 单次 commit，单文件，便于审查。

---

### 步骤 3：推送并在 Gitea 开 PR

```bash
git push -u origin feature/review-demo
```

在浏览器打开 http://localhost:3000 ，进入 `playground/playground-hello`：

1. 点击 **Pull Requests** → **New Pull Request**
2. Base：`main`，Compare：`feature/review-demo`
3. 标题示例：`docs: add code review practice section`
4. 描述模板（填写后提交）：

   ```markdown
   ## 变更说明
   添加 Code Review 练习段落，配合关卡 23。

   ## 审查清单
   - [ ] diff 仅涉及 README
   - [ ] 提交信息符合约定式提交
   - [ ] 无无关文件
   ```

---

### 步骤 4：以审查者身份检查 diff

在 PR 页面打开 **Files changed**，逐项核对：

| 检查项 | 看什么 | 本练习预期 |
|--------|--------|------------|
| **范围** | 是否混入无关重构/格式化 | 仅 README |
| **逻辑** | 改动是否符合 PR 描述 | 段落与描述一致 |
| **测试/CI** | 是否破坏构建（本仓库可看 Actions） | 文档改动，CI 应通过 |
| **提交历史** | commit message 是否可读 | `docs: ...` |

在终端本地复核：

```bash
git fetch origin
git diff origin/main...origin/feature/review-demo --stat
git log origin/main..origin/feature/review-demo --oneline
```

**预期输出示例：**

```text
 README.md | 5 +++++
 1 file changed, 5 insertions(+)
```

```text
abc1234 docs: add code review practice section
```

---

### 步骤 5：留下审查评论（行内）

在 Gitea PR 的 diff 视图中：

1. 点击 README 新增行旁的 **+** 号
2. 评论示例：`建议：可以加一句「本关配合 lesson-23 使用」方便学习者定位`
3. 状态选择 **Comment**（本环境若无多人账号， mentally 记为「Request changes」或「Approve」）

**审查者心态：**

- **Approve**：改动正确、范围合理、可合并
- **Request changes**：有问题需作者修复后再合并
- **Comment**：建议性意见，不阻塞合并

---

### 步骤 6：作者响应并合并

若有评论，在本地修改后追加提交：

```bash
# 可选：响应审查意见
sed -i 's/本段由/本段（lesson-23）由/' README.md
git add README.md
git commit -m "docs: address review feedback on lesson reference"
git push origin feature/review-demo
```

回到 Gitea PR 页面，确认 diff 更新后点击 **Merge Pull Request**（选 merge commit 或 squash 均可，本练习重点在流程）。

合并后本地同步：

```bash
git switch main
git pull origin main
git log --oneline -3
```

---

## 四、如何确认自己做对了

```bash
cd ~/playground-hello
git branch -a | grep review-demo
git log --oneline -5
git diff origin/main~1 origin/main --stat 2>/dev/null || git log --oneline -1
```

- [ ] ✓ Gitea 上 PR 状态为 **Merged**
- [ ] ✓ `main` 分支包含 `Code Review 练习` 段落
- [ ] ✓ PR 描述中有审查清单
- [ ] ✓ 你在 diff 上至少留过 1 条行内评论（或 mentally 完成 approve 流程）

---

## 五、常见错误与排查

### ❌ 情况 1：PR 包含几十个文件、难以审查

**可能原因：** 分支长期未同步 main，或混入了格式化全仓库

**解决方法：**

```bash
git switch feature/review-demo
git fetch origin
git rebase origin/main   # 或 merge origin/main
# 拆 commit、去掉无关改动后再 push
```

---

### ❌ 情况 2：PR 描述为空或只写「update」

**可能原因：** 审查者不知道意图和风险

**解决方法：** 用「背景 → 改动 → 如何验证 → 风险」四段式写描述。

---

### ❌ 情况 3：没看 CI 就合并

**可能原因：** 文档改动也可能触发 workflow 失败

**解决方法：** 合并前确认 PR 页 Actions / Checks 为绿色；失败时看日志（关卡 11）。

---

## 六、扩展练习

- [ ] **练习 1：** 故意在 PR 里多改一个无关文件，自检 diff 时能否立刻发现
- [ ] **练习 2：** 用 `git diff main...feature/review-demo` 在合并前本地审查
- [ ] **练习 3：** 在 `playground-ci` 开一个小 PR，审查 `.gitea/workflows` 或 workflow 文件改动

---

## 七、下一步

| 上一关 | 下一关 |
|--------|--------|
| [关卡 22：约定式提交](./lesson-22-conventional-commits.md) | [关卡 24：Fork 与 upstream](./lesson-24-fork-and-upstream.md) |
