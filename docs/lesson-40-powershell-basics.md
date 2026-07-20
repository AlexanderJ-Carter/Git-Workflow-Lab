# 关卡 40：PowerShell 与 Windows 命令行

**所属阶段**：编程与跨平台 CLI / Windows 终端  
**本关关键词**：`Get-Location`、`Set-Location`、`Get-ChildItem`、`Copy-Item`、管道、`foreach`、`git`

---

## 一、本关目标

- 理解 Windows 上三种常见命令环境：**cmd**、**PowerShell**、**Git Bash** 的区别与选用场景。
- 掌握 PowerShell 基础：导航目录、列出文件、复制移动、变量与管道。
- 能在 PowerShell 中执行 **Git** 命令，完成与 Linux 终端等价的日常操作。
- 知道何时应改用 **WSL** 或本实验的 Web 终端（Linux）来对齐课程其余关卡。

Windows 用户不必「先学会 Linux 才能学 Git」——用对工具，PowerShell 同样能高效协作。

---

## 二、前置条件

**学习模式：**

- 🌐 **在线可学**：阅读本文与命令对照表、完成测验。
- 🐳 **建议本地实验**：在 Windows 本机打开 **PowerShell** 或 **Windows Terminal**（无需 Docker）。

**环境要求：**

- [ ] Windows 10/11（或 macOS/Linux 上阅读对照，了解团队 Windows 同事的视角）。
- [ ] 已安装 [Git for Windows](https://git-scm.com/download/win)（自带 Git Bash，且 `git` 会加入 PATH）。
- [ ] 推荐安装 [Windows Terminal](https://aka.ms/terminal) 统一管理 PowerShell / cmd / WSL 标签页。

---

## 三、边看边做

> 以下在 **PowerShell** 中执行（提示符多为 `PS C:\...>`）。以你的用户目录为起点。

### 步骤 1：确认环境与版本

```powershell
$PSVersionTable.PSVersion
git --version
Get-Location
```

- PowerShell 5.x 随 Windows 自带；PowerShell 7+（`pwsh`）跨平台，语法基本一致。
- `Get-Location` 相当于 Linux 的 `pwd`。

### 步骤 2：导航与列目录

| 目标 | Bash（关卡 00b） | PowerShell |
|------|------------------|------------|
| 当前路径 | `pwd` | `Get-Location` 或 `pwd`（别名） |
| 切换目录 | `cd projects` | `Set-Location projects` 或 `cd projects` |
| 列出文件 | `ls -la` | `Get-ChildItem` 或 `ls` |
| 创建目录 | `mkdir demo` | `New-Item -ItemType Directory demo` 或 `mkdir demo` |
| 复制文件 | `cp a b` | `Copy-Item a b` |
| 删除文件 | `rm a` | `Remove-Item a` |

练习：

```powershell
cd $HOME
mkdir git-lab-demo -Force
cd git-lab-demo
New-Item -ItemType File -Name README.md -Value "# Demo"
Get-ChildItem
```

### 步骤 3：变量与字符串

```powershell
$user = "Playground"
$branch = "feature/login"
Write-Host "User: $user on branch $branch"
```

- 变量以 `$` 开头（类似 Bash 的 `$VAR`，但赋值用 `$x = 1` 而非 `x=1`）。
- 双引号字符串会展开变量；单引号 `'$user'` 按字面量。

### 步骤 4：管道与过滤

```powershell
Get-ChildItem -Recurse -Filter *.md | Select-Object Name, Length
Get-ChildItem | Where-Object { $_.Length -gt 1000 }
```

- `|` 管道把左边输出传给右边命令（与 Bash 管道概念相同）。
- `Where-Object` 类似 `grep` 的过滤，更适合结构化对象。

### 步骤 5：条件与循环

```powershell
$env = "dev"
if ($env -eq "prod") {
  Write-Host "careful!"
} elseif ($env -eq "dev") {
  Write-Host "dev mode"
}

foreach ($name in @("main", "develop", "feature/x")) {
  if ($name -like "feature/*") {
    Write-Host "feature branch: $name"
  }
}
```

### 步骤 6：在 PowerShell 里用 Git

```powershell
cd $HOME\git-lab-demo
git init
git add README.md
git commit -m "docs: init readme"
git log --oneline
git status
```

与 Linux 终端中的 Git 命令**完全相同**——差异主要在**路径**与**Shell 引号规则**：

```powershell
# Windows 路径可用反斜杠或正斜杠
cd C:\Users\You\projects
cd C:/Users/You/projects   # Git 也接受
```

### 步骤 7：三种 Windows 终端怎么选？

| 环境 | 适合 |
|------|------|
| **PowerShell** | 日常 Windows 管理、运行 Git、自动化脚本（`.ps1`） |
| **Git Bash** | 想直接复用课程里的 Bash 命令、跑 `.sh` 脚本 |
| **WSL** | 需要完整 Linux 环境、与 Docker/本课程 Web 终端一致 |
| **本课程 Web 终端** | 浏览器内 Linux Shell，与文档 00b–38 关卡一致 |

---

## 四、验收清单

- [ ] ✓ 能打开 PowerShell 并运行 `Get-Location`、`Get-ChildItem`
- [ ] ✓ 会用 `$变量` 与 `Write-Host`
- [ ] ✓ 能写简单的 `if` 与 `foreach`
- [ ] ✓ 在 PowerShell 中完成 `git init` → `commit` 最小闭环
- [ ] ✓ 能说出 PowerShell、Git Bash、WSL 的适用场景

---

## 五、常见错误

### ❌ 执行策略禁止运行脚本

**现象：** `.\script.ps1` 报 `running scripts is disabled`。

**解决：** 当前用户放宽策略（需管理员或组策略允许）：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

仅运行自己写的脚本；不要从不明来源执行 `.ps1`。

### ❌ `git` 不是内部或外部命令

**原因：** Git for Windows 未安装或未加入 PATH。

**解决：** 重装 Git 并勾选「Git from the command line and also from 3rd-party software」。

### ❌ 路径含空格未加引号

**解决：** `cd "C:\Users\My Name\projects"` 或对路径用引号包裹。

---

## 六、练习/思考题

1. 在 PowerShell 中列出当前目录下所有 `.md` 文件及其大小（`Get-ChildItem -Filter`）。
2. 用 `foreach` 打印 `git branch -a` 的每一行（提示：`git branch -a | ForEach-Object { ... }`）。
3. 对比 [关卡 00b](./lesson-00-terminal-basics.md) 的 `grep`，查文档说明 `Select-String` 的用法并试一条。
4. **思考题**：为什么本课程的 Docker Web 终端选择 Linux 而不是 Windows 容器？

**下一关：** [关卡 41：跨平台命令行对照](./lesson-41-cli-cross-platform.md)
