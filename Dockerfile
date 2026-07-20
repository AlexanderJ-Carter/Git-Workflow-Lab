# Git Workflow Lab - Gitea Image
FROM gitea/gitea:1.22.3

LABEL maintainer="Git Workflow Lab"
LABEL description="Pre-configured Git learning environment with Gitea"
LABEL version="1.7.0"

COPY docker/gitea/entrypoint.sh /custom-entrypoint.sh
USER root
RUN chmod +x /custom-entrypoint.sh

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=5 \
    CMD curl -sf http://127.0.0.1:3000/healthcheck || exit 1

USER git
ENTRYPOINT ["/custom-entrypoint.sh"]
CMD ["gitea", "web"]
