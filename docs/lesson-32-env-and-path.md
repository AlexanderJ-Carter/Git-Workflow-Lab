# 关卡 32：环境变量与 PATH

**所属阶段**：计算机基础 / 运行环境  
**本关命令关键词**：`env`、`export`、`echo $VAR`、`PATH`、`which`、`type`、`.bashrc`、`.zshrc`

---

## 一、本关目标

- 理解环境变量是什么，以及「当前 Shell 会话」与「子进程」如何继承变量。
- 会用 `export` 把变量导出给子命令和脚本使用。
- 理解 `PATH`：系统如何按顺序查找可执行命令。
- 知道 `.bashrc` / `.zshrc` 的作用，以及 `which` 如何定位命令路径。

配置好 Git 用户信息、CI Secrets、自定义工具路径，都离不开环境变量。

---

## 二、前置条件

**学习模式：**

- 🌐 **在线可学**：阅读本文与测验；`PATH` 概念可在文档中完整理解。
- 🐳 **建议本地实验**：在 Web 终端修改临时变量、查看 `which git`，体验更直观。

**环境要求：**

- [ ] 已完成 [关卡 00b](./lesson-00-terminal-basics.md)。
- [ ] 🐳 `docker compose up -d`，Web 终端 <http://localhost:8080> 可用。
- [ ] 了解 Git 全局配置（`git config --global user.name`）——它写入配置文件，与环境变量是不同机制，但常一起使用。

---

## 三、边看边做

### 步骤 1：查看与设置 Shell 变量

```bash
echo $HOME
echo $USER
echo $SHELL
MY_NOTE="learning PATH"
echo $MY_NOTE
```

- 未 `export` 的变量只在当前 Shell 内可见，子进程（脚本、命令）读不到。

### 步骤 2：`export` 导出给子进程

```bash
export LAB_REPO="playground-hello"
bash -c 'echo "Child sees: $LAB_REPO"'

UNEXPORTED="temp"
bash -c 'echo "Child cannot see: [$UNEXPORTED]"'
```

第二条子 Shell 中 `UNEXPORTED` 应为空。

在脚本中使用（🐳）：

```bash
cat > /tmp/use-env.sh << 'EOF'
#!/bin/bash
echo "Building $LAB_REPO ..."
EOF
chmod +x /tmp/use-env.sh
export LAB_REPO="playground-hello"
/tmp/use-env.sh
```

### 步骤 3：理解 `PATH`

```bash
echo $PATH
which git
which bash
type git
```

- `PATH` 是冒号分隔的目录列表；输入 `git` 时，Shell 按顺序在这些目录中查找名为 `git` 的可执行文件。
- `which` 显示第一个匹配的路径；`type` 还会说明是别名还是内置命令。

临时把自定义目录加入 PATH 前面（优先查找）：

```bash
mkdir -p ~/bin
echo '#!/bin/bash
echo "Hello from ~/bin/say-hi"' > ~/bin/say-hi
chmod +x ~/bin/say-hi
export PATH="$HOME/bin:$PATH"
which say-hi
say-hi
```

### 步骤 4：`env` 查看全部环境变量

```bash
env | grep -E '^(PATH|HOME|USER|TERM)=' | sort
env | wc -l
```

CI 里常见写法 `env:` 块，就是在 Job 里注入这些键值对。

### 步骤 5：配置文件 `.bashrc` / `.zshrc`

Web 终端容器内通常是 bash：

```bash
echo $SHELL
ls -la ~/.bashrc 2>/dev/null || echo "No .bashrc yet"
```

持久化变量（🐳 练习——重启容器后可能丢失，取决于 volume）：

```bash
grep -q 'MY_LAB_TAG' ~/.bashrc 2>/dev/null || echo 'export MY_LAB_TAG="git-workflow-lab"' >> ~/.bashrc
source ~/.bashrc
echo $MY_LAB_TAG
```

要点：

- 新开终端会读取 `~/.bashrc`（bash）或 `~/.zshrc`（zsh）。
- 修改后需 `source ~/.bashrc` 或重新登录才生效。
- **不要**把 Secrets 明文写进会提交到 Git 的文件；本关只练习非敏感标记。

### 步骤 6：与 Git / Docker 实验环境的关系

本仓库 `.env` 中的变量（如 `GITEA_ADMIN_USER`）由 **docker compose** 注入容器，不是 Shell 的 `export`：

```bash
# 在 Web 终端内（若已安装 docker CLI 且挂载了 compose 项目）
# docker compose config 2>/dev/null | head -20
```

在 Gitea 容器里，数据库连接等也来自环境变量——与你在 Shell 里 `export DATABASE_URL=...` 是同一套机制。

### 步骤 7：（可选）playground-hello 与 CI 变量名

阅读 [关卡 10](./lesson-10-first-ci-workflow.md) 工作流里的 `$GITHUB_REPOSITORY`、`$GITHUB_SHA`——Runner 在启动 Job 前 **export** 这些变量，脚本里才能 `$VAR` 引用。

---

## 四、如何确认自己做对了

```bash
export LAB_CHECK="ok"
bash -c 'test "$LAB_CHECK" = "ok" && echo "export OK"'
echo $PATH | grep -q "$HOME/bin" && echo "PATH prepend OK" || echo "run step 3 first"
which git
```

- [ ] ✓ 能解释「Shell 变量」与 `export` 后「环境变量」的区别
- [ ] ✓ `echo $PATH` 能看到多个目录，且理解查找顺序
- [ ] ✓ `which git` 返回可执行文件路径
- [ ] ✓ 知道 `.bashrc` 用途及 `source` 的作用
- [ ] ✓ 能说明 Docker Compose `environment:` 与 Shell `export` 的相似点

---

## 五、常见错误

### ❌ 脚本里 `$VAR` 为空

**可能原因：** 父 Shell 设置了变量但未 `export`；或在不同终端会话中设置。

**解决方法：** `export VAR=value`；或在同一脚本开头定义。

### ❌ `command not found` 但文件明明存在

**可能原因：** 可执行文件不在 `PATH` 中；或未 `chmod +x`。

**解决方法：** `export PATH="/path/to/dir:$PATH"` 或用绝对路径 `/path/to/cmd`；检查 `which cmd`。

### ❌ 修改 `.bashrc` 后不生效

**可能原因：** 未 `source`；或当前 Shell 是 login shell 只读 `.profile`。

**解决方法：** `source ~/.bashrc`；或开新终端标签页。

### ❌ PATH 拼写错误导致系统命令「消失」

**可能原因：** 错误地 `export PATH="~/bin"` 覆盖了原有 PATH，丢失 `/usr/bin` 等。

**解决方法：** 始终 **追加**：`export PATH="$HOME/bin:$PATH"`，不要覆盖整个 PATH。

---

## 六、练习/思考题

1. 创建 `~/bin/lab-pwd`，输出当前目录和 `git --version`（若可用），加入 PATH 后直接运行 `lab-pwd`。
2. 用 `env | sort` 找出 5 个你能在 CI 文档里见到的变量名（如 `HOME`、`CI`、`PATH`）。
3. 对比：`git config --global user.name "You"` 与 `export GIT_AUTHOR_NAME="You"` 分别存在哪里、谁读取？
4. **思考题**：为什么生产环境把密码放在环境变量里，而不是写在 Shell 脚本里？

**清理（可选）：**

```bash
rm -f ~/bin/say-hi ~/bin/lab-pwd 2>/dev/null
# 若曾修改 .bashrc，可手动删除 MY_LAB_TAG 那一行
```
