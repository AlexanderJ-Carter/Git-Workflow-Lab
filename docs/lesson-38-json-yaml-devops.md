# 关卡 38：JSON、YAML 与 DevOps 配置

**所属阶段**：计算机基础 / 配置与数据格式  
**本关命令关键词**：JSON、YAML、`jq`、`yq`（了解）、验证、GitHub Actions、docker compose

---

## 一、本关目标

- 理解 JSON 与 YAML 的适用场景：API 与程序交换用 JSON；CI/CD、Compose 配置常用 YAML。
- 掌握 JSON 基本结构：对象 `{}`、数组 `[]`、键值对、字符串引号规则。
- 会用 `jq` 过滤与提取字段（若未安装则了解语法，🐳 容器内通常可 `apt` 或已预装）。
- 能阅读本仓库的 **GitHub Actions** 工作流与 **docker-compose.yml** 片段，并做基本语法校验。

读懂 `.github/workflows/*.yml` 和 `docker-compose.yml`，是继续深入 CI/CD 关卡的基石。

---

## 二、前置条件

**学习模式：**

- 🌐 **在线可学**：阅读 YAML/JSON 示例、GitHub 上查看本仓库 workflow 文件；测验可巩固语法。
- 🐳 **建议本地实验**：在终端用 `jq` 解析 Gitea API 的 JSON；用 `docker compose config` 验证 compose。

**环境要求：**

- [ ] 已完成 [关卡 35](./lesson-35-http-rest-curl.md)（API 返回 JSON）。
- [ ] 🐳 可选：`docker compose up -d`，仓库根目录有 `docker-compose.yml`。
- [ ] 能访问本仓库 `.github/workflows/`（在线 GitHub 或本地克隆均可）。

---

## 三、边看边做

### 步骤 1：JSON 基础

```json
{
  "name": "playground-hello",
  "private": false,
  "owner": {
    "login": "playground"
  },
  "tags": ["git", "lab"]
}
```

规则要点：

- 键必须是双引号字符串。
- 最后一个属性后 **不能** 加逗号（部分解析器严格报错）。
- `true` / `false` / `null` 小写，无引号。

在 Shell 中保存示例：

```bash
mkdir -p ~/projects/json-demo && cd ~/projects/json-demo
curl -s https://httpbin.org/json -o sample.json 2>/dev/null || cat > sample.json << 'EOF'
{"slideshow": {"title": "Demo", "slides": [{"title": "Git"}, {"title": "CI"}]}}
EOF
cat sample.json
```

### 步骤 2：`jq` 读取与过滤

```bash
jq . sample.json                    # 格式化输出
jq '.slideshow.title' sample.json
jq '.slideshow.slides[].title' sample.json
jq '.slideshow.slides | length' sample.json
```

Gitea API（🐳 替换账号）：

```bash
curl -s -u "USER:PASS" http://localhost:3000/api/v1/user | jq '{login, id, is_admin}'
curl -s -u "USER:PASS" http://localhost:3000/api/v1/user/repos?limit=3 | jq '.[].name'
```

若 `jq` 未安装：

```bash
command -v jq || echo "install: apt-get update && apt-get install -y jq"
```

### 步骤 3：YAML 基础

YAML 用缩进（通常 2 空格）表示层级，**不用**大括号：

```yaml
name: Hello CI
on:
  push:
    branches:
      - main
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Hello"
```

与 JSON 的对应关系：同一结构两种写法；YAML 更易手写配置。

### 步骤 4：阅读本仓库 GitHub Actions

打开 `.github/workflows/check-lessons.yml`（或 `pages.yml`），识别：

```yaml
name: ...          # 工作流名称
on: ...            # 触发条件
jobs:              # 任务集合
  job-id:
    runs-on: ...
    steps:
      - uses: ...
      - run: ...
```

要点：

- 列表项以 `-` 开头。
- 字符串含 `:` 或特殊字符时加引号。
- 多行脚本用 `|` 或 `>`（见 [关卡 30](./lesson-30-shell-scripting-basics.md)）。

### 步骤 5：阅读 docker-compose.yml

仓库根目录片段：

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "8081:80"
  gitea:
    depends_on:
      db:
        condition: service_healthy
```

- `services` 下每个 key 是一个容器服务。
- 缩进错误会导致 compose 解析失败。

### 步骤 6：验证配置（🐳 宿主机）

```bash
cd /path/to/Git-Workflow-Lab
docker compose config --quiet && echo "compose YAML OK"
docker compose config 2>/dev/null | head -40
```

`docker compose config` 会合并 `.env` 并检查语法，是排查 compose 的利器。

YAML lint（可选，若已安装 `yamllint`）：

```bash
yamllint .github/workflows/check-lessons.yml 2>/dev/null || echo "yamllint optional"
```

### 步骤 7：JSON 校验

```bash
jq empty sample.json && echo "JSON valid"
echo '{bad json}' | jq . 2>&1 | head -3
```

`jq empty` 仅解析不输出，成功则 JSON 合法。

在线：GitHub 编辑 workflow 时也会高亮 YAML 错误。

### 步骤 8：JSON vs YAML 选型

| 场景 | 常用格式 | 本仓库示例 |
|------|----------|------------|
| REST API 响应 | JSON | Gitea `/api/v1/user` |
| GitHub/Gitea Actions | YAML | `.github/workflows/*.yml` |
| Docker Compose | YAML | `docker-compose.yml` |
| package 元数据 | JSON | `package.json`（若存在） |

### 步骤 9：与 CI/CD 关卡衔接

[关卡 10](./lesson-10-first-ci-workflow.md) 让你在 Gitea 写 `.gitea/workflows/*.yml`；语法与 GitHub Actions 高度相似。本关读懂 YAML 后，可直接动手改 `on:`、`jobs:`、`steps:`。

---

## 四、如何确认自己做对了

```bash
jq -e '.slideshow.title' ~/projects/json-demo/sample.json >/dev/null && echo "jq OK"
# 宿主机：
# docker compose config --quiet && echo "compose OK"
```

- [ ] ✓ 能区分 JSON 对象与数组语法
- [ ] ✓ 用过 `jq .` 或 `jq '.path'` 提取字段
- [ ] ✓ 能指出 workflow 文件中 `on`、`jobs`、`steps` 的含义
- [ ] ✓ 读过 `docker-compose.yml` 中至少两个 service 的定义
- [ ] ✓ 知道 `docker compose config` 用于验证 YAML

---

## 五、常见错误

### ❌ YAML：`found character that cannot start any token`

**可能原因：** 用了 Tab 缩进；或 `:` 后缺少空格。

**解决方法：** 统一 2 空格缩进；写成 `key: value` 而非 `key:value`。

### ❌ JSON：`Unexpected token`

**可能原因：**  trailing comma；单引号；注释（JSON 不允许注释）。

**解决方法：** 用 `jq . file` 验证；去掉最后一项后的逗号。

### ❌ `jq` 路径报错 `null`

**可能原因：** 字段不存在或 API 返回错误对象。

**解决方法：** `jq 'paths' file` 探索结构；先 `curl | jq .` 看全貌。

### ❌ compose 与环境变量

**可能原因：** `.env` 缺失导致 `${VAR}` 为空。

**解决方法：** 复制 `.env.example`；`docker compose config` 查看展开后的值（注意勿泄露密码）。

---

## 六、练习/思考题

1. 用 `jq` 从 Gitea `/api/v1/user/repos` 响应中只输出 `{name, clone_url}` 数组。
2. 阅读 `.github/workflows/pages.yml`，用一句话说明它在什么事件下做什么。
3. 把下面 JSON 改写成 YAML（纸面或文件均可）：

   ```json
   {"service": "web", "ports": [8081, 80], "enabled": true}
   ```

4. **思考题**：为什么 GitHub Actions 选 YAML 而不是 JSON 作为 workflow 格式？

**清理（可选）：**

```bash
rm -rf ~/projects/json-demo
```

**延伸阅读：**

- [jq 手册](https://jqlang.github.io/jq/manual/)
- [YAML 官方规范（简明）](https://yaml.org/spec/1.2.2/)
