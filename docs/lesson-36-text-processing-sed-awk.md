# 关卡 36：文本处理（grep、sed、awk 与常用工具）

**所属阶段**：计算机基础 / 文本处理  
**本关命令关键词**：`grep`、`sed`、`awk`、`cut`、`sort`、`uniq`、`wc`

---

## 一、本关目标

- 复习并强化 `grep`：行过滤、正则、递归、忽略大小写。
- 掌握 `sed` 替换：`s/old/new/g`，以及原地修改 `-i` 的用法与风险。
- 掌握 `awk` 按列打印字段：空格/分隔符、`$1` `$NF`、`print`。
- 会用 `cut`、`sort`、`uniq` 做简单统计与去重。

读 CI 日志、从 `git log` 提取作者、批量改配置文件，这些工具能省大量时间。

---

## 二、前置条件

**学习模式：**

- 🌐 **在线可学**：语法与示例可在文档中完成；[命令练习场](../site/playground.html) 可模拟部分命令。
- 🐳 **建议本地实验**：在 Web 终端 <http://localhost:8080> 对真实文件操作。

**环境要求：**

- [ ] 已完成 [关卡 00b](./lesson-00-terminal-basics.md)（含 `grep` 入门）。
- [ ] 🐳 Web 终端可用。
- [ ] 🐳 可选：`playground-hello` 中有若干次提交，便于 `git log` 练习。

---

## 三、边看边做

### 步骤 1：准备示例数据

```bash
mkdir -p ~/projects/text-demo
cd ~/projects/text-demo

cat > access.log << 'EOF'
192.168.1.10 GET /api/users 200
192.168.1.11 POST /api/login 401
192.168.1.10 GET /api/users 200
192.168.1.12 GET /health 200
192.168.1.11 POST /api/login 200
EOF

cat > packages.csv << 'EOF'
name,version,license
git-workflow-lab,1.0.0,MIT
helper-lib,2.1.0,Apache-2.0
git-workflow-lab,1.0.1,MIT
EOF
```

### 步骤 2：`grep` 复习

```bash
grep "200" access.log
grep -c "401" access.log
grep -E "GET|POST" access.log
grep -v "health" access.log
```

在目录树中递归（与 Git 无关的文件搜索）：

```bash
grep -r "git-workflow" .
```

### 步骤 3：`sed` 替换

```bash
sed 's/200/OK/g' access.log
sed 's/401/FAIL/g' access.log | grep FAIL
```

- `s/模式/替换/g`：`g` 表示一行内全部替换。
- 默认输出到 stdout，**不**改原文件。

原地修改（🐳 练习前备份）：

```bash
cp access.log access.log.bak
sed -i 's/192.168.1.10/10.0.0.1/g' access.log
diff access.log.bak access.log
```

macOS 上 `sed -i` 语法不同；本实验 Linux 容器用 `sed -i '...'` 即可。

删除匹配行：

```bash
sed '/health/d' access.log.bak
```

### 步骤 4：`awk` 按列处理

空格分隔的 log：

```bash
awk '{print $1, $3, $4}' access.log.bak
awk '$4 == "401" {print $1, $2}' access.log.bak
awk '{count[$1]++} END {for (ip in count) print ip, count[ip]}' access.log.bak
```

- `$0` 整行，`$1` 第一列，`$NF` 最后一列。
- `END` 块在全部行处理完后执行，适合统计。

CSV 指定逗号分隔：

```bash
awk -F',' 'NR>1 {print $1, $2}' packages.csv
awk -F',' '$1=="git-workflow-lab" {print $0}' packages.csv
```

### 步骤 5：`cut`、`sort`、`uniq`

```bash
cut -d' ' -f1 access.log.bak | sort | uniq -c | sort -nr
```

- `cut` 按分隔符切列；`-d' '` 空格，`-f1` 第一列。
- `sort` 排序；`uniq -c` 合并相邻重复并计数（故需先 sort）。

CSV 版：

```bash
cut -d',' -f1 packages.csv | tail -n +2 | sort | uniq -c
```

### 步骤 6：管道组合——小型「分析链」

统计每种 HTTP 方法出现次数：

```bash
awk '{print $2}' access.log.bak | sort | uniq -c
```

找出返回 200 的 IP 列表（去重）：

```bash
awk '$4=="200" {print $1}' access.log.bak | sort -u
```

### 步骤 7：结合 Git log（🐳 playground-hello）

```bash
cd ~/playground-hello 2>/dev/null || echo "skip if no repo"

git log --oneline | head -10
git log --format='%an' | sort | uniq -c | sort -nr
git log --format='%h %s' | grep -i fix
```

从提交信息里筛 `fix` 类 commit，是发布说明的常见前处理。

### 步骤 8：`wc` 与组合

```bash
wc -l access.log.bak
grep "200" access.log.bak | wc -l
```

---

## 四、如何确认自己做对了

```bash
cd ~/projects/text-demo
test $(grep -c "OK" <(sed 's/200/OK/g' access.log.bak)) -ge 3 && echo "sed OK"
awk '$4=="401" {print $1}' access.log.bak | grep -q "192.168.1.11" && echo "awk OK"
cut -d' ' -f1 access.log.bak | sort -u | wc -l
```

- [ ] ✓ `grep -E` 能匹配 GET 或 POST
- [ ] ✓ `sed 's///g'` 替换后输出符合预期，理解 `-i` 会改原文件
- [ ] ✓ `awk '{print $N}'` 能取出 IP、方法、状态码列
- [ ] ✓ `sort | uniq -c` 能统计 IP 或方法次数
- [ ] ✓ 🐳 对 `git log` 用过 `grep` 或 `awk` 过滤

---

## 五、常见错误

### ❌ `sed` 把备份也改了

**可能原因：** 对原文件多次 `-i` 且无备份。

**解决方法：** 先 `cp file file.bak`；或使用 `sed -i.bak '...'` 自动生成备份。

### ❌ `uniq` 没有合并重复行

**可能原因：** 未先 `sort`，重复行不相邻。

**解决方法：** 始终 `sort | uniq`。

### ❌ `awk` 列错位

**可能原因：** 多个连续空格仍算一列（默认 FS）；CSV 未 `-F','`。

**解决方法：** 对 CSV 用 `-F','`；对不规则空格可用 `awk -F'[ ]+'`。

### ❌ `grep` 正则特殊字符未转义

**可能原因：** `.` `*` 在正则中有含义。

**解决方法：** 固定字符串用 `grep -F 'literal'`；或转义 `\`。

---

## 六、练习/思考题

1. 从 `access.log.bak` 生成报告：每个状态码各有多少行（提示：`awk` + `sort` + `uniq -c`）。
2. 用 `sed` 把 `packages.csv` 里版本号 `1.0.0` 改成 `1.0.2`，输出到新文件 `packages-new.csv`（不要用 `-i`）。
3. 🐳 在 `playground-hello` 执行：`git log --format='%s' | grep -E '^(feat|fix|docs):' | wc -l`。
4. **思考题**：CI 日志几千行，你会如何用 `grep` + `tail` 或 `awk` 快速定位失败步骤？

**清理（可选）：**

```bash
rm -rf ~/projects/text-demo
```
