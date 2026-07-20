# 关卡 00：命令行与工作目录基础

**所属阶段**：环境与配置 / 终端基础  
**本关命令关键词**：`pwd`、`ls`、`cd`、`mkdir`、`rm`、`cp`、`mv`、`cat`、`less`、`head`、`tail`、`grep`、`find`、`chmod`、`tree`、`df`、`du`、`tar`、`curl`、`clear`

---

## 一、本关目标

- 让完全不熟悉命令行的同学，在进入 Git 关卡前先适应一下终端。
- 掌握 Git 学习前最常用的 Linux 命令：导航目录、读写文件、搜索、打包与网络请求。
- 能在 Web 终端里自如地切换到练习目录，执行简单命令而不慌。

学完这一关，你再看后面文档里出现的「在终端执行以下命令」时，就不会被 `cd` / `ls` / `grep` 这些基础命令绊住了。

---

## 二、前置条件

- 已经能够通过 `docker compose up -d --build` 启动本学习环境。
- 能在浏览器打开学习工作台：`http://localhost:8081/workspace.html`。
- 能在 Web 终端（`http://localhost:8080`）中输入命令并看到输出。

---

## 三、边看边做：终端基础体验

> 建议：左侧打开本关文档，右侧 Web 终端中边看边敲。以下步骤都在 Web 终端中完成。

### 步骤 1：认识「当前目录」

```bash
pwd
```

**预期输出：**

```text
/home/playground
```

- `pwd` 是「print working directory」的缩写，用来查看**当前所在目录**。

### 步骤 2：列出当前目录下的文件

```bash
ls
```

你会看到当前目录下的文件 / 文件夹，例如 `projects`、`README.md` 等。

常用变体：

```bash
ls -l    # 详细列表（权限、大小、时间）
ls -a    # 包含隐藏文件（以 . 开头）
ls -la   # 两者结合
```

### 步骤 3：切换到练习目录

Web 终端中已经为你准备了一个通用的工作目录 `projects`：

```bash
cd projects
pwd
```

**预期输出：**

```text
/home/playground/projects
```

- `cd` 是「change directory」，用来切换目录。
- `cd ..` 回到上一级；`cd ~` 回到用户主目录。

### 步骤 4：创建与删除目录 / 文件

```bash
mkdir cli-playground
cd cli-playground
pwd
```

创建一个测试文件并查看内容：

```bash
echo "hello terminal" > notes.txt
cat notes.txt
```

- `cat` 一次性显示整个文件内容（适合短文件）。
- `less notes.txt` 分页查看（按 `q` 退出；适合长文件）。
- `head notes.txt` 看前几行；`tail notes.txt` 看后几行（`-n 5` 指定行数）。

复制、移动、重命名：

```bash
cp notes.txt notes-backup.txt
ls
mv notes-backup.txt backup.txt
ls
```

删除文件与目录：

```bash
rm backup.txt
cd ..
rmdir cli-playground    # 只能删空目录
mkdir -p cli-playground/subdir
echo "x" > cli-playground/subdir/x.txt
rm -r cli-playground  # 删除非空目录（本关练习可用，生产环境慎用）
```

> 小提示：`rm -r` 不可恢复，删除前务必确认路径。本课程后续 Git 操作不会依赖这条命令。

### 步骤 5：搜索文件与内容

在 `projects` 下创建几个文件用于练习：

```bash
cd ~/projects
mkdir -p search-demo/src
echo "Git is awesome" > search-demo/README.md
echo "function login() {}" > search-demo/src/app.js
echo "function logout() {}" > search-demo/src/auth.js
```

按文件名查找：

```bash
find search-demo -name "*.js"
```

在文件内容中搜索：

```bash
grep -r "function" search-demo
grep -n "Git" search-demo/README.md
```

### 步骤 6：权限与目录树（可选）

查看文件权限：

```bash
ls -l search-demo/README.md
chmod +x search-demo/README.md   # 示例：添加可执行位（对普通文本文件无实际意义）
ls -l search-demo/README.md
```

若系统已安装 `tree`，可直观查看目录结构：

```bash
tree search-demo 2>/dev/null || find search-demo
```

### 步骤 7：磁盘空间与打包（了解即可）

```bash
df -h .          # 当前文件系统可用空间
du -sh search-demo   # 目录占用大小
```

打包与解包示例：

```bash
tar -czf search-demo.tar.gz search-demo
ls -lh search-demo.tar.gz
mkdir unpack-demo && tar -xzf search-demo.tar.gz -C unpack-demo
ls unpack-demo
```

### 步骤 8：用 curl 请求网络（可选）

```bash
curl -sI https://example.com | head -5
```

`-s` 静默模式，`-I` 只取响应头。后续 CI/CD 关卡里也会见到 `curl` 检查服务是否就绪。

### 步骤 9：清空终端屏幕

```bash
clear
```

清屏只是让当前显示干净一些，并不会删除任何文件或 Git 仓库。

---

## 四、如何确认自己做对了

运行以下命令快速自检：

```bash
cd ~/projects
pwd
ls search-demo 2>/dev/null || ls
grep -r "function" search-demo 2>/dev/null | head -3
```

- [ ] ✓ `pwd` 输出以 `/home/playground` 开头的路径
- [ ] ✓ 能用 `cd` 进入 `projects` 并在其中创建 / 删除测试目录
- [ ] ✓ 能用 `cat` / `head` / `tail` 查看文件，`cp` / `mv` 复制或移动文件
- [ ] ✓ 能用 `grep` 或 `find` 找到刚创建的文件或关键字
- [ ] ✓ 知道 `rm -r` 的危险性，并能在练习后清理 `search-demo`、`unpack-demo` 等测试目录

---

## 五、常见错误与排查

### ❌ `cd: no such file or directory`

**可能原因：** 目录名拼写错误，或尚未创建。

**解决方法：**

```bash
pwd
ls
mkdir -p projects   # 若 projects 不存在则创建
cd projects
```

### ❌ `Permission denied`

**可能原因：** 对文件 / 目录没有读、写或执行权限。

**解决方法：** 用 `ls -l` 查看权限；确认你在自己的主目录下操作。不要随意对系统目录使用 `chmod`。

### ❌ `command not found: tree`

**可能原因：** 容器镜像未预装 `tree`。

**解决方法：** 用 `find .` 或 `ls -R` 代替，或跳过该步骤——不影响后续 Git 学习。

### ❌ `grep` 没有输出

**可能原因：** 关键字大小写不匹配，或路径不对。

**解决方法：** 使用 `grep -ri "关键字" 目录`（`-i` 忽略大小写），并先用 `ls` 确认文件存在。

---

## 六、完整命令参考（扩展阅读）

本关只收录 Git 学习**前**最常用的命令子集。更完整的 Linux 命令说明见：

- [Linux 命令搜索与速查（本仓库镜像）](https://linux-command.alexander.xin/)

> 致谢：上述参考站内容整理自开源项目 [jaywcjlove/linux-command](https://github.com/jaywcjlove/linux-command)（MIT），本课程按实验场景做了裁剪与改写，**不会**把全部 600+ 条命令塞进文档。

**Windows 用户：** 若更习惯 PowerShell，可先阅读 [关卡 40：PowerShell 基础](./lesson-40-powershell-basics.md) 与 [关卡 41：跨平台命令行对照](./lesson-41-cli-cross-platform.md)；也可安装 Git Bash / WSL 后直接跟本关 Bash 命令练习。

---

## 七、练习题（可选）

1. 在 `projects` 目录下，创建两个子目录：`git-basic` 和 `git-advanced`。
2. 在 `git-basic` 中创建 `notes.txt`，写入三行内容，用 `head -2` 和 `tail -1` 分别查看。
3. 用 `find git-basic -type f` 列出所有文件，用 `grep` 搜索其中一行文字。
4. 将整个 `git-basic` 打成 `git-basic.tar.gz`，再解压到 `git-advanced/restore` 目录，确认内容一致。
5. 完成后删除练习目录，保持 `projects` 整洁：

   ```bash
   rm -rf ~/projects/search-demo ~/projects/unpack-demo ~/projects/git-basic ~/projects/git-advanced
   rm -f ~/projects/search-demo.tar.gz
   ```
