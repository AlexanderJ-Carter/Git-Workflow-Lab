# 关卡 33：进程与作业控制

**所属阶段**：计算机基础 / 进程管理  
**本关命令关键词**：`ps`、`top`/`htop`、`jobs`、`bg`、`fg`、`kill`、`nohup`、`&`

---

## 一、本关目标

- 理解「进程」：正在运行的程序实例，以及如何用 `ps` 查看。
- 会用 `top` 或 `htop`（若已安装）观察 CPU/内存占用。
- 掌握前台/后台作业：`&`、`jobs`、`bg`、`fg`。
- 会用 `kill` 发送信号终止进程；用 `nohup` 让任务在退出终端后继续运行。

当你在 Web 终端里跑长任务、或调试「端口被占用」时，这些命令是必备技能。

---

## 二、前置条件

**学习模式：**

- 🐳 **建议本地实验**：本关涉及进程、信号与后台作业，**需要在真实终端中操作**（Web 终端 <http://localhost:8080>）。
- 🌐 在线阅读可了解概念，但无法完整体验 `bg`/`fg`/`kill` 交互。

**环境要求：**

- [ ] 已完成 [关卡 00b](./lesson-00-terminal-basics.md)。
- [ ] 🐳 `docker compose up -d`，Web 终端可用。
- [ ] 本关练习均为临时进程，**不要** `kill` 系统关键服务或 Docker 容器内 PID 1。

---

## 三、边看边做

> 以下在 Web 终端执行。若 `htop` 未安装，用 `top` 代替（按 `q` 退出）。

### 步骤 1：查看当前 Shell 与进程

```bash
echo $$
ps -p $$
ps aux | head -5
ps aux | grep -E '[b]ash|[s]leep'
```

- `$$` 是当前 Shell 的 PID。
- `ps -p PID` 查看指定进程；`ps aux` 列出更多详细信息。
- `grep [b]ash` 技巧：避免 grep 匹配自身。

### 步骤 2：启动一个长时间运行的前台任务

```bash
sleep 300
```

终端会被占用。按 `Ctrl+C` 发送 SIGINT，终止 `sleep`。

### 步骤 3：后台运行与 `jobs`

```bash
sleep 200 &
sleep 150 &
jobs -l
```

- 命令末尾 `&` 把任务放到 **后台**，立即返回 Shell 提示符。
- `jobs -l` 显示作业编号（如 `[1]`）和 PID。

### 步骤 4：`fg` 与 `bg`

```bash
# 先启动一个前台 sleep（另开逻辑：用已有后台作业演示）
kill %1 2>/dev/null; sleep 120 &
jobs
fg %1
```

按 `Ctrl+Z` **挂起**前台任务，然后：

```bash
jobs
bg %1
jobs
```

- `Ctrl+Z`：暂停（SIGTSTP），任务变为 Stopped。
- `bg %N`：在后台 **继续** 运行第 N 个作业。
- `fg %N`：调到前台。

练习结束后清理：

```bash
kill %1 %2 2>/dev/null
jobs
```

### 步骤 5：`kill` 与信号

```bash
sleep 999 &
SLEEP_PID=$!
kill $SLEEP_PID
jobs
```

常用信号：

| 信号 | 命令 | 含义 |
|------|------|------|
| SIGTERM (15) | `kill PID` | 礼貌终止（默认） |
| SIGKILL (9) | `kill -9 PID` | 强制杀死，无法捕获 |
| SIGINT (2) | `Ctrl+C` | 中断前台进程 |

```bash
sleep 999 &
kill -15 %1
sleep 999 &
kill -9 %1
```

**注意：** 优先 `kill`（15），`-9` 仅当进程不响应时使用。

### 步骤 6：`nohup`——断开终端仍继续

```bash
cd ~/projects 2>/dev/null || mkdir -p ~/projects && cd ~/projects
nohup bash -c 'for i in 1 2 3 4 5; do echo "tick $i"; sleep 2; done' > nohup-demo.log 2>&1 &
echo "Background PID: $!"
tail -f nohup-demo.log
```

按 `Ctrl+C` 停止 `tail`（不会停止 nohup 任务）。等待约 10 秒后：

```bash
cat nohup-demo.log
```

- `nohup` 忽略挂断信号（SIGHUP），适合长时间脚本。
- 输出重定向到 `nohup-demo.log`，避免写入 `nohup.out`。

### 步骤 7：`top` 观察负载（可选）

```bash
top -b -n 1 | head -20
```

若容器内有 `htop`：

```bash
htop -d 5  # 5 秒后自动退出需手动 q；或直接 htop 后按 q
```

找出一个占用 CPU 较高的进程名，与 `ps aux` 对照。

### 步骤 8：与本实验环境的关系

本仓库 `docker compose up -d` 会启动多个容器进程（nginx、gitea、postgres、terminal）。在 **宿主机** 可用 `docker ps` 查看；在 Web 终端内你主要管理 **当前容器内** 的用户进程，不要误杀 ttyd 或 shell 父进程。

---

## 四、如何确认自己做对了

```bash
sleep 5 &
jobs | grep -q Running && echo "background OK"
kill %1 2>/dev/null; sleep 0.5; jobs
test -f ~/projects/nohup-demo.log && grep -q "tick 5" ~/projects/nohup-demo.log && echo "nohup OK"
```

- [ ] ✓ 能用 `ps` 找到自己的 bash PID
- [ ] ✓ 能用 `&` 启动后台任务，`jobs` 能看到
- [ ] ✓ 试过 `fg` / `bg` 或 `Ctrl+Z` 挂起/恢复
- [ ] ✓ 能用 `kill` 结束后台 `sleep`
- [ ] ✓ `nohup-demo.log` 中有 5 行 tick 输出

---

## 五、常见错误

### ❌ `kill: (12345) - No such process`

**可能原因：** 进程已自行结束；或 PID 写错。

**解决方法：** `jobs -l` 或 `ps aux | grep sleep` 确认 PID；用 `kill %1` 按作业号杀更稳妥。

### ❌ `Ctrl+Z` 后任务一直 Stopped

**可能原因：** 忘记 `bg` 或 `kill`。

**解决方法：** `bg %N` 继续，或 `kill %N` 结束。

### ❌ `nohup` 日志找不到

**可能原因：** 未重定向时默认写当前目录 `nohup.out`；工作目录不对。

**解决方法：** 显式 `> log 2>&1`；`cat nohup.out` 或指定路径。

### ❌ 在 Web 终端里 `kill -9` 自己的 Shell

**可能原因：** 对 `$` 或父进程误操作。

**解决方法：** 只 kill 练习用的 `sleep`；用作业号 `%N` 而非随意 PID。

---

## 六、练习/思考题

1. 同时启动 3 个 `sleep 600 &`，用 `jobs -l` 列出 PID，再一次性 `kill` 全部。
2. 写一行命令：后台跑 `while true; do date >> ~/tick.log; sleep 5; done`，用 `nohup` 并重定向 stderr。
3. 用 `ps aux | grep sleep` 与 `jobs` 对比：两者看到的进程有何不同？
4. **思考题**：CI Runner 里每个 Job 是独立进程还是容器？与你在终端里启动的后台任务有何相似之处？

**清理：**

```bash
kill $(jobs -p) 2>/dev/null
rm -f ~/projects/nohup-demo.log ~/tick.log 2>/dev/null
```
