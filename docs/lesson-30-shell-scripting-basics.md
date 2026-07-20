# 关卡 30：Shell 脚本基础（Bash）

**所属阶段**：计算机基础 / Shell 脚本  
**本关命令关键词**：`#!/bin/bash`、`chmod +x`、`$变量`、`if`、`for`、`echo`、`read`

---

## 一、本关目标

- 理解 Shell 脚本是什么，以及 shebang（`#!/bin/bash`）的作用。
- 能编写包含变量、条件判断（`if`）和循环（`for`）的简单 Bash 脚本。
- 会用 `chmod +x` 赋予执行权限，并直接运行脚本。
- 知道脚本与「一条条敲命令」的关系——CI/CD 流水线里的 `run:` 步骤本质上就是脚本。

学完这一关，你在阅读 GitHub Actions / Gitea Actions 的 `run:` 块时，就不会对 `$变量`、`if`、`for` 感到陌生。

---

## 二、前置条件

**学习模式：**

- 🌐 **在线可学**：阅读本文、完成 [技能测验](../site/quiz.html) 相关题目；概念部分不依赖 Docker。
- 🐳 **建议本地实验**：在 Web 终端（<http://localhost:8080>）中编写并运行脚本，体验更完整。

**环境要求：**

- [ ] 已完成 [关卡 00b：命令行基础](./lesson-00-terminal-basics.md)（或具备等价的 `cd` / `echo` / `ls` 能力）。
- [ ] 🐳 本地实验：已执行 `docker compose up -d`，能打开 <http://localhost:8080>。
- [ ] 🐳 可选：已 clone 演示仓库 `playground-hello`，在仓库中练习提交脚本文件：

  ```bash
  cd ~
  git clone http://localhost:3000/playground/playground-hello.git
  cd playground-hello
  ```

---

## 三、边看边做

> 建议：左侧打开本关文档，右侧 Web 终端边看边敲。以下步骤默认在 `~/projects` 或 `playground-hello` 目录下进行。

### 步骤 1：第一个脚本——用 shebang 声明解释器

```bash
mkdir -p ~/projects/shell-demo
cd ~/projects/shell-demo
```

创建 `hello.sh`：

```bash
cat > hello.sh << 'EOF'
#!/bin/bash
echo "Hello from a Bash script!"
echo "Current user: $(whoami)"
echo "Current directory: $(pwd)"
EOF
```

- `#!/bin/bash` 是 **shebang**，告诉系统用哪个解释器执行此文件。
- 第一行必须是文件的第一行，且前面不能有空格。

### 步骤 2：赋予执行权限并运行

```bash
chmod +x hello.sh
ls -l hello.sh
./hello.sh
```

**预期输出：** 三行问候信息，以及当前用户名和目录路径。

- `chmod +x` 添加「可执行」权限；没有这一步时，只能 `bash hello.sh` 而不能 `./hello.sh`。
- `./` 表示「当前目录下的可执行文件」。

### 步骤 3：变量与命令替换

创建 `greet.sh`：

```bash
cat > greet.sh << 'EOF'
#!/bin/bash
NAME="Git Learner"
REPO="playground-hello"
echo "Hi, $NAME!"
echo "Practice repo: $REPO"
echo "Today is $(date +%Y-%m-%d)"
EOF
chmod +x greet.sh
./greet.sh
```

要点：

- 变量赋值 **不能** 有空格：`NAME="value"` ✓，`NAME = "value"` ✗。
- `$变量名` 或 `${变量名}` 引用变量；`` `command` `` 或 `$(command)` 执行命令并嵌入结果。

### 步骤 4：读取用户输入

```bash
cat > ask.sh << 'EOF'
#!/bin/bash
read -p "Enter your name: " USER_NAME
echo "Welcome, $USER_NAME!"
EOF
chmod +x ask.sh
./ask.sh
```

输入任意名字后回车，应看到个性化问候。

### 步骤 5：条件判断 `if`

```bash
cat > check-branch.sh << 'EOF'
#!/bin/bash
BRANCH="${1:-main}"
if [ "$BRANCH" = "main" ]; then
  echo "On default branch: $BRANCH"
else
  echo "On feature branch: $BRANCH"
fi
EOF
chmod +x check-branch.sh
./check-branch.sh
./check-branch.sh feature/login
```

- `$1` 是第一个命令行参数；`${1:-main}` 表示「无参数时默认为 main」。
- `[ ]` 是 `test` 命令的简写，注意 `[` 与 `]` 两侧要有空格。

### 步骤 6：循环 `for`

```bash
cat > loop-commits.sh << 'EOF'
#!/bin/bash
for msg in "feat: add login" "fix: typo" "docs: update README"; do
  echo "Would commit: $msg"
done
EOF
chmod +x loop-commits.sh
./loop-commits.sh
```

若你在 `playground-hello` 目录，可扩展为遍历真实文件：

```bash
for f in *.md; do
  echo "Markdown file: $f"
done
```

### 步骤 7：（可选）提交到 Git

在 `playground-hello` 中：

```bash
mkdir -p scripts
cp ~/projects/shell-demo/hello.sh scripts/
git add scripts/hello.sh
git commit -m "feat: add hello shell script"
```

---

## 四、如何确认自己做对了

运行自检：

```bash
cd ~/projects/shell-demo
./hello.sh
./check-branch.sh develop | grep -q "feature branch" && echo "if OK"
./loop-commits.sh | wc -l
```

- [ ] ✓ `hello.sh` 第一行是 `#!/bin/bash`，且 `ls -l` 显示有 `x`（可执行）权限
- [ ] ✓ 能用 `./脚本名` 运行，输出符合预期
- [ ] ✓ `check-branch.sh feature/login` 输出包含 `feature branch`
- [ ] ✓ `for` 循环脚本输出了 3 行（或你设定的次数）
- [ ] ✓ 理解 shebang、`chmod +x`、变量引用与 `$1` 参数的基本用法

---

## 五、常见错误

### ❌ `bad interpreter: No such file or directory`

**可能原因：** 脚本在 Windows 上编辑，行尾是 CRLF（`\r\n`），或 shebang 路径错误。

**解决方法：**

```bash
sed -i 's/\r$//' hello.sh   # 去掉 Windows 换行
head -1 hello.sh              # 确认是 #!/bin/bash
```

### ❌ `Permission denied` 运行 `./hello.sh`

**可能原因：** 未 `chmod +x`，或文件系统挂载了 `noexec`。

**解决方法：** `chmod +x hello.sh`，或改用 `bash hello.sh`。

### ❌ `[ : missing ]` 或条件判断总是失败

**可能原因：** `[` 与 `]` 内侧缺少空格，或字符串比较未加引号导致变量为空时语法错误。

**解决方法：** 写成 `[ "$VAR" = "value" ]`，变量始终用双引号包裹。

### ❌ 变量赋值报错 `command not found`

**可能原因：** 写了 `NAME = "x"`（等号两侧有空格）。

**解决方法：** 改为 `NAME="x"`。

---

## 六、练习/思考题

1. 编写 `backup.sh`：接受一个目录名作为参数，若目录存在则用 `tar -czf 目录名.tar.gz 目录名` 打包，否则打印错误信息并退出（提示：`exit 1`）。
2. 编写 `count-lines.sh`：统计当前目录下所有 `.md` 文件的总行数（提示：`for` + `wc -l`）。
3. 在 `playground-hello` 添加 `scripts/pre-check.sh`，用 `if` 检查 `README.md` 是否存在，再 `git commit` 提交。
4. **思考题**：CI 工作流 YAML 里的 `run: |` 多行脚本，与你在本关写的 `.sh` 文件有什么相同与不同？

**清理练习目录（可选）：**

```bash
rm -rf ~/projects/shell-demo
```
