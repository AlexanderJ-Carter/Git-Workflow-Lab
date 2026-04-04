#!/bin/bash
# Git Workflow Lab - Gitea 启动和初始化脚本

set -e

# 启动 Gitea（后台）
echo "Starting Gitea..."
/usr/bin/entrypoint "$@" &

# 等待 Gitea 启动
echo "Waiting for Gitea to be ready..."
for i in {1..60}; do
    if curl -s http://localhost:3000/healthcheck > /dev/null 2>&1; then
        echo "✓ Gitea is ready!"
        break
    fi
    if [ $i -eq 60 ]; then
        echo "✗ Gitea failed to start"
        exit 1
    fi
    sleep 2
done

# 创建管理员用户
echo "Creating admin user..."
ADMIN_USER="${GITEA_ADMIN_USER:-playground}"
ADMIN_PASS="${GITEA_ADMIN_PASSWORD:-playground2026}"
ADMIN_EMAIL="${GITEA_ADMIN_EMAIL:-playground@example.com}"

# 检查用户是否存在
if ! su git -c "gitea admin user list" | grep -q "${ADMIN_USER}"; then
    echo "Creating user: ${ADMIN_USER}"
    su git -c "gitea admin user create \
        --username ${ADMIN_USER} \
        --password ${ADMIN_PASS} \
        --email ${ADMIN_EMAIL} \
        --admin \
        --must-change-password=false"
    echo "✓ User created successfully"
else
    echo "✓ User already exists"
fi

# 创建示例仓库
echo "Creating demo repositories..."

# 使用 API 创建仓库
create_repo() {
    local repo_name=$1
    local repo_desc=$2

    curl -s -X POST "http://localhost:3000/api/v1/user/repos" \
        -H "Content-Type: application/json" \
        -u "${ADMIN_USER}:${ADMIN_PASS}" \
        -d "{
            \"name\": \"${repo_name}\",
            \"description\": \"${repo_desc}\",
            \"private\": false,
            \"auto_init\": true,
            \"license\": \"MIT\",
            \"readme\": \"Default\"
        }" > /dev/null 2>&1 && echo "✓ Created: ${repo_name}" || echo "✗ Failed: ${repo_name}"
}

create_repo "hello-git" "🎓 Git 学习练习仓库 - 第一个仓库"
create_repo "git-workflow-demo" "🔧 Git Workflow 演示仓库"

echo ""
echo "════════════════════════════════════════════"
echo "✨ Git Workflow Lab setup complete!"
echo "════════════════════════════════════════════"
echo "Username: ${ADMIN_USER}"
echo "Password: ${ADMIN_PASS}"
echo "════════════════════════════════════════════"

# 保持容器运行
wait
