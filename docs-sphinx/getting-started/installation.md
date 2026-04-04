# 安装指南

本指南将帮助你快速搭建 Git Workflow Lab 学习环境。

## 系统要求

### 必需软件

- **Docker** >= 24.0
- **Docker Compose** >= 2.20
- **Git** >= 2.40

### 推荐配置

- **CPU**: 2 核心以上
- **内存**: 4GB 以上
- **磁盘**: 10GB 可用空间

## 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/AlexanderJ-Carter/Git-Workflow-Lab.git
cd Git-Workflow-Lab
```

### 2. 配置环境变量

复制环境变量模板：

```bash
cp .env.example .env
```

编辑 `.env` 文件，**必须修改以下配置**：

```bash
# 数据库密码（至少 16 位随机字符）
GITEA_DB_PASSWORD=your_strong_password_here

# Gitea 管理员密码（至少 12 位）
GITEA_ADMIN_PASSWORD=your_admin_password_here

# 安全密钥（至少 32 位随机字符）
GITEA_SECRET_KEY=your_secret_key_here
```

生成随机密码：

```bash
# Linux/macOS
openssl rand -base64 24

# 或使用 Python
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. 启动服务

```bash
docker-compose up -d
```

等待服务启动（首次启动需要拉取镜像，可能需要几分钟）：

```bash
# 查看启动日志
docker-compose logs -f
```

### 4. 验证安装

访问以下地址确认服务正常：

| 服务 | 地址 | 说明 |
|------|------|------|
| 教程网站 | http://localhost:8081 | Nginx 静态网站 |
| Web 终端 | http://localhost:8080 | ttyd 终端 |
| Gitea | http://localhost:3000 | Git 托管平台 |

## 常见问题

### 端口被占用

如果默认端口被占用，编辑 `docker-compose.yml` 修改端口映射：

```yaml
services:
  web:
    ports:
      - "8082:80"  # 改为其他端口
```

### Docker 权限问题

Linux 用户可能需要将用户加入 docker 组：

```bash
sudo usermod -aG docker $USER
# 注销后重新登录生效
```

### Windows/macOS Docker Desktop

确保 Docker Desktop 已启动，并分配了足够的资源（Settings > Resources）。

## 下一步

- {doc}`quickstart` - 快速开始学习
- {doc}`../environment/docker-setup` - 详细环境配置
- {doc}`../lessons/index` - 课程目录
