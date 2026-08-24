#!/usr/bin/env bash
# Amina v2_soniox — Nina, tts-rt-v2, speed 0.9, Soniox-Tags.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -f .env.local ]]; then
  echo "Fehlt: $ROOT/.env.local"
  exit 1
fi
if ! grep -q '^SONIOX_API_KEY=' .env.local; then
  echo "Fehlt SONIOX_API_KEY in .env.local"
  exit 1
fi

echo "Amina v2_soniox — Nina + tts-rt-v2 + 0.9 + [warm]/[calm]. Stopp: Ctrl+C"
exec uv run python -m amina.agent_soniox_v2 console "$@"
