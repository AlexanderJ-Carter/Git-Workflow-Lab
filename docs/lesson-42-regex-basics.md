# 关卡 42：正则表达式基础

**所属阶段**：配置与文本处理 / 正则  
**本关关键词**：正则、`grep -E`、`sed`、捕获组、字符类、量词、`git grep`

---

## 一、本关目标

- 理解正则表达式（Regular Expression）是什么：用模式描述「一类文本」，而不是写死某一个字符串。
- 掌握最常用的元字符：`.`、`*`、`+`、`?`、`[]`、`^`、`$`、`|`、`()`。
- 能在 `grep -E`、`sed` 和 `git grep` 里写出实用模式，配合 [关卡 36](./lesson-36-text-processing-sed-awk.md) 处理日志与代码。
- 知道正则在 CI、代码审查、`.gitignore` 思维中的常见用途。

---

## 二、前置条件

**学习模式：**

- 🌐 **在线可学**：阅读模式与示例，完成 [技能测验](../site/quiz.html)。
- 🐳 **建议本地实验**：Web 终端（8080）或本机 Bash 执行 `grep`/`sed`。

**环境要求：**

- [ ] 已完成 [关卡 00b](./lesson-00-terminal-basics.md) 与 [关卡 36](./lesson-36-text-processing-sed-awk.md)（或至少会用 `grep`）。
- [ ] 可选：已完成 [关卡 39](./lesson-39-programming-basics-python.md)，便于对比 Python `re` 模块。

---

## 三、边看边做

> 在终端创建练习目录：

```bash
mkdir -p ~/projects/regex-demo
cd ~/projects/regex-demo
cat > commits.txt <<'EOF'
feat: add login page
fix(auth): handle timeout
docs: update readme
chore: bump deps
fix: typo in error message
feat(api): add health check
EOF
```

### 步骤 1：字面匹配 vs 模式匹配

```bash
grep 'fix' commits.txt
grep -E '^fix' commits.txt
grep -E '^feat' commits.txt
```

- 不加 `-E` 时，`grep` 默认用基本正则（BRE）；`-E` 启用扩展正则（ERE），`+`、`?`、`|`、`()` 更直观。
- `^` 表示行首；`fix` 只匹配以 `fix` 开头的行。

### 步骤 2：字符类与量词

| 模式 | 含义 | 示例匹配 |
|------|------|----------|
| `.` | 任意单个字符 | `a.c` → `abc`、`a1c` |
| `*` | 前一个字符 0 次或多次 | `ab*c` → `ac`、`abc` |
| `+` | 前一个字符 1 次或多次（需 `-E`） | `ab+c` → `abc` |
| `?` | 前一个字符 0 次或 1 次 | `colou?r` → `color`、`colour` |
| `[abc]` | 字符集之一 | `[Ff]ix` → `fix`、`Fix` |
| `[0-9]+` | 一个或多个数字 | `v[0-9]+` → `v1`、`v12` |
| `[^0-9]` | 非数字 | 排除数字 |

练习：

```bash
grep -E 'feat|fix' commits.txt
grep -E '\([a-z]+\)' commits.txt
grep -E ':[a-z ]+$' commits.txt
```

### 步骤 3：捕获组与替换（sed）

```bash
sed -E 's/^(feat|fix|docs|chore): (.+)$/\1 | \2/' commits.txt
```

- 括号 `()` 形成**捕获组**，`\1`、`\2` 在替换中引用。
- `s/模式/替换/` 只替换每行第一个匹配；`g` 标志替换全部。

从提交信息里提取 type：

```bash
sed -E 's/^([a-z]+)(\(.*\))?:.*/\1/' commits.txt | sort | uniq -c
```

### 步骤 4：在 Git 仓库里搜索

```bash
cd ~/projects
git clone http://localhost:3000/playground/playground-hello.git 2>/dev/null || true
cd playground-hello

git grep -E 'function|def ' -- '*.md' '*.sh' 2>/dev/null || git grep -E 'hello|README'
git grep -n -E 'TODO|FIXME' || echo "no TODO markers"
```

`git grep` 只搜**已跟踪**文件，比全目录 `grep -r` 更快，且尊重 `.gitignore`。

### 步骤 5：与 Python 对照（可选）

```python
import re
lines = open("commits.txt").read().splitlines()
for line in lines:
    m = re.match(r"^(feat|fix):\s+(.+)$", line)
    if m:
        print(m.group(1), "->", m.group(2))
```

Python 的 `re` 与终端 `grep -E` 语法高度相似，差异主要在转义规则。

---

## 四、验收清单

- [ ] ✓ 能解释 `^`、`$`、`.`、`*`、`+` 的含义
- [ ] ✓ 能用 `grep -E` 过滤以特定前缀开头的行
- [ ] ✓ 能用 `sed -E` 做简单捕获与替换
- [ ] ✓ 能在仓库内使用 `git grep` 定位代码
- [ ] ✓ 知道 BRE 与 ERE 的区别（本关以 `grep -E` 为主）

---

## 五、常见错误

### ❌ `grep: repetition-operator operand invalid`

**原因：** 在基本正则里写了 `+` 或 `?`，未加 `-E`。

**解决：** 使用 `grep -E`，或写成 `\+`、`\?`（BRE 转义）。

### ❌ 匹配过多或匹配不到

**原因：** `.` 匹配任意字符；`*` 贪婪；未锚定 `^`/`$`。

**解决：** 尽量写具体字符类 `[a-z]+`；需要整行匹配时加 `^` 与 `$`。

### ❌ sed 替换里 `\1` 不生效

**原因：** 未使用 `-E`，或括号未转义。

**解决：** `sed -E` 并检查捕获组写法。

---

## 六、练习/思考题

1. 写一条 `grep -E`，从 `commits.txt` 找出带 scope 的提交（含括号，如 `fix(auth):`）。
2. 用 `sed` 把所有 `feat:` 行改成 `feature:` 前缀（仅练习，勿提交到真实仓库）。
3. 在任意仓库用 `git grep` 搜索 `import` 或 `require`，统计命中文件数。
4. **思考题**：GitHub 的代码搜索、IDE「全局查找」与 `grep -E` 各适合什么场景？

**下一关：** [关卡 43：Git 别名与配置进阶](./lesson-43-git-config-advanced.md)
