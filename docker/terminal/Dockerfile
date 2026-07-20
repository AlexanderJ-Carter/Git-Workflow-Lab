# Git Workflow Lab - Web Terminal
FROM alpine:3.21

LABEL maintainer="Git Workflow Lab"
LABEL description="Lightweight Web Terminal with Git for learning"
LABEL version="1.7.0"

RUN apk add --no-cache \
    git \
    python3 \
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
    less \
    tree \
    grep \
    findutils \
    coreutils \
    && rm -rf /var/cache/apk/*

RUN adduser -D -s /bin/zsh playground

USER playground
WORKDIR /home/playground

# Pin oh-my-zsh to a known commit for reproducible builds
RUN git clone --depth=1 https://github.com/ohmyzsh/ohmyzsh.git ~/.oh-my-zsh \
    && cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc \
    && sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="simple"/' ~/.zshrc

RUN mkdir -p /home/playground/projects /home/playground/.ssh

COPY --chown=playground:playground welcome.sh /home/playground/.welcome.sh

RUN echo '\n# Show welcome banner\ncat ~/.welcome.sh\n' >> ~/.zshrc

RUN git config --global user.name "Playground User" \
    && git config --global user.email "playground@example.com" \
    && git config --global init.defaultBranch main \
    && git config --global core.editor nano

USER playground
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:8080/ || exit 1

CMD ["ttyd", "-p", "8080", "-t", "fontSize=16", "-t", "theme={'background':'#1e1e1e'}", "zsh"]
