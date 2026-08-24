#!/usr/bin/env bash
# Kopiert die .command-Dateien nach ~/Desktop/LiveKit Agents
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${1:-$HOME/Desktop/LiveKit Agents}"
mkdir -p "$DEST"
cp -f "$ROOT/scripts/macos-commands/"*.command "$DEST/"
chmod +x "$DEST/"*.command "$ROOT/scripts/macos-commands/"*.command
xattr -d com.apple.quarantine "$DEST/"*.command 2>/dev/null || true
echo "Desktop: $DEST"
ls -1 "$DEST"/*.command
