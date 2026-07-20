#!/usr/bin/env bash
# Deprecated: Gitea init now runs in docker/gitea/entrypoint.sh.
# This script remains as a documented host-side alias.

set -euo pipefail
exec "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/init-gitea-manual.sh" "$@"
