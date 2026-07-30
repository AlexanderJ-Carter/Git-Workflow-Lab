#!/usr/bin/env bash
# Validate or generate .env for local Docker lab.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ROOT_DIR}/.env"
EXAMPLE_FILE="${ROOT_DIR}/.env.example"
PLACEHOLDER='CHANGE_ME'

generate_secrets() {
  if [[ ! -f "${EXAMPLE_FILE}" ]]; then
    echo "Missing .env.example" >&2
    exit 1
  fi
  if [[ -f "${ENV_FILE}" ]]; then
    echo ".env already exists: ${ENV_FILE}" >&2
    echo "Remove it first or edit manually." >&2
    exit 1
  fi

  local db_pass admin_pass secret
  db_pass="$(openssl rand -base64 24 | tr -d '\n')"
  admin_pass="$(openssl rand -base64 18 | tr -d '\n')"
  secret="$(openssl rand -base64 32 | tr -d '\n')"

  sed \
    -e "s|^GITEA_DB_PASSWORD=.*|GITEA_DB_PASSWORD=${db_pass}|" \
    -e "s|^GITEA_ADMIN_PASSWORD=.*|GITEA_ADMIN_PASSWORD=${admin_pass}|" \
    -e "s|^GITEA_SECRET_KEY=.*|GITEA_SECRET_KEY=${secret}|" \
    "${EXAMPLE_FILE}" > "${ENV_FILE}"

  echo "Created ${ENV_FILE} with generated secrets."
  echo "Admin password is in .env (GITEA_ADMIN_PASSWORD). Do not commit this file."
}

validate_env() {
  if [[ ! -f "${ENV_FILE}" ]]; then
    echo "Missing .env. Run: make env-init" >&2
    exit 1
  fi

  # shellcheck disable=SC1090
  set -a
  # shellcheck disable=SC1091
  source "${ENV_FILE}"
  set +a

  local failed=0
  require_var() {
    local name=$1
    local value=${!name-}
    if [[ -z "${value}" || "${value}" == *"${PLACEHOLDER}"* ]]; then
      echo "Invalid or placeholder value: ${name}" >&2
      failed=1
    fi
  }

  require_var GITEA_DB_PASSWORD
  require_var GITEA_ADMIN_PASSWORD
  require_var GITEA_SECRET_KEY

  if [[ "${failed}" -ne 0 ]]; then
    echo "Fix .env or regenerate with: make env-init" >&2
    exit 1
  fi

  echo ".env looks valid."
}

usage() {
  cat <<'EOF'
Usage: scripts/check-env.sh [--generate|--check]

  --generate   Create .env from .env.example with random secrets
  --check      Validate required secrets are set (default)
EOF
}

case "${1:---check}" in
  --generate|-g)
    generate_secrets
    ;;
  --check|-c)
    validate_env
    ;;
  -h|--help)
    usage
    ;;
  *)
    usage >&2
    exit 1
    ;;
esac
