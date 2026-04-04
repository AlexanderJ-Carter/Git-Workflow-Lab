#!/bin/bash
# Git Workflow Lab - 初始化 Gitea 用户和仓库
# 当 Docker 构建失败时使用此脚本手动初始化

set -e

echo "🚀 Git Workflow Lab - Gitea 初始化"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 检查容器是否运行
if ! docker ps | grep -q git-playground-gitea; then
    echo "❌ Gitea 容器未运行"
    echo "请先执行: docker-compose up -d gitea"
    exit 1
fi

# 等待 Gitea 完全启动
echo "⏳ 等待 Gitea 启动..."
for i in {1..30}; do
    if curl -s http://localhost:3000/healthcheck > /dev/null 2>&1; then
        echo "✓ Gitea 已就绪"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Gitea 启动超时"
        exit 1
    fi
    sleep 2
done

# 配置
ADMIN_USER="playground"
ADMIN_PASS="playground2026"
ADMIN_EMAIL="playground@example.com"

# 创建管理员用户
echo ""
echo "📝 创建管理员用户..."
if docker exec -u git git-playground-gitea gitea admin user list 2>/dev/null | grep -q "${ADMIN_USER}"; then
    echo "✓ 用户已存在: ${ADMIN_USER}"
else
    docker exec -u git git-playground-gitea gitea admin user create \
        --username "${ADMIN_USER}" \
        --password "${ADMIN_PASS}" \
        --email "${ADMIN_EMAIL}" \
        --admin \
        --must-change-password=false > /dev/null 2>&1 && \
    echo "✓ 用户创建成功: ${ADMIN_USER}" || \
    echo "✗ 用户创建失败"
fi

# 创建示例仓库
echo ""
echo "📦 创建示例仓库..."

create_repo() {
    local repo_name=$1
    local repo_desc=$2

    if curl -s "http://localhost:3000/api/v1/repos/${ADMIN_USER}/${repo_name}" \
       -u "${ADMIN_USER}:${ADMIN_PASS}" | grep -q '"name"'; then
        echo "✓ 仓库已存在: ${repo_name}"
        return
    fi

    if curl -s -X POST "http://localhost:3000/api/v1/user/repos" \
       -H "Content-Type: application/json" \
       -u "${ADMIN_USER}:${ADMIN_PASS}" \
       -d "{
           \"name\": \"${repo_name}\",
           \"description\": \"${repo_desc}\",
           \"private\": false,
           \"auto_init\": true,
           \"license\": \"MIT\",
           \"readme\": \"Default\"
       }" > /dev/null 2>&1; then
        echo "✓ 仓库创建成功: ${repo_name}"
    else
        echo "✗ 仓库创建失败: ${repo_name}"
    fi
}

create_repo "hello-git" "🎓 Git 学习练习仓库 - 你的第一个仓库"
create_repo "git-workflow-demo" "🔧 Git Workflow 演示仓库 - 分支管理和协作练习"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ 初始化完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 访问地址: http://localhost:3000"
echo "👤 用户名: ${ADMIN_USER}"
echo "🔑 密码: ${ADMIN_PASS}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
