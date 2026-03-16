# Git Workflow Lab - Gitea Image
# 基于 Gitea，预配置学习环境

FROM gitea/gitea:latest

LABEL maintainer="Git Workflow Lab"
LABEL description="Pre-configured Git learning environment with Gitea"
LABEL version="1.0.0"

# 复制初始化脚本
COPY scripts/init-gitea.sh /docker-entrypoint-init.d/

# 设置权限（保持官方 entrypoint 与启动方式不变）
USER root
RUN chmod +x /docker-entrypoint-init.d/init-gitea.sh
