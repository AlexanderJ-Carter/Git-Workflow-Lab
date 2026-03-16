# 关卡 13：Git 标签与版本发布

**所属阶段**：进阶操作
**本关命令关键词**：`git tag`、`git push --tags`、`git tag -d`、语义化版本

---

## 一、本关目标

- 理解轻量标签与注解标签的区别。
- 学会创建、查看、推送、删除标签。
- 了解语义化版本号规范（SemVer）。
- 掌握 GitHub/Gitea Release 功能的使用。

学完这一关，你就能为项目打上规范的版本标签，并发布正式版本了。

---

## 二、前置条件

- 已完成关卡 01-03（Git 基础操作）。
- 有一个可用的 Gitea 仓库用于练习。
- 了解基本的版本管理概念。

---

## 三、边看边做前先理解的核心概念

### 什么是标签（Tag）？

标签是 Git 中用于标记特定提交的"别名"，通常用于标记发布版本。

```
v1.0.0 ──► abc1234 (某个特定的提交)
v1.1.0 ──► def5678 (另一个提交)
```

### 轻量标签 vs 注解标签

| 类型     | 命令                       | 特点                   | 推荐场景           |
| -------- | -------------------------- | ---------------------- | ------------------ |
| 轻量标签 | `git tag v1.0`             | 只是一个指针           | 临时标记、个人使用 |
| 注解标签 | `git tag -a v1.0 -m "msg"` | 包含创建者、日期、消息 | 正式发布版本       |

### 语义化版本号（SemVer）

版本号格式：`MAJOR.MINOR.PATCH`

- **MAJOR**：不兼容的 API 变更
- **MINOR**：向后兼容的功能新增
- **PATCH**：向后兼容的问题修复

示例：
- `1.0.0` → `1.0.1`：修复 Bug
- `1.0.1` → `1.1.0`：新增功能
- `1.1.0` → `2.0.0`：重大变更

---

## 四、边看边做：具体步骤

### 步骤 1：准备实验仓库

```bash
# 使用已有的 playground-hello 仓库
cd playground-hello

# 确保工作区干净
git status

# 确认当前分支
git branch
```

### 步骤 2：创建轻量标签

```bash
# 创建轻量标签
git tag v0.1.0

# 查看所有标签
git tag

# 查看标签指向的提交
git show v0.1.0
```

### 步骤 3：创建注解标签（推荐）

```bash
# 创建注解标签
git tag -a v1.0.0 -m "Release version 1.0.0

Features:
- Initial release
- Basic functionality

Bug fixes:
- None
"

# 查看标签详情
git show v1.0.0
```

### 步骤 4：给历史提交打标签

```bash
# 查看提交历史
git log --oneline -10

# 给特定提交打标签
git tag -a v0.0.1 abc1234 -m "Initial prototype"
# 把 abc1234 替换为实际的提交 hash
```

### 步骤 5：推送标签到远程

```bash
# 推送单个标签
git push origin v1.0.0

# 推送所有本地标签
git push --tags

# 或者
git push origin --tags
```

### 步骤 6：在 Gitea 上查看标签和 Release

1. 打开 Gitea 仓库页面
2. 点击"Releases"或"Tags"标签
3. 你应该能看到刚才推送的标签

### 步骤 7：创建正式 Release

在 Gitea Web 界面：

1. 进入 Releases 页面
2. 点击"New Release"
3. 填写信息：
   - **Tag**: 选择已有标签或创建新标签
   - **Title**: `v1.0.0 - First Release`
   - **Content**: 发布说明
   - **Attach files**: 可选，上传构建产物
4. 点击"Publish Release"

### 步骤 8：删除标签

```bash
# 删除本地标签
git tag -d v0.1.0

# 删除远程标签
git push origin --delete v0.1.0

# 或者用简写
git push origin :refs/tags/v0.1.0
```

### 步骤 9：检出标签版本

```bash
# 检出特定标签（detached HEAD 状态）
git checkout v1.0.0

# 基于标签创建分支
git checkout -b hotfix/v1.0.1 v1.0.0
```

---

## 五、版本发布最佳实践

### 发布说明模板

```markdown
## [v1.1.0] - 2024-01-15

### Added
- 新增用户登录功能
- 添加暗色主题支持

### Changed
- 优化首页加载速度

### Fixed
- 修复移动端显示问题 (#42)

### Breaking Changes
- API 端点 `/api/user` 改为 `/api/v1/user`

### Contributors
@alice, @bob
```

### 标签命名规范

| 格式           | 用途       |
| -------------- | ---------- |
| `v1.0.0`       | 正式版本   |
| `v1.0.0-alpha` | 内部测试版 |
| `v1.0.0-beta`  | 公开测试版 |
| `v1.0.0-rc.1`  | 发布候选版 |

---

## 六、如何确认自己做对了

- `git tag` 能列出创建的标签。
- `git show v1.0.0` 能看到标签信息和对应提交。
- 标签已推送到 Gitea 远程仓库。
- Gitea 的 Releases 页面能看到发布的版本。

---

## 七、练习题

### 练习 1：完整版本发布流程

1. 在项目中做几次提交，模拟功能开发。
2. 创建 `v1.0.0` 注解标签并推送。
3. 在 Gitea 上创建 Release，填写发布说明。
4. 删除本地标签，再从远程拉取标签验证。

### 练习 2：语义化版本实践

1. 当前版本 `v1.0.0`，修复一个 Bug → 创建什么标签？
2. 新增一个功能 → 创建什么标签？
3. 做了一个不兼容的改动 → 创建什么标签？

### 练习 3：基于标签创建 hotfix

1. 假设 `v1.0.0` 有紧急 Bug。
2. 基于该标签创建 hotfix 分支。
3. 修复 Bug 后，创建 `v1.0.1` 标签。

---

## 八、参考答案（仅供对照）

### 练习 1 参考思路

```bash
# 1. 提交代码
echo "Feature A" > feature-a.txt
git add feature-a.txt && git commit -m "feat: add feature A"

# 2. 创建标签
git tag -a v1.0.0 -m "First release"

# 3. 推送
git push origin main --tags

# 4. 在 Gitea 创建 Release...

# 5. 删除并重新拉取
git tag -d v1.0.0
git fetch --tags
git tag  # 验证标签存在
```

### 练习 2 参考答案

- 修复 Bug → `v1.0.1`（PATCH）
- 新增功能 → `v1.1.0`（MINOR）
- 不兼容改动 → `v2.0.0`（MAJOR）

### 练习 3 参考思路

```bash
# 1. 基于 v1.0.0 创建 hotfix 分支
git checkout -b hotfix/urgent-fix v1.0.0

# 2. 修复 Bug
echo "Fix applied" >> bug.txt
git add bug.txt && git commit -m "fix: urgent bug fix"

# 3. 创建新标签
git tag -a v1.0.1 -m "Hotfix for urgent bug"

# 4. 推送
git push origin hotfix/urgent-fix --tags
```

---

## 九、常见问题与排查

### 问题 1：推送标签时报错

```text
error: dst refspec v1.0.0 matches more than one
```

**原因**：本地和远程都有同名分支和标签。

**解决**：使用完整路径：

```bash
git push origin refs/tags/v1.0.0
```

### 问题 2：标签推送到错误的分支

标签是附在特定提交上的，不是分支上的。如果标签出现在"错误"的分支，说明那个提交在两个分支都存在。

### 问题 3：如何在 CI 中获取当前标签

```bash
# GitHub Actions
echo $GITHUB_REF  # refs/tags/v1.0.0

# Git 命令
git describe --tags --exact-match
```

---

## 十、延伸阅读

- [语义化版本规范](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- Git 官方文档：`git help tag`
- GitHub Releases 最佳实践
