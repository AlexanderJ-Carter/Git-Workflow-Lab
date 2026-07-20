# 关卡 37：网络排查基础

**所属阶段**：计算机基础 / 网络诊断  
**本关命令关键词**：`ping`、`curl`、`ss`、`lsof`、`dig`、`nslookup`、`ssh -v`

---

## 一、本关目标

- 会用 `ping` 与 `curl` 做最基本的「通不通、端口是否响应」检查。
- 会用 `ss`（或 `lsof`）查看本机监听端口与连接状态。
- 理解 DNS 查询：`dig` / `nslookup` 解析域名到 IP。
- 会用 `ssh -v` 调试 SSH 连接失败（本实验 Gitea SSH 端口 **2222**）。

「Gitea 打不开」「clone 失败」「端口被占用」——按本关顺序排查，多数能定位到环节。

---

## 二、前置条件

**学习模式：**

- 🐳 **建议本地实验**：网络命令需在真实网络栈上运行；Web 终端 <http://localhost:8080> 或宿主机均可，部分命令在容器内结果有限。
- 🌐 在线阅读可学习排查思路；公网 `ping`/`dig` 可在有网络的本地终端练习。

**环境要求：**

- [ ] 🐳 本实验环境已启动：`docker compose up -d`。
- [ ] 知道服务端口：**8081** 站点、**8080** 终端、**3000** Gitea、**2222** SSH。
- [ ] 已完成 [关卡 35](./lesson-35-http-rest-curl.md)（curl 基础）更佳。
- [ ] 可选：已完成 [关卡 06a](./lesson-06a-ssh-setup-and-clone.md) SSH 配置。

---

## 三、边看边做

> 在 **Web 终端** 或 **宿主机** 执行。容器内可能缺少 `ping` 权限或 `systemd`，某步不可用时看「常见错误」。

### 步骤 1：分层排查模型

遇到「访问不了服务」时，按层检查：

```text
1. DNS 能否解析？     → dig / nslookup
2. 网络是否可达？     → ping（ICMP，可能被禁）
3. TCP 端口是否开放？ → curl / ss / nc
4. 应用是否正常？     → curl 路径、HTTP 状态码、docker compose logs
5. 认证/配置是否正确？→ ssh -v、Gitea 日志
```

### 步骤 2：`ping`——可达性（ICMP）

```bash
ping -c 3 127.0.0.1
ping -c 3 localhost
ping -c 3 example.com
```

- `-c 3` 只发 3 个包。
- 云环境或容器内常 **禁止 ping 外网**，失败不一定代表 HTTP 也不通。

### 步骤 3：`curl`——应用层 HTTP/TCP

检查本实验各服务（🐳 在能访问 localhost 的环境）：

```bash
curl -sf -o /dev/null -w "8081 web: %{http_code}\n" http://localhost:8081/
curl -sf -o /dev/null -w "3000 gitea: %{http_code}\n" http://localhost:3000/
curl -sf -o /dev/null -w "8080 terminal: %{http_code}\n" http://localhost:8080/
```

`-w` 打印状态码；`-sf` 失败时静默且非零退出。

仅测 TCP 连接（不发完整 HTTP）：

```bash
curl -sf telnet://localhost:3000 2>&1 | head -3 || nc -zv localhost 3000 2>&1
```

（`nc` 未安装时可跳过。）

### 步骤 4：`ss` 查看监听端口

```bash
ss -tlnp 2>/dev/null | grep -E '8080|8081|3000|2222' || ss -tln | grep -E '8080|8081|3000|2222'
```

在 **宿主机** 上应看到 Docker 映射的 0.0.0.0:8081 等。

在 Web 终端 **容器内**，通常 **看不到** 宿主机 3000 端口——这是正常的，应在宿主机或用 curl 测 localhost。

### 步骤 5：`lsof` 查占用（宿主机）

```bash
lsof -i :8081 2>/dev/null | head -5
lsof -i :3000 2>/dev/null | head -5
```

若 `port already allocated`，用此命令找谁占用了端口。

### 步骤 6：DNS——`dig` 与 `nslookup`

```bash
dig +short example.com
dig +short github.com A

nslookup example.com
```

检查本机 DNS 是否工作：

```bash
dig +short localhost
# 通常无 A 记录；127.0.0.1 由 /etc/hosts 提供
grep localhost /etc/hosts
```

Gitea 在本地用 `localhost`，一般 **不依赖** 外网 DNS；clone URL 用 `http://localhost:3000/...` 即可。

### 步骤 7：SSH 调试——`ssh -v`（🐳 端口 2222）

本实验 Gitea SSH 映射：**宿主机 2222 → 容器 22**。

```bash
ssh -v -p 2222 -o BatchMode=yes -o ConnectTimeout=5 git@localhost 2>&1 | head -30
```

- `-v`  verbose，显示握手步骤。
- `BatchMode=yes` 非交互，便于脚本与练习。
- 未配置公钥时可能看到 `Permission denied (publickey)`——说明 **端口通、SSH 服务在**，只是认证未通过（参见 [关卡 06a](./lesson-06a-ssh-setup-and-clone.md)）。

对比错误类型：

| 现象 | 可能原因 |
|------|----------|
| `Connection refused` | 2222 未监听，compose 未启动 gitea |
| `Connection timed out` | 防火墙或错误 IP/端口 |
| `Permission denied (publickey)` | 网络 OK，需配置密钥 |

### 步骤 8：结合 Docker 日志

```bash
docker compose logs gitea --tail 20
docker compose ps
```

HTTP 200 但功能异常时，应用层日志比 `ping` 更有用。

### 步骤 9：playground-hello clone 路径检查

```bash
# HTTP clone 是否可达（替换 owner）
curl -sI http://localhost:3000/playground/playground-hello | head -5
```

404 检查 owner/仓库名；401/302 可能与登录有关，浏览器能打开即可。

---

## 四、如何确认自己做对了

```bash
curl -sf http://localhost:8081/ >/dev/null && echo "web reachable"
curl -sf http://localhost:3000/ >/dev/null && echo "gitea reachable"
ssh -p 2222 -o BatchMode=yes -o ConnectTimeout=3 git@localhost 2>&1 | grep -qE 'denied|Authentications' && echo "ssh port open"
dig +short example.com | grep -q '.' && echo "dns OK"
```

- [ ] ✓ 能说出 ping 与 curl 分别验证哪一层
- [ ] ✓ 四个实验端口与服务的对应关系正确
- [ ] ✓ 🐳 在宿主机或合适环境用 `ss`/`lsof` 看过监听端口
- [ ] ✓ 用过 `dig` 或 `nslookup` 解析至少一个公网域名
- [ ] ✓ 见过 `ssh -v` 输出中的连接/认证阶段信息

---

## 五、常见错误

### ❌ 容器内 `ping localhost` OK，但 `curl localhost:3000` 失败

**可能原因：** 在 terminal 容器内，`localhost:3000` 指向 **本容器**，不是 Gitea。

**解决方法：** 对 Gitea 用宿主机浏览器/curl，或 compose 网络内用 `http://gitea:3000`（从其他容器）；学习者通常用 **宿主机** `localhost:3000`。

### ❌ `ping: permission denied` 或 `Operation not permitted`

**可能原因：** 容器缺少 CAP_NET_RAW。

**解决方法：** 用 `curl` 代替 ping 测连通；或在宿主机执行 ping。

### ❌ `ss: command not found`

**可能原因：** 最小镜像未安装 iproute2。

**解决方法：** 用 `netstat -tln`（若可用）或宿主机 `ss`；本关理解概念即可。

### ❌ SSH 连 22 端口失败

**可能原因：** 本实验 SSH 在 **2222**，不是 22。

**解决方法：** `ssh -p 2222 git@localhost`；clone URL 使用 `ssh://git@localhost:2222/...`。

---

## 六、练习/思考题

1. 模拟故障：执行 `docker compose stop gitea`，用 `curl` 与 `docker compose ps` 记录现象，再 `docker compose start gitea` 恢复。
2. 在宿主机找占用 8080 的进程（若有冲突），说明与 `docker compose ps` 中 terminal 的关系。
3. 写一段 5 行以内的「排查清单」，给同学解释「浏览器打不开 http://localhost:8081」时你怎么查。
4. **思考题**：为什么生产环境禁止随意 `ping`，却允许 `curl` 健康检查？

**安全提示：** 勿对公网 IP 做 aggressive 端口扫描；本关仅针对 localhost 实验环境。
