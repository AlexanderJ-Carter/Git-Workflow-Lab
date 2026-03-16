# 关卡 06b：远程协作规则与常见约定

**所属阶段**：分支与协作
**本关关键词**：分支命名规范、PR/MR 流程、Code Review、Git Flow、GitHub Flow、强推危害

---

## 一、本关目标

- 掌握常见的分支命名规范和含义。
- 理解 Pull Request / Merge Request 的最佳实践。
- 了解主流 Git 工作流（Git Flow、GitHub Flow）。
- 明白为什么**绝对不要对共享分支强制推送**。

学完这一关，你就能在团队协作中遵循"行规"，避免踩坑。

---

## 二、前置条件

- 已完成关卡 04（分支与 PR）和关卡 05（合并冲突）。
- 熟悉 `git push`、`git pull`、`git merge` 的基本操作。
- 在 Gitea 上有创建和合并 PR 的经验。

---

## 三、边看边做前先理解的分支命名规范

### 常见的分支前缀

| 前缀        | 用途               | 示例                        |
| ----------- | ------------------ | --------------------------- |
| `feature/`  | 新功能开发         | `feature/user-auth`         |
| `bugfix/`   | 修复 Bug           | `bugfix/login-error`        |
| `hotfix/`   | 紧急线上修复       | `hotfix/security-patch`     |
| `release/`  | 发布准备           | `release/v1.2.0`            |
| `docs/`     | 文档更新           | `docs/api-reference`        |
| `refactor/` | 代码重构           | `refactor/user-service`     |
| `test/`     | 测试相关           | `test/integration-tests`    |
| `chore/`    | 杂项（依赖更新等） | `chore/update-dependencies` |

### 命名最佳实践

1. **简短但有意义**：`feature/add-login` 比 `feature/add-a-login-page-for-users` 更好
2. **使用连字符分隔**：`feature/user-auth` 而不是 `feature/userAuth` 或 `feature_user_auth`
3. **包含 Issue 编号**（可选）：`feature/user-auth-#123`
4. **避免使用特殊字符**：不要用空格、中文、`@`、`#` 等

### 步骤 1：按规范创建分支

```bash
# 假设要开发用户登录功能
git switch main
git pull origin main
git switch -c feature/user-login

# 假设要修复一个登录 Bug
git switch main
git switch -c bugfix/login-timeout-#42

# 假设要做紧急线上修复
git switch main
git switch -c hotfix/critical-security-fix
```

---

## 四、Pull Request / Merge Request 规范

### PR 标题规范

使用类似"约定式提交"的格式：

```
<类型>: <简短描述>
```

常见类型：

| 类型       | 用途                   |
| ---------- | ---------------------- |
| `feat`     | 新功能                 |
| `fix`      | Bug 修复               |
| `docs`     | 文档变更               |
| `style`    | 代码格式（不影响逻辑） |
| `refactor` | 重构                   |
| `test`     | 测试相关               |
| `chore`    | 构建/工具/依赖         |

**示例**：

- `feat: add user login page`
- `fix: resolve login timeout issue`
- `docs: update API documentation`
- `refactor: extract user service`

### PR 描述模板

一个完整的 PR 描述应该包含：

```markdown
## 变更内容
<!-- 简要描述这个 PR 做了什么 -->

## 相关 Issue
<!-- 关联的 Issue 编号，如 Closes #123 -->
Closes #42

## 变更类型
- [ ] 新功能
- [ ] Bug 修复
- [ ] 重构
- [ ] 文档更新
- [ ] 其他：___

## 测试情况
<!-- 描述如何测试这些变更 -->

## 截图（如适用）
<!-- UI 变更的截图 -->

## 检查清单
- [ ] 代码已自测
- [ ] 已添加必要注释
- [ ] 已更新相关文档
```

### 步骤 2：创建一个规范的 PR

在 Gitea 上创建 PR 时：

1. **标题**：使用规范格式，如 `feat: add user login page`
2. **描述**：填写变更内容、关联 Issue、测试情况
3. **审查者**：指派合适的 Reviewer
4. **标签**：添加类型标签（feature/bug/documentation 等）

---

## 五、Code Review 基本礼仪

### 提交者应该做的

1. **PR 粒度适中**：一个 PR 只做一件事，不要"大杂烩"
2. **自测后再提交**：确保 CI 通过、功能正常
3. **及时响应评论**：认真对待每个 Review 意见
4. **保持耐心**：Review 是为了代码质量，不是针对个人

### Reviewer 应该做的

1. **及时 Review**：不要让 PR 积压太久
2. **评论要具体**：说清楚问题在哪里、怎么改进
3. **区分建议和必须**：用"建议"、"必须"、"Nit"（小问题）区分
4. **保持友善**：对事不对人

### 常见的 Review 评论示例

```markdown
# 必须修改的问题
**必须**：这里存在空指针风险，请添加判空检查。

# 建议性意见
**建议**：这个方法可以提取成工具类，方便复用。

# 小问题（非阻塞）
**Nit**：这个变量名可以更具描述性。

# 认可
LGTM (Looks Good To Me)
```

---

## 六、主流 Git 工作流

### GitHub Flow（推荐入门）

最简单的工作流，适合持续部署的场景：

1. `main` 分支永远可部署
2. 从 `main` 创建功能分支
3. 开发完成后创建 PR
4. Review 通过后合并到 `main`
5. 合并后立即部署

```
main ────●────●────●────●────→
         \    /
feature ──●──●──●
```

### Git Flow（复杂项目）

适合有明确发布周期的项目：

- `main`：生产环境代码
- `develop`：开发主分支
- `feature/*`：功能分支
- `release/*`：发布准备
- `hotfix/*`：紧急修复

```
main ──────────●─────────────●──→
               \           /
release ────────●─────────●
                 \       /
develop ──●──●──●──●──●──●──●──→
         /           \
feature ─●──●──●
```

### 步骤 3：在团队中模拟 GitHub Flow

假设你们团队要开发一个新功能：

```bash
# 1. 从 main 创建功能分支
git switch main
git pull origin main
git switch -c feature/new-dashboard

# 2. 开发并提交
echo "Dashboard content" > dashboard.html
git add dashboard.html
git commit -m "feat: add dashboard page"

# 3. 推送到远程
git push -u origin feature/new-dashboard

# 4. 在 Gitea 上创建 PR
# （通过 Web 界面操作）

# 5. Review 通过后合并 PR
# （通过 Web 界面或命令行）

# 6. 删除已合并的功能分支
git switch main
git pull origin main
git branch -d feature/new-dashboard
git push origin --delete feature/new-dashboard
```

---

## 七、为什么不能对共享分支强制推送

### 危险场景演示

假设团队有两个人：Alice 和 Bob

1. Alice 和 Bob 都从 `main` 拉取了代码
2. Alice 提交了 commit A，推送到 `main`
3. Bob 本地做了 commit B，但忘记了先 pull
4. Bob 使用 `git push --force` 强制推送

**结果**：Alice 的 commit A 被"覆盖"了，从历史中消失！

### 实验步骤 4：模拟强推危害

在 Gitea 上创建一个测试分支，模拟这个场景：

```bash
# Alice 的视角（本地）
git switch -c test-force-push
echo "Alice's work" > alice.txt
git add alice.txt
git commit -m "Alice: add alice.txt"
git push -u origin test-force-push

# 假设现在 Bob 在另一台机器上
# Bob 忘记了 pull，直接做了提交
echo "Bob's work" > bob.txt
git add bob.txt
git commit -m "Bob: add bob.txt"

# Bob 尝试普通 push，会失败
git push origin test-force-push
# 报错：! [rejected] ... (non-fast-forward)

# Bob 使用了危险的 force push
git push --force origin test-force-push
```

现在去 Gitea 上看：Alice 的提交不见了！

### 如何补救

如果 Alice 的提交还在本地：

```bash
# Alice 找回自己的提交
git fetch origin
git log --oneline HEAD..origin/test-force-push
# 找到 Alice 提交的 hash
git cherry-pick <alice-commit-hash>
git push origin test-force-push
```

### 什么时候可以用 force push

- 只对自己的**私有分支**使用
- 确认没有其他人基于这个分支工作
- 推荐使用 `--force-with-lease`（更安全的强制推送）

```bash
# 更安全的强制推送
git push --force-with-lease origin feature/my-branch
```

---

## 八、团队协作检查清单

### 提交前

- [ ] 代码已通过本地测试
- [ ] 提交信息符合规范
- [ ] 提交粒度合理（一个提交做一件事）

### Push 前

- [ ] 已经 `git pull` 获取最新代码
- [ ] 解决了可能的冲突
- [ ] 确认推送到正确的分支

### 创建 PR 前

- [ ] PR 标题和描述完整
- [ ] 关联了相关 Issue
- [ ] CI 检查通过

### 合并 PR 前

- [ ] 至少有一位 Reviewer 批准
- [ ] 所有讨论已解决
- [ ] CI 通过

---

## 九、练习题

### 练习 1：按规范完成一次完整流程

1. 从 `main` 创建一个规范命名的功能分支
2. 做几次符合规范的提交
3. 推送到远程，创建一个规范的 PR
4. 模拟 Review（自己批准自己的 PR）
5. 合并 PR，删除分支

### 练习 2：编写团队协作规范文档

为你的（模拟）团队编写一份简短的协作规范，包含：

- 分支命名规则
- 提交信息格式
- PR 流程要求
- 禁止事项（如禁止对 main 强推）

---

## 十、参考答案（仅供对照）

### 练习 1 参考流程

```bash
# 创建分支
git switch main
git pull origin main
git switch -c feature/sample-feature

# 开发与提交
echo "Sample feature" > sample.txt
git add sample.txt
git commit -m "feat: add sample feature"

# 推送
git push -u origin feature/sample-feature

# 在 Gitea Web 界面创建 PR...

# 合并后清理
git switch main
git pull origin main
git branch -d feature/sample-feature
```

### 练习 2 参考模板

```markdown
# 团队 Git 协作规范

## 分支命名
- feature/<功能名>
- bugfix/<问题描述>
- hotfix/<紧急修复>

## 提交信息
- feat: 新功能
- fix: 修复 Bug
- docs: 文档更新
- refactor: 重构

## PR 流程
1. 从 main 创建分支
2. 开发完成后创建 PR
3. 等待至少一人 Review
4. Review 通过后合并

## 禁止事项
- 禁止对 main 分支强制推送
- 禁止直接提交到 main
- 禁止合并未通过 CI 的 PR
```

---

## 十一、延伸阅读

- [GitHub Flow 官方文档](https://docs.github.com/en/get-started/quickstart/github-flow)
- [Git Flow 原文](https://nvie.com/posts/a-successful-git-branching-model/)
- [约定式提交](https://www.conventionalcommits.org/)
- [如何写好 Git Commit Message](https://cbea.ms/git-commit/)
