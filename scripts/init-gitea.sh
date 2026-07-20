#!/bin/bash
# Git Workflow Lab - Gitea 初始化脚本
# 在容器启动后自动配置学习环境

set -e

echo "🚀 Git Workflow Lab - Initializing..."

# 等待 Gitea 完全启动
echo "⏳ Waiting for Gitea to start..."
for i in {1..60}; do
    if curl -s http://localhost:3000/ > /dev/null 2>&1; then
        echo "✅ Gitea is ready!"
        break
    fi
    if [ $i -eq 60 ]; then
        echo "❌ Gitea failed to start within timeout"
        exit 1
    fi
    sleep 2
done

# 环境变量
GITEA_URL="http://localhost:3000"
ADMIN_USER="${GITEA_ADMIN_USER:-playground}"
ADMIN_PASS="${GITEA_ADMIN_PASSWORD:-playground}"
ADMIN_EMAIL="${GITEA_ADMIN_EMAIL:-playground@example.com}"

# 确认 API 可用（跳过安装向导，直接进入正常模式）
if ! curl -s "${GITEA_URL}/api/v1/version" > /dev/null 2>&1; then
    echo "❌ Gitea API 不可用，初始化失败"
    exit 1
fi

# 创建管理员用户（如果不存在）
echo "📝 Setting up admin user..."
if ! curl -s "${GITEA_URL}/api/v1/users/${ADMIN_USER}" > /dev/null 2>&1; then
    echo "   Admin user not found, creating..."
    gitea admin user create \
        --admin \
        --username "${ADMIN_USER}" \
        --password "${ADMIN_PASS}" \
        --email "${ADMIN_EMAIL}" \
        --must-change-password=false || true
else
    echo "✅ Admin user already exists"
fi

# 创建示例仓库（如果用户存在）
create_repo() {
    local repo_name=$1
    local repo_desc=$2

    curl -s -X POST "${GITEA_URL}/api/v1/user/repos" \
        -H "Content-Type: application/json" \
        -u "${ADMIN_USER}:${ADMIN_PASS}" \
        -d "{
            \"name\": \"${repo_name}\",
            \"description\": \"${repo_desc}\",
            \"private\": false,
            \"auto_init\": true,
            \"license\": \"MIT\",
            \"readme\": \"Default\"
        }" > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        echo "✅ Created repository: ${repo_name}"
    fi
}

# 尝试创建示例仓库
echo "📦 Creating demo repositories..."
create_repo "playground-hello" "🚀 Git 学习练习仓库"
create_repo "playground-ci" "🔧 CI/CD 流水线练习仓库"

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "✨ Setup complete! Happy learning!"
echo "═══════════════════════════════════════════════════════════"
