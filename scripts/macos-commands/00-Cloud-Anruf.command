#!/bin/bash
# Doppelklick: Cloud-Agent wählen und Nummer anrufen.
cd /Users/activi/Code/Projects/LiveKit || { echo "Projekt fehlt"; read -r _; exit 1; }
exec ./scripts/call-cloud-pick-agent.sh
