#!/usr/bin/env bash
# Deepgram STT replace map — interaktiv oder: list | add <from> <to> | remove <from>
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLI="$ROOT/src/amina/deepgram_replace.py"
cd "$ROOT"

if [[ $# -eq 0 ]]; then
  exec uv run python "$CLI" interactive
fi

exec uv run python "$CLI" "$@"
