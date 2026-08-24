#!/usr/bin/env bash
# Dr Mujo lokal am Mikrofon (kein SIP, keine Cloud).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [[ ! -f .env.local ]]; then
  echo "Fehlt: $ROOT/.env.local"
  exit 1
fi
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
echo "Alans_mujo V3 — Daniel. Stopp: Ctrl+C"
exec uv run python -m alans_mujo_v3.agent console "$@"
