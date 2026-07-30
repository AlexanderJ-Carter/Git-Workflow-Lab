#!/usr/bin/env bash
# Deprecated alias: Gitea init prefers docker image entrypoint.
# Host-side recovery still goes through init-gitea-manual.sh.

set -euo pipefail
echo "Note: prefer container entrypoint init; this forwards to init-gitea-manual.sh" >&2
exec "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/init-gitea-manual.sh" "$@"
