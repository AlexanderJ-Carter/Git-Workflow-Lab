# 关卡 35：HTTP、REST 与 curl

**所属阶段**：计算机基础 / 网络与 API  
**本关命令关键词**：`curl`、`GET`/`POST`/`PUT`/`DELETE`、HTTP 状态码、`-i`、`-X`、`-H`、REST

---

## 一、本关目标

- 理解 HTTP 请求方法（GET、POST 等）与常见状态码（200、201、404、401、500）。
- 熟练使用 `curl`：`-i` 看响应头、`-X` 指定方法、`-H` 添加头、`-d` 发送 body。
- 能阅读 REST 风格 API 的路径与 JSON 响应。
- 用 **Gitea API** 做一次真实请求（列出仓库或当前用户信息）。

调用 API、调试 Webhook、检查 CI 里的服务健康检查，都离不开 HTTP 与 curl。

---

## 二、前置条件

**学习模式：**

- 🌐 **在线可学**：HTTP 概念与 curl 语法；可对公网 URL（如 `https://httpbin.org`）练习。
- 🐳 **建议本地实验**：访问本地 Gitea <http://localhost:3000> API，使用 `.env` 中的管理员账号。

**环境要求：**

- [ ] 已完成 [关卡 00b](./lesson-00-terminal-basics.md)（含 `curl` 入门）。
- [ ] 🐳 Gitea 已启动；知道管理员用户名/密码（`.env` 中 `GITEA_ADMIN_USER` / `GITEA_ADMIN_PASSWORD`）。
- [ ] 🐳 可选：已存在 `playground-hello` 仓库，便于 API 返回非空列表。

---

## 三、边看边做

### 步骤 1：HTTP 方法与 REST 直觉

| 方法 | 常见用途 | 是否常有 body |
|------|----------|---------------|
| GET | 读取资源 | 通常无 |
| POST | 创建资源 | 有 |
| PUT/PATCH | 更新资源 | 有 |
| DELETE | 删除资源 | 可选 |

REST 把 URL 当作资源名，用 HTTP 方法表达操作，例如：

- `GET /api/v1/repos/{owner}/{repo}` — 获取仓库信息
- `POST /api/v1/user/repos` — 创建仓库

### 步骤 2：状态码速查

| 码 | 含义 | 典型场景 |
|----|------|----------|
| 200 | OK | GET 成功 |
| 201 | Created | POST 创建成功 |
| 204 | No Content | DELETE 成功无 body |
| 401 | Unauthorized | 未带 Token / 密码错误 |
| 404 | Not Found | 路径或资源不存在 |
| 500 | Internal Server Error | 服务端异常 |

### 步骤 3：curl 基础——只看 body

```bash
curl -s https://httpbin.org/get
curl -s "https://httpbin.org/get?repo=playground-hello"
```

`-s` 静默进度条，适合脚本。

### 步骤 4：`-i` 查看响应头

```bash
curl -si https://httpbin.org/status/200 | head -15
curl -si https://httpbin.org/status/404 | head -5
```

第一行形如 `HTTP/1.1 200 OK`，即状态行。

### 步骤 5：`-X` 与 `-H`、`-d` 发送 POST

```bash
curl -s -X POST https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"name":"playground-hello","private":false}' \
  | head -20
```

httpbin 会把收到的 headers 与 body 回显，便于学习。

### 步骤 6：Gitea API——未认证与 401

```bash
curl -si http://localhost:3000/api/v1/version | head -10
curl -si http://localhost:3000/api/v1/user | head -5
```

`/api/v1/version` 通常无需登录；`/api/v1/user` 未带凭证时常见 **401**。

### 步骤 7：Gitea API——Basic 认证（🐳）

将 `<USER>`、`<PASS>` 换成 `.env` 中的管理员账号：

```bash
curl -s -u "<USER>:<PASS>" http://localhost:3000/api/v1/user | head -5
```

预期：JSON 中包含 `"login"` 等字段，状态码 200。

列出当前用户的仓库：

```bash
curl -s -u "<USER>:<PASS>" \
  "http://localhost:3000/api/v1/user/repos?limit=5" \
  | grep -o '"name":"[^"]*"' | head -5
```

若已有 `playground-hello`，应能在列表中看到 `"name":"playground-hello"`。

### 步骤 8：获取指定仓库信息

```bash
# 若仓库在 playground 组织下：
curl -s -u "<USER>:<PASS>" \
  http://localhost:3000/api/v1/repos/playground/playground-hello \
  | grep -E '"name"|"html_url"|"default_branch"'
```

404 时检查 owner 名是 `playground` 还是你的个人用户名。

### 步骤 9：与 CI 健康检查对照

本仓库 `docker-compose.yml` 中 Gitea healthcheck：

```text
curl -sf http://127.0.0.1:3000/healthcheck
```

- `-f`：HTTP 4xx/5xx 时 curl 以非零退出，便于脚本判断失败。
- 你在 [关卡 34](./lesson-34-docker-basics.md) 见过的 `curl -sf http://localhost:8081/`，是同一模式。

---

## 四、如何确认自己做对了

```bash
curl -sf http://localhost:3000/api/v1/version >/dev/null && echo "gitea api OK"
curl -si http://localhost:3000/api/v1/user 2>/dev/null | head -1 | grep -q "401" && echo "unauth 401 OK"
# 认证后（替换账号）：
# curl -sf -u "USER:PASS" http://localhost:3000/api/v1/user | grep -q login && echo "auth OK"
```

- [ ] ✓ 能解释 GET 与 POST 的区别
- [ ] ✓ 见过 200 与 404（或 401）的响应头第一行
- [ ] ✓ 用过 `curl -H` 设置 `Content-Type`
- [ ] ✓ 🐳 用 Basic 认证成功调用 Gitea `/api/v1/user`
- [ ] ✓ 知道 `-i`、`-s`、`-f`、`-u` 的常见用途

---

## 五、常见错误

### ❌ `curl: (7) Failed to connect to localhost:3000`

**可能原因：** Gitea 容器未启动；端口错误或防火墙。

**解决方法：** `docker compose ps`；等待 healthcheck 通过后再 curl。

### ❌ 401 Unauthorized

**可能原因：** 用户名/密码错误；API 需要 Token 而非密码（部分 Gitea 配置）。

**解决方法：** 核对 `.env`；或在 Gitea Web → Settings → Applications 创建 Access Token，改用：

```bash
curl -H "Authorization: token YOUR_TOKEN" http://localhost:3000/api/v1/user
```

### ❌ JSON 里中文乱码

**可能原因：** 终端编码；未指定 Accept。

**解决方法：** `curl -s ... | jq .`（见 [关卡 38](./lesson-38-json-yaml-devops.md)）；或 `export LANG=C.UTF-8`。

### ❌ Shell 引号导致 JSON 无效

**可能原因：** 单引号/双引号嵌套错误。

**解决方法：** JSON body 用单引号包裹整体，内部双引号；或 `@file.json` 从文件读取。

---

## 六、练习/思考题

1. 用 `curl -si` 请求 `https://httpbin.org/redirect/2`，观察几次 302/301 与最终 200（可加 `-L` 跟随重定向）。
2. 🐳 调用 `GET /api/v1/repos/search?limit=1`，在响应里找到 `full_name` 字段。
3. 对比浏览器访问 Gitea 仓库页与 API 返回的 `html_url` 是否一致。
4. **思考题**：为什么 API 认证推荐 Access Token，而不是在脚本里写明文密码？

**安全提示：** 不要把 Token 或密码提交到 `playground-hello` 仓库；练习完删除 shell 历史中的 `-u user:pass`（或改用 Token 环境变量）。
