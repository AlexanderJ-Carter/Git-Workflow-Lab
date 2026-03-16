# Git Workflow Lab - Web Terminal (轻量版)
# 基于 Alpine Linux，提供 Web 终端和 Git 环境

FROM alpine:3.19

LABEL maintainer="Git Workflow Lab"
LABEL description="Lightweight Web Terminal with Git for learning"

# 安装必要的包（包含 ttyd，避免从 GitHub 直接下载）
RUN apk add --no-cache \
    git \
    vim \
    nano \
    curl \
    wget \
    bash \
    zsh \
    openssh-client \
    ca-certificates \
    tzdata \
    ttyd \
    && rm -rf /var/cache/apk/*

# 创建练习用户
RUN adduser -D -s /bin/zsh playground

# 配置 Git
USER playground
WORKDIR /home/playground

# 配置 zsh 和欢迎信息
RUN git clone --depth=1 https://github.com/ohmyzsh/ohmyzsh.git ~/.oh-my-zsh \
    && cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc \
    && sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="simple"/' ~/.zshrc

# 创建工作目录
RUN mkdir -p /home/playground/projects \
    && mkdir -p /home/playground/.ssh

# 复制欢迎脚本
COPY --chown=playground:playground welcome.sh /home/playground/.welcome.sh

# 配置 zsh 自动显示欢迎信息
RUN echo '\n# 显示欢迎信息\ncat ~/.welcome.sh\n' >> ~/.zshrc

# 配置 Git 默认设置
RUN git config --global user.name "Playground User" \
    && git config --global user.email "playground@example.com" \
    && git config --global init.defaultBranch main \
    && git config --global core.editor nano

USER root

# 暴露端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# 启动 ttyd
CMD ["ttyd", "-W", "-p", "8080", "-t", "fontSize=16", "-t", "theme={'background':'#1e1e1e'}", "zsh"]
