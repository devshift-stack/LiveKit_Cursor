#!/bin/bash
# Doppelklick im Finder: Amina am Mikrofon.
cd "$(dirname "$0")" || exit 1
exec ./scripts/start-amina-console.sh
