# 关卡 34：Docker 基础与本实验环境

**所属阶段**：计算机基础 / 容器  
**本关命令关键词**：`docker`、`docker compose`、`image`、`container`、`ps`、`logs`、`exec`

---

## 一、本关目标

- 理解 **镜像（Image）** 与 **容器（Container）** 的区别：镜像是模板，容器是运行实例。
- 掌握常用命令：`docker ps`、`docker logs`、`docker exec`、`docker compose up/down`。
- 读懂 **本仓库** 的 `docker-compose.yml`：web、gitea、terminal、db 四个服务如何协作。
- 能把端口映射（8081/8080/3000/2222）与服务对应起来。

Git Workflow Lab 本身跑在 Docker 里——理解 compose 文件，等于理解你的「练习场」是怎么搭起来的。

---

## 二、前置条件

**学习模式：**

- 🐳 **建议本地实验**：需要在本机（或能访问 Docker 的环境）运行 `docker compose` 命令。
- 🌐 **在线只读**：可阅读 `docker-compose.yml` 与本文理解架构，无需启动容器。

**环境要求：**

- [ ] 已安装 Docker 与 Docker Compose v2。
- [ ] 🐳 在仓库根目录执行过 `docker compose up -d`（或准备在本关跟随操作）。
- [ ] 了解 [关卡 00：安装与配置](./lesson-00-install-and-config.md) 中的端口说明。
- [ ] 阅读本文件时，可对照仓库根目录的 `docker-compose.yml`。

---

## 三、边看边做

> 🐳 以下命令在 **宿主机**（安装了 Docker 的机器）上执行，不是在 Web 终端容器内——除非你的 Web 终端已挂载 Docker socket（本课程默认 **没有**）。

### 步骤 1：启动本实验环境

在 Git Workflow Lab 仓库根目录：

```bash
cd /path/to/Git-Workflow-Lab   # 换成你的克隆路径
docker compose up -d
docker compose ps
```

**预期：** 看到 `web`、`gitea`、`terminal`、`db` 四个服务，状态为 `running` 或 `healthy`。

### 步骤 2：端口与服务对照

| 服务 | 容器名 | 宿主机端口 | 作用 |
|------|--------|-----------|------|
| web | git-playground-web | **8081** → 80 | Nginx 教程站点，挂载 `site/` 与 `docs/` |
| terminal | git-playground-terminal | **8080** → 8080 | ttyd Web 终端 |
| gitea | git-playground-gitea | **3000**、**2222** | Git 托管 HTTP + SSH |
| db | git-playground-db | （内部） | PostgreSQL，供 Gitea 使用 |

在浏览器验证：

- <http://localhost:8081> — 教程首页
- <http://localhost:8080> — Web 终端
- <http://localhost:3000> — Gitea

### 步骤 3：读懂 compose 片段——web 服务

`docker-compose.yml` 中 web 部分核心逻辑：

```yaml
web:
  image: nginx:alpine
  ports:
    - "8081:80"
  volumes:
    - ./site:/usr/share/nginx/html
    - ./docs:/usr/share/nginx/html/docs:ro
```

- `image`：从 Docker Hub 拉取 nginx 镜像。
- `ports`：`宿主机:容器` → 访问 localhost:8081 等于访问容器内 80 端口。
- `volumes`：把本地 `site/`、`docs/` **挂载**进容器，改本地文件即可反映到网站。

### 步骤 4：gitea 与 db 的依赖

```yaml
gitea:
  depends_on:
    db:
      condition: service_healthy
  environment:
    - GITEA__database__HOST=db:5432
```

- `db` 是服务名，在同一 compose 网络内可用 `db:5432` 访问 PostgreSQL。
- `depends_on` + `healthcheck` 保证数据库就绪后再启动 Gitea。
- 环境变量 `GITEA__*` 来自 `.env` 文件（勿提交 Secrets 到 Git）。

### 步骤 5：`docker compose logs`

```bash
docker compose logs web --tail 20
docker compose logs gitea --tail 30
docker compose logs -f terminal   # Ctrl+C 退出跟随
```

排查「Gitea 起不来」「终端 502」时，先看 logs。

### 步骤 6：`docker exec` 进入容器（只读探索）

```bash
docker exec -it git-playground-web sh -c 'ls /usr/share/nginx/html | head'
docker exec -it git-playground-terminal bash -c 'whoami && pwd'
```

- `-it` 交互式；生产环境慎用 root 进入数据库容器修改数据。
- Web 终端里你用的用户通常是 `playground`，与 terminal 镜像配置一致。

### 步骤 7：镜像 vs 容器

```bash
docker compose images
docker image ls | grep -E 'nginx|gitea|terminal|postgres'
```

- `docker compose build` 会构建 `gitea`、`terminal` 的本地镜像（见 `build:` 段）。
- `nginx:alpine`、`postgres:16-alpine` 直接从 registry 拉取。

停止与清理（🐳 练习完可选）：

```bash
docker compose stop
docker compose start    # 再次启动，保留 volume 数据
# docker compose down   # 停止并移除容器（volume 默认保留）
```

### 步骤 8：与 Git 课程的关系

- **8081** 站点里的 `workspace.html` 依赖 **8080** 终端与 **3000** Gitea 同时在线。
- `playground-hello` 等演示仓库数据存在 Gitea volume 中，`docker compose down` 不删 volume 时数据仍在。
- CI 关卡里的 Runner 是 **另一类** 容器；本 compose 未包含 Runner，但概念相同。

---

## 四、如何确认自己做对了

```bash
docker compose ps --format 'table {{.Name}}\t{{.Status}}\t{{.Ports}}'
curl -sf http://localhost:8081/ >/dev/null && echo "web OK"
curl -sf http://localhost:3000/ >/dev/null && echo "gitea OK"
curl -sf http://localhost:8080/ >/dev/null && echo "terminal OK"
```

- [ ] ✓ 四个服务运行中，端口映射与上表一致
- [ ] ✓ 能解释 image 与 container 的区别
- [ ] ✓ 能指出 `docker-compose.yml` 里 web 挂载了哪两个本地目录
- [ ] ✓ 知道 Gitea 如何连接 `db` 服务
- [ ] ✓ 会用 `docker compose logs` 查看某一服务日志

---

## 五、常见错误

### ❌ `port is already allocated`

**可能原因：** 8080/8081/3000/2222 已被其他程序占用。

**解决方法：** `ss -tlnp | grep 8081`（或 `lsof -i :8081`）找占用进程；停止冲突服务或修改 compose 端口映射。

### ❌ Gitea 一直 `starting`，无法访问 3000

**可能原因：** 数据库未就绪；`.env` 缺失或密码不一致。

**解决方法：** `docker compose logs db gitea`；确认已复制 `.env.example` 为 `.env`。

### ❌ 修改 `site/` 后浏览器没变化

**可能原因：** 看错端口（GitHub Pages 在线站 vs 本地 8081）；浏览器缓存。

**解决方法：** 确认访问 <http://localhost:8081>；硬刷新。注意：本课程 **GitHub Pages 不运行 Docker**，仅本地 compose 挂载生效。

### ❌ 在 Web 终端内运行 `docker compose` 报错

**可能原因：** 终端容器内未安装 Docker CLI，或未挂载 `/var/run/docker.sock`。

**解决方法：** 在 **宿主机** Shell 执行 Docker 命令；Web 终端用于 Git 与 Shell 练习。

---

## 六、练习/思考题

1. 画出四服务依赖图：`db` → `gitea`；`web`、`terminal` 独立。
2. 执行 `docker compose config`（宿主机），找出 gitea 使用的 SSH 端口环境变量名。
3. 阅读 [学习模式说明](./learning-modes.md)，对比「在线 GitHub Pages」与「本地 Docker」各能用到 compose 的哪些部分。
4. **思考题**：为什么把 PostgreSQL 放在单独容器里，而不是和 Gitea 打进同一个镜像？

**延伸阅读：**

- [Docker Compose 官方文档](https://docs.docker.com/compose/)
- 本仓库 [关卡 00：安装与配置](./lesson-00-install-and-config.md)
