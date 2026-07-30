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
    echo "Gitea is not reachable at ${GITEA_URL}" >&2
    echo "Tip: ensure containers are up (make docker-up) and PUBLIC_GITEA_URL is reachable from this host." >&2
    exit 1
  fi
  sleep 2
done

ensure_repo() {
  local name=$1
  local desc=$2
  local code
  code=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST "${GITEA_URL}/api/v1/user/repos" \
    -H "Content-Type: application/json" \
    -u "${ADMIN_USER}:${ADMIN_PASS}" \
    -d "{\"name\":\"${name}\",\"description\":\"${desc}\",\"private\":false,\"auto_init\":true,\"license\":\"MIT\",\"readme\":\"Default\"}")

  case "${code}" in
    201)
      echo "${name}: created (HTTP ${code})"
      ;;
    409)
      echo "${name}: already exists (HTTP ${code}) — ok"
      ;;
    *)
      echo "${name}: unexpected HTTP ${code}" >&2
      return 1
      ;;
  esac
}

ensure_repo "playground-hello" "Git learning starter repository"
ensure_repo "playground-ci" "CI/CD practice repository"
echo "Done. User: ${ADMIN_USER} @ ${GITEA_URL}"
