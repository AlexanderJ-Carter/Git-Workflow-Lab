#!/usr/bin/env bash
# Host-side manual Gitea init (fallback when container already running).
# Prefer the image entrypoint; use this only for recovery.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -f "${ROOT_DIR}/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "${ROOT_DIR}/.env"
  set +a
fi

GITEA_URL="${PUBLIC_GITEA_URL:-http://localhost:3000}"
GITEA_URL="${GITEA_URL%/}"
ADMIN_USER="${GITEA_ADMIN_USER:-playground}"
ADMIN_PASS="${GITEA_ADMIN_PASSWORD:?Set GITEA_ADMIN_PASSWORD in .env}"
ADMIN_EMAIL="${GITEA_ADMIN_EMAIL:-playground@example.com}"

echo "Waiting for Gitea at ${GITEA_URL}..."
for i in $(seq 1 60); do
  if curl -sf "${GITEA_URL}/healthcheck" > /dev/null; then
    break
  fi
  if [[ "$i" -eq 60 ]]; then
    echo "Gitea is not reachable" >&2
    exit 1
  fi
  sleep 2
done

create_repo() {
  local name=$1
  local desc=$2
  local code
  code=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST "${GITEA_URL}/api/v1/user/repos" \
    -H "Content-Type: application/json" \
    -u "${ADMIN_USER}:${ADMIN_PASS}" \
    -d "{\"name\":\"${name}\",\"description\":\"${desc}\",\"private\":false,\"auto_init\":true,\"license\":\"MIT\",\"readme\":\"Default\"}")
  echo "${name}: HTTP ${code}"
}

create_repo "playground-hello" "Git learning starter repository"
create_repo "playground-ci" "CI/CD practice repository"
echo "Done. User: ${ADMIN_USER}"
