# 关卡 31：管道与重定向

**所属阶段**：计算机基础 / Shell I/O  
**本关命令关键词**：`|`、`>`、`>>`、`<`、`2>`、`2>&1`、`&>`、`tee`、`stdin`/`stdout`/`stderr`

---

## 一、本关目标

- 理解标准输入（stdin）、标准输出（stdout）、标准错误（stderr）三个数据流。
- 掌握管道 `|`：把前一个命令的输出作为后一个命令的输入。
- 掌握重定向：`>` 覆盖写入、`>>` 追加、`<` 输入重定向、`2>` 错误重定向、`2>&1` 合并错误到标准输出。
- 会用 `tee` 同时输出到屏幕和文件。

这些技能在查看 Git 日志、过滤 CI 日志、保存命令结果时每天都会用到。

---

## 二、前置条件

**学习模式：**

- 🌐 **在线可学**：阅读概念与示例，配合测验巩固；重定向语法可在纸上推演。
- 🐳 **建议本地实验**：在 Web 终端（<http://localhost:8080>）亲手敲命令，观察 stdout/stderr 行为。

**环境要求：**

- [ ] 已完成 [关卡 00b](./lesson-00-terminal-basics.md) 或 [关卡 30](./lesson-30-shell-scripting-basics.md)。
- [ ] 🐳 本地：`docker compose up -d`，终端可用。
- [ ] 🐳 可选：在 `playground-hello` 中生成一些 Git 日志用于过滤练习。

---

## 三、边看边做

> 在 Web 终端执行以下命令。

### 步骤 1：认识三个标准流

每个命令默认：

| 流 | 文件描述符 | 默认去向 |
|----|-----------|----------|
| stdin  | 0 | 键盘输入 |
| stdout | 1 | 终端屏幕 |
| stderr | 2 | 终端屏幕（错误信息） |

演示 stdout 与 stderr 分离：

```bash
echo "this is stdout"
echo "this is stderr" >&2
ls existing-file 2>/dev/null || true
ls no-such-file-xyz
```

第三条命令把 stderr 丢弃；第四条会在屏幕上看到 `No such file` 错误。

### 步骤 2：输出重定向 `>` 与 `>>`

```bash
cd ~/projects 2>/dev/null || mkdir -p ~/projects && cd ~/projects
mkdir -p pipe-demo && cd pipe-demo

echo "line 1" > output.txt
echo "line 2" >> output.txt
cat output.txt
```

- `>` **覆盖**文件；再次 `>` 会清空原内容。
- `>>` **追加**到文件末尾。

### 步骤 3：错误重定向 `2>` 与合并 `2>&1`

```bash
ls no-such-file > ok.txt 2> err.txt
cat ok.txt
cat err.txt

ls no-such-file > combined.txt 2>&1
cat combined.txt
```

- `2>` 只把 stderr 写入文件，stdout 仍显示在屏幕。
- `2>&1` 表示「把 stderr 重定向到 stdout 当前指向的位置」，常写成 `command > file 2>&1` 把全部输出写入同一文件。

简写（bash）：`&> all.txt` 等价于 stdout+stderr 都进文件。

### 步骤 4：管道 `|`

```bash
echo -e "apple\nbanana\napricot\ncherry" > fruits.txt
cat fruits.txt | grep "ap"
cat fruits.txt | grep "ap" | wc -l
```

管道连接 **stdout**；stderr 默认不会进入管道。若需一起过滤：

```bash
{ ls pipe-demo; ls no-such-file; } 2>&1 | grep -v "^total"
```

### 步骤 5：输入重定向 `<`

```bash
wc -l < fruits.txt
grep "ap" < fruits.txt
```

`< file` 表示从文件读 stdin，等价于 `grep "ap" fruits.txt`，但在脚本里更明确。

### 步骤 6：`tee`——边看边存

```bash
echo "deploy log entry" | tee deploy.log
cat deploy.log
echo "second entry" | tee -a deploy.log
```

- `tee` 把 stdin 复制一份到文件，另一份仍输出到终端。
- `-a` 追加模式，类似 `>>`。

模拟 CI 里「打印日志并保存 artifact」：

```bash
git --version | tee -a ~/projects/pipe-demo/tool-versions.log 2>/dev/null || echo "git not in path" | tee -a ~/projects/pipe-demo/tool-versions.log
```

### 步骤 7：结合 Git 日志（🐳 在 playground-hello）

若已 clone `playground-hello`：

```bash
cd ~/playground-hello
git log --oneline | head -5
git log --oneline 2>/dev/null | grep -i "feat" | tee /tmp/feat-commits.txt
cat /tmp/feat-commits.txt
```

---

## 四、如何确认自己做对了

```bash
cd ~/projects/pipe-demo
test -f output.txt && grep -q "line 2" output.txt && echo "redirect OK"
echo "test" | grep "test" | wc -l
echo "test" | tee /tmp/tee-test.txt >/dev/null && test -s /tmp/tee-test.txt && echo "tee OK"
```

- [ ] ✓ `output.txt` 有两行，`>>` 追加生效
- [ ] ✓ 能把 `ls` 错误写入 `err.txt` 或 `combined.txt`
- [ ] ✓ 管道 `grep | wc -l` 输出正确行数
- [ ] ✓ `tee` 后文件内容与屏幕一致
- [ ] ✓ 能口头解释 `2>&1` 与 `|` 的区别

---

## 五、常见错误

### ❌ 管道后文件为空，但屏幕有输出

**可能原因：** 错误信息走 stderr，未进入管道。例如 `curl bad-url | grep HTTP` 看不到错误。

**解决方法：** 使用 `{ curl ...; } 2>&1 | grep` 或先 `-s` / `-f` 处理 curl。

### ❌ `>` 误删重要文件

**可能原因：** `> important.log` 会先清空文件再写入。

**解决方法：** 确认路径；需要保留时用 `>>`；危险操作前 `cp` 备份。

### ❌ `2>&1` 顺序写反

**可能原因：** 写成 `command 2>&1 > file` 时，stderr 仍可能进屏幕。

**解决方法：** 正确顺序：`command > file 2>&1`。

### ❌ 管道中 `$?` 只反映最后一个命令

**可能原因：** `cmd1 | cmd2` 的退出码来自 `cmd2`，`cmd1` 失败可能被忽略。

**解决方法：** 在 bash 中可 `set -o pipefail`（脚本里常用）；或分开执行检查。

---

## 六、练习/思考题

1. 把 `fruits.txt` 中含字母 `a` 的行数写入 `count.txt`（只用管道与重定向，不用手动数数）。
2. 运行 `find ~/projects -name "*.txt" 2>/dev/null | sort | uniq -c`，解释每一部分的作用。
3. 在 `playground-hello` 执行 `git log --oneline | head -3 | tee last-3.txt`，把结果贴进 `notes.md` 再提交。
4. **思考题**：为什么 CI 日志里常看到 `2>&1 | tee build.log`？它解决了什么问题？

**清理（可选）：**

```bash
rm -rf ~/projects/pipe-demo /tmp/feat-commits.txt /tmp/tee-test.txt
```
