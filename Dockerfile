# Git Workflow Lab - Gitea Image
# 基于 Gitea，预配置学习环境

FROM gitea/gitea:latest

LABEL maintainer="Git Workflow Lab"
LABEL description="Pre-configured Git learning environment with Gitea"
LABEL version="2.0.0"

# 复制自定义启动脚本
COPY docker/gitea/entrypoint.sh /custom-entrypoint.sh
RUN chmod +x /custom-entrypoint.sh

# 设置权限
USER root
RUN chmod +x /custom-entrypoint.sh

# 使用自定义 entrypoint
ENTRYPOINT ["/custom-entrypoint.sh"]
CMD ["gitea", "web"]
