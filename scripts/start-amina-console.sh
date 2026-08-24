#!/usr/bin/env bash
# Amina am Mac-Mikrofon / Lautsprecher (LiveKit console — kein SIP, keine Cloud).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -f .env.local ]]; then
  echo "Fehlt: $ROOT/.env.local"
  echo "Zuerst: uv run python scripts/write_env_local.py"
  exit 1
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "uv fehlt. Install: https://docs.astral.sh/uv/"
  exit 1
fi

echo "Amina Console — Headset empfohlen. Stopp: Ctrl+C"
echo "Projekt: $ROOT"
echo "Mac: Mikrofon erlauben, wenn gefragt."
echo

exec uv run python -m amina.agent console "$@"
