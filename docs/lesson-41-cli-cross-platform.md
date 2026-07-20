# 关卡 41：跨平台命令行对照与选型

**所属阶段**：编程与跨平台 CLI / 综合  
**本关关键词**：Bash、PowerShell、cmd、WSL、路径、CRLF、引号、终端选型

---

## 一、本关目标

- 建立 **Bash / PowerShell / cmd** 常用命令的对照表，减少「在 Windows 上不知道 Linux 命令怎么写」的摩擦。
- 理解**路径**、**引号**、**通配符**、**行尾符（LF vs CRLF）** 在跨平台协作中的坑。
- 能根据场景选择：**本机 PowerShell**、**Git Bash**、**WSL**、**本课程 Docker 终端**。
- 为团队协作（有人用 macOS、有人用 Windows）建立共同语言。

---

## 二、前置条件

**学习模式：**

- 🌐 **在线可学**：以阅读对照表与场景说明为主，测验巩固。
- 🐳 **可选实验**：分别在 PowerShell 与 Web 终端（8080）执行同一组 Git 命令，对比输出。

**环境要求：**

- [ ] 已阅读 [关卡 00b](./lesson-00-terminal-basics.md)、[关卡 40](./lesson-40-powershell-basics.md) 至少其一。
- [ ] 知道 Git 命令在各平台通常一致（`git status` 等）。

---

## 三、边看边做

### 3.1 核心对照表

### 3.1 文件与目录

| 任务 | Bash / Linux | PowerShell | cmd（了解即可） |
|------|--------------|------------|-----------------|
| 当前目录 | `pwd` | `Get-Location` / `pwd` | `cd` |
| 列目录 | `ls -la` | `Get-ChildItem` / `ls` | `dir` |
| 切换目录 | `cd path` | `Set-Location path` / `cd` | `cd path` |
| 创建目录 | `mkdir -p a/b` | `mkdir a\b -Force` | `mkdir a\b` |
| 复制 | `cp -r src dst` | `Copy-Item -Recurse src dst` | `xcopy` |
| 移动/重命名 | `mv a b` | `Move-Item a b` | `move` |
| 删除 | `rm -rf dir` | `Remove-Item -Recurse dir` | `rmdir /s` |
| 读文件 | `cat file` | `Get-Content file` | `type file` |
| 搜索文本 | `grep -r pat .` | `Select-String -Path * -Pattern pat` | `findstr` |
| 查命令位置 | `which git` | `Get-Command git` | `where git` |

### 3.2 环境变量

| 任务 | Bash | PowerShell |
|------|------|------------|
| 查看 | `echo $HOME` | `$env:USERPROFILE` 或 `echo $env:HOME` |
| 临时设置 | `export VAR=1` | `$env:VAR = "1"` |
| 列出全部 | `env` | `Get-ChildItem Env:` |

详见 [关卡 32](./lesson-32-env-and-path.md)。

### 3.3 管道与重定向

| 任务 | Bash | PowerShell |
|------|------|------------|
| 管道 | `cmd1 \| cmd2` | `cmd1 \| cmd2` |
| 标准输出到文件 | `> file` | `> file` |
| 追加 | `>> file` | `>> file` |
| 标准错误 | `2> err.log` | `2> err.log` |

详见 [关卡 31](./lesson-31-pipes-redirection.md)。

### 3.4 Git（全平台一致）

以下命令在 Bash、PowerShell、cmd 中**相同**（路径引号需注意）：

```bash
git status
git add .
git commit -m "feat: message"
git push origin main
git clone http://localhost:3000/playground/playground-hello.git
```

Windows 上推荐在 **PowerShell** 或 **Git Bash** 中操作；避免在 cmd 里处理复杂引号。

---

## 四、跨平台陷阱

### 4.1 路径分隔符

- Linux / macOS / Web 终端：`/home/playground/projects`
- Windows 传统：`C:\Users\You\projects`
- **Git 内部** 常用正斜杠；Windows 上 `git status` 可能显示 `/` 路径——属正常。

在脚本中优先用引号包裹路径：`"C:\My Projects\repo"`。

### 4.2 行尾符 CRLF vs LF

| 系统 | 行尾 |
|------|------|
| Linux / macOS | LF (`\n`) |
| Windows 默认 | CRLF (`\r\n`) |

**与 Git 的关系：**

```bash
git config --global core.autocrlf true    # Windows 常用：检出 CRLF，提交 LF
git config --global core.autocrlf input # macOS/Linux：提交 LF
```

若 Shell 脚本报 `bad interpreter`，见 [关卡 30](./lesson-30-shell-scripting-basics.md) 的 `sed -i 's/\r$//'` 处理。

### 4.3 引号与转义

- Bash 单引号 `'$VAR'` **不**展开变量；双引号 `"$VAR"` 展开。
- PowerShell 单引号同样字面量；双引号展开 `$var`。
- 含空格的提交信息：各平台都推荐 `git commit -m "fix: update readme"`。

### 4.4 通配符

- Bash：`*.md` 由 Shell 展开。
- PowerShell：`*.md` 多由 cmdlet 处理；递归常用 `-Recurse -Filter *.md`。

---

## 五、学习路径选型建议

```text
你是 Windows 用户？
├── 只学 Git + 阅读课程 → PowerShell + Git for Windows 即可
├── 要完全复现文档里的 Bash 命令 → Git Bash 或 WSL
├── 要跟本课程 Docker 实验一致 → docker compose + Web 终端 :8080
└── 要写 Python/自动化 → PowerShell 7+ 或 WSL + python3

你是 macOS / Linux 用户？
└── 终端默认 Bash/Zsh，直接跟 00b 与 30+ 关卡即可；读 40–41 了解 Windows 同事环境
```

**推荐组合（Windows 完整学习本仓库）：**

1. 安装 Docker Desktop + Git for Windows + Windows Terminal  
2. `docker compose up -d` 启动实验环境  
3. 浏览器打开 `http://localhost:8081/workspace.html` 分屏学习  
4. 日常 Windows 文件操作用 PowerShell；实验关卡用 Web 终端  

---

## 六、验收清单

- [ ] ✓ 能从对照表查出 5 组 Bash ↔ PowerShell 等价命令
- [ ] ✓ 能解释 CRLF 与 `core.autocrlf` 的作用
- [ ] ✓ 能根据场景在 PowerShell / Git Bash / WSL / Web 终端中做出选择
- [ ] ✓ 知道 Git 子命令本身跨平台一致，差异在 Shell 与路径

---

## 七、练习/思考题

1. 分别在 PowerShell 与 Web 终端执行：`git --version`、`pwd`/`Get-Location`、`ls`/`Get-ChildItem`，记录差异。
2. 在 `playground-hello` 故意用 Windows 记事本改一个 `.sh` 文件，观察 CRLF 导致的报错并修复。
3. 制作一张你自己的「常用命令小抄」（5 行 Bash + 5 行 PowerShell）。
4. **思考题**：为什么 CI 服务器（GitHub Actions、Gitea Runner）几乎总是 Linux 环境？

**下一关：** [关卡 42：正则表达式基础](./lesson-42-regex-basics.md)

**延伸阅读：**

- [关卡 39：编程入门（Python）](./lesson-39-programming-basics-python.md)
- [学习模式说明](./learning-modes.md)
- 外部：[Microsoft PowerShell 文档](https://learn.microsoft.com/powershell/)
