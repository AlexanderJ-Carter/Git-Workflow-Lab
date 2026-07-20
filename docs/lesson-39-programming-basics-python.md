# 关卡 39：编程入门（Python）

**所属阶段**：编程与跨平台 CLI / 编程基础  
**本关关键词**：变量、数据类型、`if`/`for`、函数、`def`、缩进、Python 3

---

## 一、本关目标

- 理解「程序」是什么：按顺序执行的一组指令，能处理输入并产生输出。
- 掌握编程最基础的积木：**变量**、**条件判断**、**循环**、**函数**。
- 用 **Python 3** 写出可运行的小脚本，并与 [关卡 30](./lesson-30-shell-scripting-basics.md) 的 Bash 脚本对照理解。
- 知道这些概念如何出现在 CI 脚本、自动化工具和后端代码里。

学完这一关，你再看到 `if`、`for`、`def` 就不会只把它们当成「Shell 专属语法」——它们是通用编程思维。

---

## 二、前置条件

**学习模式：**

- 🌐 **在线可学**：阅读本文、对照代码示例、完成 [技能测验](../site/quiz.html)；概念不依赖 Docker。
- 🐳 **建议本地实验**：在本机终端运行 `python3`（Windows/macOS/Linux 均可）；Web 终端（8080）默认不含 Python，请用宿主机练习。

**环境要求：**

- [ ] 已完成 [关卡 00b](./lesson-00-terminal-basics.md)（知道如何在终端里运行命令）。
- [ ] 本机已安装 Python 3.10+（验证：`python3 --version` 或 Windows 上 `py -3 --version`）。
- [ ] 可选：已完成 [关卡 30](./lesson-30-shell-scripting-basics.md)，便于对比 Bash 与 Python。

---

## 三、边看边做

> 以下代码在**本机终端**执行。创建练习目录：

```bash
mkdir -p ~/projects/python-demo
cd ~/projects/python-demo
```

Windows PowerShell 可用：`mkdir $HOME\projects\python-demo; cd $HOME\projects\python-demo`

### 步骤 1：交互式解释器

```bash
python3
```

进入后尝试：

```python
>>> print("Hello, Python!")
>>> name = "Git Learner"
>>> print(f"Hi, {name}")
>>> exit()
```

- `print()` 输出到屏幕，类似 Bash 的 `echo`。
- `name = "..."` 是**变量赋值**；Python 用**缩进**表示代码块（不用 `{}`）。

### 步骤 2：变量与基本类型

创建 `types_demo.py`：

```python
title = "Git Workflow Lab"
lesson_no = 39
passed = True
tags = ["git", "python", "cli"]

print(type(title), title)
print(type(lesson_no), lesson_no)
print(type(passed), passed)
print(type(tags), tags)
```

运行：

```bash
python3 types_demo.py
```

常见类型：

| 类型 | 示例 | 用途 |
|------|------|------|
| `str` | `"hello"` | 文本 |
| `int` / `float` | `42`, `3.14` | 数字 |
| `bool` | `True`, `False` | 逻辑值 |
| `list` | `[1, 2, 3]` | 有序列表 |

### 步骤 3：条件判断 `if`

```python
branch = "main"

if branch == "main":
    print("production line")
elif branch.startswith("feature/"):
    print("feature branch")
else:
    print("other branch")
```

对照 Bash（关卡 30）：

```bash
if [ "$branch" = "main" ]; then
  echo "production line"
fi
```

### 步骤 4：循环 `for`

```python
commits = ["fix: typo", "feat: add quiz", "docs: update readme"]

for msg in commits:
    if msg.startswith("feat"):
        print("feature:", msg)
    else:
        print("other:", msg)
```

`for` 遍历列表中的每一项——与 Shell 的 `for f in *.md` 思路相同。

### 步骤 5：函数 `def`

```python
def greet(name: str) -> None:
  """向学习者问好。"""
  print(f"Hello, {name}! Ready to learn Git?")

def line_count(path: str) -> int:
  with open(path, encoding="utf-8") as f:
    return len(f.readlines())

greet("Alex")
```

- `def` 定义可复用的代码块，类似「把多行命令打包成一个名字」。
- 类型注解 `name: str` 可选，但有助于阅读和维护。

### 步骤 6：与 Git / CI 的衔接

阅读本仓库 `scripts/build-site.py` 开头几行——你会看到：

- `import` 引入模块（类似 Shell 的 `source` 其他脚本）
- `def build_site()` 函数组织逻辑
- `if __name__ == "__main__":` 表示「直接运行此文件时才执行」

CI 里的 Python 步骤也常是这样写的：

```yaml
- name: Run checks
  run: python3 scripts/some_check.py
```

---

## 四、验收清单

- [ ] ✓ 能在本机运行 `python3 --version` 并进入交互式解释器
- [ ] ✓ 理解变量赋值、四种基本类型
- [ ] ✓ 能写出含 `if`/`elif`/`else` 的脚本
- [ ] ✓ 能写出 `for` 循环遍历列表
- [ ] ✓ 能定义并调用 `def` 函数
- [ ] ✓ 能说出 Python 与 Bash 在缩进、变量语法上的主要区别

---

## 五、常见错误

### ❌ `IndentationError: unexpected indent`

**原因：** Python 用缩进表示块，混用 Tab 与空格或缩进不一致。

**解决：** 统一用 4 个空格；编辑器开启「显示空白字符」。

### ❌ `python: command not found`

**原因：** 未安装 Python，或 Windows 上需用 `py` 启动器。

**解决：** 安装 Python 3；Windows 试 `py -3 script.py`。

### ❌ 字符串与数字拼接报错

**原因：** `"Count: " + 3` 类型不匹配。

**解决：** 用 f-string：`f"Count: {3}"` 或 `str(3)` 转换。

---

## 六、练习/思考题

1. 写 `count_md.py`：统计当前目录下 `.md` 文件数量（提示：`import os` 或 `pathlib.Path`）。
2. 写 `conventional_check.py`：接收一组提交信息，打印哪些以 `feat:` 或 `fix:` 开头。
3. 把脚本放进 `playground-hello` 并 `git commit`（若已配置 Gitea）。
4. **思考题**：为什么很多 DevOps 工具（Ansible、pytest、本仓库构建脚本）选择 Python 而不是纯 Shell？

**下一关：** [关卡 40：PowerShell 与 Windows 命令行](./lesson-40-powershell-basics.md)
