#!/bin/bash
# Git Workflow Lab - 欢迎脚本

cat << 'EOF'

╔═══════════════════════════════════════════════════════════════╗
║   Git Workflow Lab 练习终端                                    ║
╚═══════════════════════════════════════════════════════════════╝

快速开始：
  1. cd ~/projects
  2. git clone http://gitea:3000/playground/playground-hello.git
  3. cd playground-hello && git status

环境信息：
  - 用户：playground
  - 工作目录：~/projects
  - Gitea HTTP：http://localhost:3000
  - Gitea SSH：ssh://git@localhost:2222/playground/playground-hello.git
  - 演示仓库：playground-hello / playground-ci

SSH 示例（需先在 Gitea 添加公钥）：
  ssh -T git@localhost -p 2222
  git clone ssh://git@localhost:2222/playground/playground-hello.git

教程站点：http://localhost:8081
重置环境：宿主机执行 docker compose down -v

EOF
