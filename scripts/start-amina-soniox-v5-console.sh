#!/usr/bin/env bash
# Amina v5_soniox — v2 prompt + build_deepgram_stt (replace.sh, endpointing 300ms).
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

echo "Amina v5_soniox — Nina + Deepgram STT v5 stack. Stopp: Ctrl+C"
exec uv run python -m amina.agent_soniox_v5 console "$@"
