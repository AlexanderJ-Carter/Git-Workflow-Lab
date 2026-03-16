# 关卡 00：安装 Git 并完成基础配置

**所属阶段**：环境与配置（阶段 0）  
**本关命令关键词**：`git --version`、`git config`、全局 `.gitignore`、`git help`

---

## 一、本关目标

- 确认本机已经正确安装了 Git。
- 完成最基本的用户信息配置（user.name / user.email）。
- 配置一些常用全局选项（如默认分支名、换行符、颜色显示）。
- 理解全局 `.gitignore` 的作用，避免把无关文件提交进仓库。
- 学会使用 `git help` / `git help <command>` 查阅官方帮助。

学完这一关，你就有了一个「干净且可用」的 Git 开发环境，后面所有关卡都以此为基础。

---

## 二、前置条件

- 已有一台可用的开发机器（Windows / macOS / Linux 均可）。
- 具备基本的命令行使用能力（能打开终端 / PowerShell 并执行命令）。

---

## 三、边看边做：安装与版本确认

### 步骤 1：检查是否已安装 Git

在终端中执行：

```bash
git --version
```

如果输出类似：

```text
git version 2.x.y
```

说明已经安装成功，可以跳到「基础配置」部分。

如果提示「未找到命令」：

- Windows：
  - 推荐从 Git 官方网站下载「Git for Windows」安装包：  
    - 浏览器访问 `https://git-scm.com/download/win`  
    - 按提示安装，安装过程中可以使用默认选项（后续需要再调整的地方会在本关提到）。
- macOS：
  - 可以使用 Homebrew：`brew install git`，或通过 Xcode Command Line Tools 安装。
- Linux：
  - 以 Debian/Ubuntu 为例：`sudo apt-get install git`。  
  - 其他发行版可使用对应包管理器。

安装完成后，重新打开终端，再次确认 `git --version`。

---

## 四、基础配置：用户名、邮箱与默认分支名

### 步骤 2：配置用户名与邮箱

这些信息会出现在每一次提交的记录里，用于标识「是谁写的这次提交」。

执行：

```bash
git config --global user.name "你的名字或昵称"
git config --global user.email "你的邮箱@example.com"
```

查看是否生效：

```bash
git config --global user.name
git config --global user.email
```

### 步骤 3：设置默认分支名（可选但推荐）

新版本 Git 默认主分支名多为 `main`，有的老环境可能仍是 `master`。建议统一为 `main`：

```bash
git config --global init.defaultBranch main
```

之后使用 `git init` 创建的新仓库，默认主分支名就会是 `main`。

---

## 五、常用全局选项与全局 .gitignore

### 步骤 4：配置换行符与颜色显示

建议启用彩色输出，方便阅读：

```bash
git config --global color.ui auto
```

关于换行符（Windows 用户特别注意）：

- 如果你主要在 Windows 上开发，并与 Linux/服务器协作，可以设置：

  ```bash
  git config --global core.autocrlf true
  ```

- 如果你主要在类 Unix 系统（macOS / Linux），常用设置为：

  ```bash
  git config --global core.autocrlf input
  ```

这可以帮助在不同系统之间统一提交到仓库中的换行符格式，减少无意义的 diff。

### 步骤 5：配置全局 .gitignore（避免常见无效文件进入仓库）

全局 `.gitignore` 用于在所有仓库中忽略某些文件/目录（如操作系统生成的垃圾文件、编辑器临时文件等）。

1. 指定全局 ignore 文件路径，例如：

   ```bash
   git config --global core.excludesfile ~/.gitignore_global
   ```

2. 编辑 `~/.gitignore_global`，加入一些常见规则，例如：

   ```text
   # 操作系统
   .DS_Store
   Thumbs.db

   # 编辑器
   .vscode/
   .idea/

   # 日志与临时文件
   *.log
   *.tmp
   ```

以后创建的所有仓库，都会自动忽略这些文件。

---

## 六、学会查看帮助文档（自我进阶的关键）

Git 自带的帮助非常完整，建议养成习惯：

- 查看某个命令的官方用法：

  ```bash
  git help status
  git help commit
  git help branch
  ```

- 或使用：

  ```bash
  git status --help
  ```

多数系统会在终端中打开 man page 或浏览器帮助页面，其中的「Examples」对学习很有用。

---

## 七、如何确认自己做对了

- `git --version` 输出正常。
- `git config --global user.name` / `user.email` 能显示出你刚设置的值。
- `git config --global init.defaultBranch` 为 `main`（如果你按推荐设置）。
- `git config --global core.autocrlf`、`color.ui` 等选项已按你的系统和习惯设置。
- `~/.gitignore_global` 存在并包含一些通用忽略规则。
- 能通过 `git help <command>` 打开官方帮助文档。

---

## 八、练习题

### 练习 1：查看当前所有全局配置

1. 在终端执行：

   ```bash
   git config --global --list
   ```

2. 观察输出，确认本关设置的各项是否都在其中。
3. 思考：是否有来自你之前环境的遗留配置需要清理或调整？

### 练习 2：为你常用的编辑器配置为 Git 默认编辑器（可选）

1. 假设你常用 VS Code，可以这样设置：

   ```bash
   git config --global core.editor "code --wait"
   ```

2. 随后在需要编辑 commit message 的场景（例如使用 `git commit` 打开编辑器时），会自动启用 VS Code。

---

## 九、参考答案（仅供对照）

### 练习 1 参考思路

```bash
git config --global --list
```

可能输出类似：

```text
user.name=Your Name
user.email=your_email@example.com
init.defaultbranch=main
color.ui=auto
core.autocrlf=true
core.excludesfile=/home/you/.gitignore_global
```

如果发现有不认识的配置项，可以暂时记下来，在后续遇到相关行为时再回头查。

### 练习 2 参考思路

常见编辑器配置示例（按需选择，非必须）：

- VS Code：

  ```bash
  git config --global core.editor "code --wait"
  ```

- Vim（多数系统默认）：

  ```bash
  git config --global core.editor "vim"
  ```

配置好后，可以通过一次测试提交来验证编辑器是否按预期打开。

