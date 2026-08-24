#!/usr/bin/env bash
# Amina v1_soniox — Mac-Mikrofon, Soniox TTS (Fish bleibt unberührt).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -f .env.local ]]; then
  echo "Fehlt: $ROOT/.env.local"
  exit 1
fi
if ! grep -q '^SONIOX_API_KEY=' .env.local; then
  echo "Fehlt SONIOX_API_KEY in .env.local"
  echo "Key aus Soniox Console (EU-Projekt) eintragen."
  exit 1
fi

echo "Amina v1_soniox — Nina + tts-rt-v2 + speed 0.9 + language=bs. Stopp: Ctrl+C"
exec uv run python -m amina.agent_soniox console "$@"
