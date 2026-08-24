#!/usr/bin/env bash
# Template V1 lokal — nur zum Hören der Vorlage, kein eigener Einsatz.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [[ ! -f .env.local ]]; then
  echo "Fehlt: $ROOT/.env.local"
  exit 1
fi
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
echo "Template V1 (Vorlage). Stopp: Ctrl+C"
exec uv run python -m amina.template_v1.agent console "$@"
