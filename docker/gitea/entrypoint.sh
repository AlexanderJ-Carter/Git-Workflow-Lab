#!/bin/bash
# Git Workflow Lab - Gitea 启动和初始化脚本

set -euo pipefail

echo "Starting Gitea..."
/usr/bin/entrypoint "$@" &
GITEA_PID=$!

echo "Waiting for Gitea to be ready..."
for i in $(seq 1 60); do
    if curl -sf http://localhost:3000/healthcheck > /dev/null; then
        echo "Gitea is ready"
        break
    fi
    if [ "$i" -eq 60 ]; then
        echo "Gitea failed to start" >&2
        exit 1
    fi
    sleep 2
done

ADMIN_USER="${GITEA_ADMIN_USER:-playground}"
ADMIN_PASS="${GITEA_ADMIN_PASSWORD:?GITEA_ADMIN_PASSWORD is required}"
ADMIN_EMAIL="${GITEA_ADMIN_EMAIL:-playground@example.com}"

echo "Ensuring admin user exists..."
if ! su git -c "gitea admin user list" | grep -q "${ADMIN_USER}"; then
    su git -c "gitea admin user create \
        --username ${ADMIN_USER} \
        --password ${ADMIN_PASS} \
        --email ${ADMIN_EMAIL} \
        --admin \
        --must-change-password=false"
    echo "Admin user created: ${ADMIN_USER}"
else
    echo "Admin user already exists: ${ADMIN_USER}"
fi

create_repo() {
    local repo_name=$1
    local repo_desc=$2
    local status

    status=$(curl -s -o /dev/null -w "%{http_code}" \
        -X POST "http://localhost:3000/api/v1/user/repos" \
        -H "Content-Type: application/json" \
        -u "${ADMIN_USER}:${ADMIN_PASS}" \
        -d "{
            \"name\": \"${repo_name}\",
            \"description\": \"${repo_desc}\",
            \"private\": false,
            \"auto_init\": true,
            \"license\": \"MIT\",
            \"readme\": \"Default\"
        }")

    if [ "$status" = "201" ] || [ "$status" = "409" ]; then
        echo "Repo ready: ${repo_name}"
    else
        echo "Repo create failed (${status}): ${repo_name}" >&2
    fi
}

echo "Creating demo repositories..."
create_repo "playground-hello" "Git learning starter repository"
create_repo "playground-ci" "CI/CD practice repository"

echo "Git Workflow Lab setup complete"
echo "Username: ${ADMIN_USER}"
echo "SSH: git@localhost -p ${GITEA__server__SSH_PORT:-2222}"

wait "${GITEA_PID}"
