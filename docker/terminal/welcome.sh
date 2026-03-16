#!/bin/bash
# Git Workflow Lab - 欢迎脚本

cat << 'EOF'

╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🎮 欢迎来到 Git Workflow Lab 练习环境！                     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

📚 这是一个预配置好的 Git / Gitea / CI/CD 学习环境。

📌 快速开始：
   1. 创建一个新仓库：mkdir my-project && cd my-project && git init
   2. 克隆远程仓库：git clone http://gitea:3000/playground/playground-hello.git
   3. 查看当前状态：git status

🔧 环境信息：
   - 用户：playground
   - 工作目录：~/projects
   - Git 版本：$(git --version | cut -d' ' -f3)
   - Gitea 地址：http://localhost:3000
   - SSH 端口：2222

💡 常用命令：
   git init          初始化仓库
   git clone <url>   克隆远程仓库
   git status        查看状态
   git add .         添加所有更改
   git commit -m ""  提交更改
   git log --oneline 查看历史
   git branch        查看分支

📖 查看完整教程：打开浏览器访问 http://localhost:8081

🔄 重置环境：在宿主机执行 docker compose down -v

EOF
