# 关卡 43：Git 别名与配置进阶

**所属阶段**：配置与文本处理 / Git 配置  
**本关关键词**：`git config`、`alias`、`includeIf`、多层配置、`credential.helper`、`git lg`

---

## 一、本关目标

- 在 [关卡 00](./lesson-00-install-and-config.md) 基础配置之上，掌握**别名（alias）**与**分层配置**。
- 能编写常用 `git config --global alias.*`，提升日常效率。
- 理解配置优先级：命令行 > 环境变量 > 本地 `.git/config` > 全局 `~/.gitconfig` > 系统配置。
- 了解 `includeIf` 按目录切换身份、`credential.helper` 保存凭据的适用场景。

---

## 二、前置条件

**学习模式：**

- 🌐 **在线可学**：阅读配置示例与对照表。
- 🐳 **建议本地实验**：在 Web 终端或本机执行 `git config` 命令。

**环境要求：**

- [ ] 已完成 [关卡 00](./lesson-00-install-and-config.md)。
- [ ] 能使用 `git config --list` 查看当前配置。

---

## 三、边看边做

### 步骤 1：查看配置来源

```bash
git config --list --show-origin | head -20
git config --global --list
git config --local --list 2>/dev/null || echo "不在 Git 仓库内，跳过 local"
```

`--show-origin` 显示每条配置来自哪个文件，排查「为什么我的设置不生效」时非常有用。

### 步骤 2：添加实用别名

以下命令写入**全局**配置（可按需删减）：

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD --stat'
```

验证：

```bash
git st
git last
```

### 步骤 3：美化日志别名 `lg`

```bash
git config --global alias.lg "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
```

在任意仓库执行：

```bash
git lg -10
```

对照原生命令：

```bash
git log --oneline --graph -10
```

别名可以包含引号与 `!` 外壳命令（见步骤 5）。

### 步骤 4：按目录切换配置（includeIf）

适合「公司项目用工作邮箱，个人项目用私人邮箱」：

编辑 `~/.gitconfig`，在末尾添加（路径按你的环境修改）：

```ini
[user]
    name = Personal User
    email = personal@example.com

[includeIf "gitdir:~/work/"]
    path = ~/.gitconfig-work

[includeIf "gitdir:~/projects/oss/"]
    path = ~/.gitconfig-oss
```

创建 `~/.gitconfig-work`：

```ini
[user]
    name = Work User
    email = you@company.com
```

进入 `~/work/` 下克隆的仓库时，Git 会自动加载工作配置。验证：

```bash
cd ~/work 2>/dev/null || mkdir -p ~/work/demo && cd ~/work/demo
git init
git config user.email
```

### 步骤 5：Shell 命令别名（`!` 前缀）

```bash
git config --global alias.undo '!git reset HEAD~1 --mixed'
git config --global alias.amend '!git commit --amend --no-edit'
```

`!` 表示后面是 Shell 命令，而不是 Git 子命令。慎用会改写历史的别名，仅在个人分支使用。

### 步骤 6：凭据与编辑器

```bash
git config --global core.editor "nano"
git config --global init.defaultBranch main
git config --global pull.rebase false
```

凭据缓存（避免每次 push 输入密码，实验环境可选）：

```bash
git config --global credential.helper 'cache --timeout=3600'
```

Windows 常用 `manager` 或 `manager-core`；macOS 可用 `osxkeychain`。本课程 Gitea 实验见 [关卡 06a](./lesson-06a-ssh-setup-and-clone.md) 优先用 SSH。

### 步骤 7：仓库级覆盖

在单个仓库内覆盖全局设置：

```bash
cd ~/projects/playground-hello 2>/dev/null || cd ~/projects/regex-demo
git init 2>/dev/null || true
git config --local user.email "playground@example.com"
git config --local --list | grep user
```

本地配置优先级高于全局，适合开源贡献时临时切换签名邮箱。

---

## 四、验收清单

- [ ] ✓ 能用 `git config --list --show-origin` 查看配置来源
- [ ] ✓ 至少创建 3 个别名并验证生效
- [ ] ✓ 理解 global / local / system 的优先级
- [ ] ✓ 能描述 `includeIf` 的典型使用场景
- [ ] ✓ 知道 `alias` 中 `!` 表示 Shell 命令

---

## 五、常见错误

### ❌ 别名不生效或报语法错误

**原因：** 引号嵌套错误，或 Shell 转义问题。

**解决：** 用单引号包裹整个 alias 值；复杂格式参考 `git lg` 示例逐段测试。

### ❌ `includeIf` 未加载

**原因：** `gitdir:` 路径末尾需要 `/`；路径与实际仓库父目录不匹配。

**解决：** 确保 `gitdir:~/work/` 形式正确，仓库位于该目录树下。

### ❌ 误用全局 `user.email` 提交到公司仓库

**原因：** 未配置 `includeIf` 或 local 覆盖。

**解决：** 公司仓库内执行 `git config --local user.email ...` 或使用条件 include。

---

## 六、练习/思考题

1. 为 `git diff --cached` 创建别名 `dc`，并试用。
2. 写一条 `alias` 显示最近 5 次提交的简短一行日志（自定格式）。
3. 列出你当前全部 alias：`git config --get-regexp '^alias\.'`。
4. **思考题**：别名应该提交到仓库 `.git/config` 吗？团队共享别名有哪些更好做法？

**下一关：** [关卡 44：.gitattributes 与合并策略](./lesson-44-gitattributes.md)
