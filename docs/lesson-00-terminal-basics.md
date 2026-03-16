# 关卡 00：命令行与工作目录基础

**所属阶段**：环境与配置 / 终端基础  
**本关命令关键词**：`pwd`、`ls` / `dir`、`cd`、`clear` / `cls`、`mkdir`、`rm` / `del`

---

## 一、本关目标

- 让完全不熟悉命令行的同学，在进入 Git 关卡前先适应一下终端。
- 搞清楚「当前目录」「切换目录」「列出文件」这些最基本操作。
- 能在 Web 终端里自如地切换到练习目录，执行简单命令而不慌。

学完这一关，你再看后面文档里出现的「在终端执行以下命令」时，就不会被 `cd` / `ls` 这些基础命令绊住了。

---

## 二、前置条件

- 已经能够通过 `docker compose up -d --build` 启动本学习环境。
- 能在浏览器打开学习工作台：`http://localhost:8081/workspace.html`。

---

## 三、边看边做：终端基础体验

> 建议：左侧打开本关文档，右侧 Web 终端中边看边敲。

### 步骤 1：认识「当前目录」

在 Web 终端中输入：

```bash
pwd
```

你会看到类似：

```text
/home/playground
```

- `pwd` 是「print working directory」的缩写，用来查看**当前所在目录**。

### 步骤 2：列出当前目录下的文件

在同一个终端中输入：

```bash
ls
```

你会看到当前目录下的文件 / 文件夹，例如：

```text
projects  README.md  ...
```

- 在 Linux / macOS / Web 终端里常用 `ls`。
- 在 Windows 原生 PowerShell / CMD 中，等价命令是 `dir`。

### 步骤 3：切换到练习目录

Web 终端中已经为你准备了一个通用的工作目录 `projects`。执行：

```bash
cd projects
pwd
```

确认输出变成类似：

```text
/home/playground/projects
```

- `cd` 是「change directory」，用来切换目录。

### 步骤 4：创建 / 删除测试目录

创建一个测试用的目录：

```bash
mkdir cli-playground
ls
```

你应该能在列表中看到 `cli-playground` 这个目录。进入它：

```bash
cd cli-playground
pwd
```

如果想返回上一级目录：

```bash
cd ..
pwd
```

- `..` 表示「上一级目录」，`.` 表示「当前目录」。

如果你想删除刚才创建的空目录：

```bash
rmdir cli-playground
ls
```

> 小提示：  
> - Linux 下 `rm -r 目录名` 可以删除「非空目录」，但属于危险命令，本课程中不会强制要求使用。  
> - Windows 原生 PowerShell 中，常见等价命令是：`New-Item`、`Remove-Item` 等。

### 步骤 5：清空终端屏幕

当终端内容滚得太长看不清时，可以清屏：

```bash
clear
```

在 Windows PowerShell 中常用：

```powershell
cls
```

清屏只是让当前显示干净一些，并不会删除任何文件或 Git 仓库。

---

## 四、如何确认自己做对了

- 你能说出：
  - `pwd` 是查看当前目录；
  - `ls` / `dir` 是列出当前目录内容；
  - `cd` 用来切换目录，`cd ..` 回到上一级；
  - `clear` / `cls` 只是清屏。
- 你知道 Web 终端里推荐把练习项目放在 `/home/playground/projects` 目录下。

---

## 五、练习题（可选）

1. 在 `projects` 目录下，创建两个子目录：`git-basic` 和 `git-advanced`。
2. 在 `git-basic` 中创建一个空文件 `notes.txt`（可以先用 `touch notes.txt` 或通过编辑器创建）。
3. 切换到 `git-advanced` 目录，再通过 `cd ..` 回到 `projects`，确保你始终搞得清自己当前在哪里。

