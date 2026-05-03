# Git Workflow Lab - Gitea Image
# 基于 Gitea，预配置学习环境

# Pin to specific version for reproducibility and security
FROM gitea/gitea:1.21.11

LABEL maintainer="Git Workflow Lab"
LABEL description="Pre-configured Git learning environment with Gitea"
LABEL version="2.0.0"

# 复制自定义启动脚本并设置权限
COPY docker/gitea/entrypoint.sh /custom-entrypoint.sh
USER root
RUN chmod +x /custom-entrypoint.sh

# Switch back to git user (non-root) for security
USER git

# 使用自定义 entrypoint
ENTRYPOINT ["/custom-entrypoint.sh"]
CMD ["gitea", "web"]
